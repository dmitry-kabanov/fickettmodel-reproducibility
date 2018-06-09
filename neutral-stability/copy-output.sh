#!/usr/bin/env bash
if [[ $# -eq 0 ]]; then
    echo "USAGE: $0 <source directory mount point>"
    exit 1
else
    _mnt_point=$1
fi

_expname=${PWD#$HOME/}
_sourcedir=${_mnt_point}/${_expname}

rsync -azP ${_sourcedir}/_output .
chmod -R a-w ./_output

unset _mnt_point
unset _expname
unset _sourcedir
