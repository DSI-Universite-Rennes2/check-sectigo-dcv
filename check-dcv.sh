#!/bin/bash
# -----------------------------------------------------------------------------
# SPDX-License-Identifier: GPL-3.0-or-later
# License-Filename: LICENSE 
LDIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
BASEDIR=$(realpath "$LDIR")
PATH="/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin"

# shellcheck disable=SC1091 disable=SC1090
source "$BASEDIR"/.venv/bin/activate

# Force to export all declared vars in env file
set -a
# shellcheck disable=SC1091 disable=SC1090
source "$BASEDIR"/config/config.env
set +a
export PYTHONUNBUFFERED=1

python3 "$LDIR"/check-dcv.py "$@"
