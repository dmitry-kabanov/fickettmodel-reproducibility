#!/usr/bin/env bash
function error_exit() { echo -e "\033[0;31m$@\033[0m"; exit 1; }

if [[ $# -eq 0 ]]; then
    echo "USAGE: $0 <source directory mount point>"
    exit 2
else
    _mnt_point=$1
fi

_expname=${PWD#$HOME/}
_sourcedir=${_mnt_point}/${_expname}

_dir=${_sourcedir}/_output

rsync -azP ${_dir}/N12=0160 _output || error_exit 'ERROR: rsync for N12=160'
rsync -azP ${_dir}/N12=0320 _output || error_exit 'ERROR: rsync for N12=320'
rsync -azP ${_dir}/N12=0640 _output || error_exit 'ERROR: rsync for N12=640'
rsync -azP ${_dir}/N12=1280 _output || error_exit 'ERROR: rsync for N12=1280'

chmod -R a-w ./_output

unset _mnt_point
unset _sourcedir
unset _expname
