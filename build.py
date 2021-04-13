from conan.packager import ConanMultiPackager


if __name__ == "__main__":
    builder = ConanMultiPackager(username="kth", channel="stable", archs=["x86_64"]
                               , remotes="https://knuth.jfrog.io/artifactory/api/conan/knuth")
    builder.add_common_builds(shared_option_name="lmdb:shared", pure_c=True)
    builder.run()

