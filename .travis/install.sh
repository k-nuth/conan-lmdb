#!/bin/bash

set -e
set -x

if [[ "$(uname -s)" == 'Darwin' ]]; then
    brew update || brew update
    brew outdated pyenv || brew upgrade pyenv
    brew install pyenv-virtualenv
    brew install cmake || true

    if which pyenv > /dev/null; then
        eval "$(pyenv init -)"
    fi

    pyenv install 3.7.1
    pyenv virtualenv 3.7.1 conan
    pyenv rehash
    pyenv activate conan
fi

pip install conan_package_tools==0.35.0 > /dev/null
# pip install kthbuild==0.0.14 > /dev/null
pip install kthbuild --upgrade > /dev/null


#conan remote add conan_bzip2 https://knuth.jfrog.io/artifactory/api/conan/knuth

conan user
