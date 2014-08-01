#!/usr/bin/env bash
# -*- mode: shell; coding: utf-8 -*-
# (c) Valik mailto:vasnake@gmail.com

PROJECT_DIR="/home/valik/data/projects/translit.bot"

main() {
    #~ createVirtualenv
    #~ makeSourceDistribution
    #~ installDevelop
    #~ createRequirements

    runBot
}

runBot() {
    pushd "${PROJECT_DIR}"
    source env/bin/activate
    export PYTHONIOENCODING=UTF-8
    export TRANSBOT_USER='translit.bot@gmail.com'
    export TRANSBOT_PASSWORD='secret'
    export TRANSBOT_SERVER='gmail.com'
    python -u -m translitbot
}

################################################################################

createVirtualenv() {
    pushd "${PROJECT_DIR}"
    sudo curl https://raw.githubusercontent.com/pypa/pip/master/contrib/get-pip.py | python -
    sudo pip install virtualenv
    virtualenv env
}

makeSourceDistribution() {
    pushd "${PROJECT_DIR}"
    source env/bin/activate
    python setup.py sdist
}

installDevelop() {
    pushd "${PROJECT_DIR}"
    source env/bin/activate
    python setup.py develop
}

createRequirements() {
    pushd "${PROJECT_DIR}"
    source env/bin/activate
    pip freeze > requirements.txt
    cat requirements.txt
}

main
