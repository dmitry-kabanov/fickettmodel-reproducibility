asset := riemann-problem.pdf
script  := plot-riemann-problem-solution.py
data    := $(wildcard $(exp)/_output/results.txt)

asset_list += $(exp)/_assets/$(asset)

$(exp) : $(BUILD_DIR)/$(asset)

$(BUILD_DIR)/$(asset) : $(exp)/_assets/$(asset)

$(exp)/_assets/$(asset) : $(exp)/$(script)
	cd ${<D} && python ${<F}

$(exp)/$(script) : $(data)
