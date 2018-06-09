asset_1 := solution-contact-shock.pdf
asset_2 := solution-contact-rarefaction.pdf
script  := plot-riemann-problem-solution.py
data    := $(wildcard $(exp)/_output/results.txt)

asset_list += $(exp)/_assets/$(asset_1)

$(exp) : $(BUILD_DIR)/$(asset_1)

$(BUILD_DIR)/$(asset_1) : $(exp)/_assets/$(asset_1)

$(exp)/_assets/$(asset_1) : $(exp)/$(script)
	cd ${<D} && python ${<F} I

$(exp)/$(script) : $(data)

asset_list += $(exp)/_assets/$(asset_2)

$(exp) : $(BUILD_DIR)/$(asset_2)

$(BUILD_DIR)/$(asset_2) : $(exp)/_assets/$(asset_2)

$(exp)/_assets/$(asset_2) : $(exp)/$(script)
	cd ${<D} && python ${<F} II

$(exp)/$(script) : $(data)
