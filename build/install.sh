#!/bin/bash
# -----------------------------------------------------------------------------
# SPDX-License-Identifier: GPL-3.0-or-later
# License-Filename: LICENSE 
LDIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
echoerr() { echo "$@" 1>&2; }

BASEDIR=$(realpath "$LDIR/..")

# error = exit
set -e

# -----------------------------------------------------------------------------
TMPDIR=$(mktemp -d -t 'tcs-serverinstall.XXXXXX')
if [[ ! "$TMPDIR" || ! -d "$TMPDIR" ]]; then
    echoerr "Could not create temp dir"
    exit 1
fi
trap 'rm -rf "$TMPDIR"' EXIT

function command_exists () { 
    command -v "$1" >/dev/null 2>&1; 
} 

# -----------------------------------------------------------------------------
# install Debian packages
if command_exists apt
then
    PKGS=$(grep -v '#' "$LDIR"/debian-packages.txt | xargs)
    # we WANT word splitting here..
    # shellcheck disable=SC2086
    apt install $PKGS
fi

# -----------------------------------------------------------------------------
# build python env
"$LDIR"/build-python.sh

cp "$LDIR/check-dcv.cfg" "$BASEDIR/check-dcv.cfg"
sed -i "s#%LDIR%#$BASEDIR#g" "$BASEDIR/check-dcv.cfg"

echo ""
echo ""
echo "To install NRPE check locally :"
echo "cp $BASEDIR/check-dcv.cfg /etc/nagios/nrpe.d/" 
echo "systemctl reload nagios-nrpe-server.service"
