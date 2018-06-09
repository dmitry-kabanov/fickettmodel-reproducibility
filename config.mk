# From http://clarkgrubb.com/makefile-style-guide#prologue
MAKEFLAGS     += --warn-undefined-variables
# Next two lines are commented out because if I use `bash`, then
# the `shell` function fails.
# SHELL         := bash
# .SHELLFLAGS   := -eu -o pipefail
.DEFAULT_GOAL := all

.DELETE_ON_ERROR :

.SUFFIXES :

RM := rm -f
