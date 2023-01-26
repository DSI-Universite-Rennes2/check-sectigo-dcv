#!/bin/bash
# -----------------------------------------------------------------------------
# SPDX-License-Identifier: GPL-3.0-or-later
# License-Filename: LICENSE 
LDIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
echoerr() { echo "$@" 1>&2; }

set -e

BASEDIR=$(realpath "$LDIR"/..)
VENV_DIRNAME='.venv'

# Force to export all declared vars in env file
set -a
# shellcheck disable=SC1091 disable=SC1090
source "$BASEDIR"/config/config.env
set +a

rm -rf "${BASEDIR:?}/${VENV_DIRNAME}"
cd "$BASEDIR"
python3 -m venv --system-site-packages "$VENV_DIRNAME" 
# shellcheck disable=SC1091 disable=SC1090
source "$BASEDIR/${VENV_DIRNAME}/bin/activate"
"$BASEDIR/${VENV_DIRNAME}"/bin/pip3 install -r "$LDIR"/requirements.txt

# Add DCV Class to cert_manager lib
cp "$LDIR/dcv.py" "${BASEDIR}/${VENV_DIRNAME}/lib/python3.8/site-packages/cert_manager/dcv.py"
cd "${BASEDIR}/${VENV_DIRNAME}"
patch -p1 < "$LDIR/patch-add-dcv.diff"
