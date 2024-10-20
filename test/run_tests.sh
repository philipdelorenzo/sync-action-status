#!/bin/bash
# Author Philip De Lorenzo
# Copyright (C) 2020 The Unity Project, LLC.
# All rights reserved
#
#

set -eou pipefail

# Set the directory of this script
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
PY="${DIR}"/../.python
APP="${DIR}"/../src

run_unit_tests ()
{
    echo "${GITHUB_ACTION}"

    if [[ -n "${GITHUB_ACTION}" ]] && [[ "${GITHUB_ACTION}" == "true" ]]; then
        echo "Running Github Action Unit Tests"
        python -m unittest discover ${APP}
    else
        echo "Running Local Unit Tests"
        "${PY}"/bin/python -m unittest discover ${APP}
    fi
}

##### ----------------------------- #####
# Run Python Test Scripts

usage() { echo "Usage: $0 -u (Unit Tests)"; exit 0; }

[ $# -eq 0 ] && usage
while getopts ":u" o; do
    case "${o}" in
        u)
            echo "************* Unit Tests *************"
            run_unit_tests
            ;;
        *)
            usage
            ;;
    esac
done
