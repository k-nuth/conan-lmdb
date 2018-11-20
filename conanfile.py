from conans import ConanFile, CMake, tools
import sys, os

def option_on_off(option):
    return "ON" if option else "OFF"

class LightningDBCppConan(ConanFile):
    name = "lmdb"
    version = "0.9.22"
    settings = "os", "compiler", "build_type", "arch"
    url = "https://github.com/bitprim/bitprim-conan-lmdb"
    license = "OpenLDAP Public License"



    generators = "cmake"

    options = {"shared": [True, False],
               "fPIC": [True, False]
    }

    default_options = "shared=False", \
        "fPIC=True"

    # exports = "conanfile.py", "mdb.def", "win32/*", "LICENSE.md"    # "CMakeLists.txt",
    exports_sources = ["CMakeLists.txt"]
    build_policy = "missing"

    def configure(self):
        del self.settings.compiler.libcxx #Pure-C 

    def source(self):
        # extension = "zip" if sys.platform == "win32" else "tar.gz" % self.folder_name
        extension = "zip" if sys.platform == "win32" else "tar.gz" #% self.build_folder
        
        base_name = "LMDB_%s" % (self.version)
        zip_name = "%s.%s" % (base_name, extension)
        url = "https://github.com/LMDB/lmdb/archive/%s" % (zip_name)
        self.output.info("Downloading %s..." % url)
        tools.download(url, zip_name)
        tools.unzip(zip_name, ".")
        os.unlink(zip_name)
        os.rename("lmdb-%s" % base_name, "lmdb")

    def build(self):
        # cmake = CMake(self.settings)
        # shared = "-DBUILD_SHARED_LIBS=1" if self.options.shared else ""
        # self.run('cmake %s %s %s' % (self.conanfile_directory, cmake.command_line, shared))
        # self.run("cmake --build . %s" % cmake.build_config)

        cmake = CMake(self)
        cmake.verbose = True
        cmake.definitions["ENABLE_SHARED"] = option_on_off(self.options.shared)
        cmake.definitions["ENABLE_POSITION_INDEPENDENT_CODE"] = option_on_off(self.options.fPIC)

        cmake.configure(source_dir=self.source_folder)
        cmake.build()

    def package(self):
        self.copy("lmdb.h", dst="include", src="lmdb/libraries/liblmdb")
        self.copy("*.lib", dst="lib", src="lib", keep_path=True)
        self.copy("*.a", dst="lib", src="lib", keep_path=True)
        self.copy("*.pdb", dst="lib", src="lib", keep_path=True)
        self.copy("*.dll", dst="bin", src="lib", keep_path=True)
        self.copy("*.so", dst="bin", src="lib", keep_path=True)
        self.copy("*.exe", dst="bin", src="bin", keep_path=True)

    def package_info(self):
        if self.settings.build_type == "Debug":
            self.cpp_info.libs = ["lmdbd"]
        else:
            self.cpp_info.libs = ["lmdb"]
            
        if  self.settings.os == "Windows":
            self.cpp_info.libs.append("ntdll")
        else:
            self.cpp_info.libs.append("pthread")
