# Main Makefile.

# Check that BUILD_DIR is given by a user as a command-line argument.
ifndef BUILD_DIR
$(error 'BUILD_DIR is not set. USAGE: make BUILD_DIR=<dirname>.')
endif

include config.mk

# List of all numerical experiments.
experiments := linear-vs-nonlinear \
               neutral-stability-quantitative-results \
               bifurcation-diagram \
               spectrum-vs-theta \
               neutral-stability \
               znd-solutions \
               riemann-problem-examples \
               verification-linear-solver \
               verification-nonlinear-solver \
               normal-modes \
               linear-solutions

# Set PYTHONPATH to be able to use the solver's code and helpers.
export PYTHONPATH := ../code:..

# Set SAVE_FIGURES environment variable such that the figures are saved.
# See `helpers.py` module.
export SAVE_FIGURES := 1

# Used by matplotlib to determine parameters for plotting.
export MATPLOTLIBRC := $(CURDIR)

# Used as a dependency for scripts that generate figures.
export matplotlibrc_file := $(MATPLOTLIBRC)/matplotlibrc

# List of all assets.
asset_list :=

# Scripts that generate figures (their filenames start with 'plot'.
plot_scripts := $(shell find . -name "plot*.py")

# Evaluates to the directory name of a makefile in which it is used.
exp = $(patsubst %/makefile.mk,%,\
                 $(word $(words $(MAKEFILE_LIST)),$(MAKEFILE_LIST)))


.PHONY : all $(experiments)
all : $(experiments)

$(BUILD_DIR) :
	mkdir -p $@

$(BUILD_DIR)/%.pdf $(BUILD_DIR)/%.tex: | $(BUILD_DIR)
	cp $< $@

.PHONY : clean
clean :
	$(RM) $(asset_list)

# Generic rule that adds `helpers.py` module and the matplotlib settings
# as prerequisites to the plotting scripts.
$(plot_scripts) : helpers.py $(matplotlibrc_file)
	touch $@

include $(addsuffix /makefile.mk,$(experiments))
