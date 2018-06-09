#!/usr/bin/env bash

_expname=${PWD#$HOME/}
_targetdir=$HOME/shaheen-scratch/${_expname}

mkdir -p ${_targetdir}

rsync -avz --exclude="*.so" \
           --exclude="*.pyc" \
           --exclude="__pycache__" \
           --exclude="code/tests/*" \
           --delete-excluded \
           code \
           job-N12=0160.sh \
           job-N12=0320.sh \
           job-N12=0640.sh \
           job-N12=1280.sh \
           run.py \
           ${_targetdir}

mkdir -p "${_targetdir}/_output"
mkdir -p "${_targetdir}/_output/N12=0160"
mkdir -p "${_targetdir}/_output/N12=0320"
mkdir -p "${_targetdir}/_output/N12=0640"
mkdir -p "${_targetdir}/_output/N12=1280"
mkdir -p "${_targetdir}/_assets"

unset _expname
unset _targetdir
