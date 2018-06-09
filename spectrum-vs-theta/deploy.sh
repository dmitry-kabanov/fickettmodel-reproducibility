#!/usr/bin/env bash

if [[ $# -eq 0 ]]; then
    echo 'USAGE: deploy.sh <target directory for deploy>'
    exit 2
else
    _mnt_point=$1
fi


_expname=${PWD#$HOME/}
_targetdir=${_mnt_point}/${_expname}

mkdir -p ${_targetdir}

rsync -avz --exclude="*.so" \
           --exclude="*.pyc" \
           --exclude="__pycache__" \
           --exclude="code/tests/*" \
           --delete-excluded \
           code \
           job.sh \
           run.py \
           ${_targetdir}

mkdir -p "${_targetdir}/_output"
mkdir -p "${_targetdir}/_assets"

unset _mnt_point
unset _expname
unset _targetdir
