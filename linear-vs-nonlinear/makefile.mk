asset  := linear-vs-nonlinear.pdf
script := plot-linear-vs-nonlinear.py
data   := $(wildcard $(exp)/_output/*/detonation-velocity.txt)

asset_list += $(exp)/_assets/$(asset)

$(exp) : $(BUILD_DIR)/$(asset)

$(BUILD_DIR)/$(asset) : $(exp)/_assets/$(asset)

$(exp)/_assets/$(asset) : $(exp)/$(script)
	cd ${<D} && python ${<F}

$(exp)/$(script) : $(data)
