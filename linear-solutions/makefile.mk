asset  := linear-time-series.pdf
script := plot-linear-time-series.py
data   := $(wildcard $(exp)/_output/*/detonation-velocity.txt)

asset_list += $(exp)/_assets/$(asset)

$(exp) : $(BUILD_DIR)/$(asset)

$(BUILD_DIR)/$(asset) : $(exp)/_assets/$(asset)

$(exp)/_assets/$(asset) : $(exp)/$(script)
	cd ${<D} && python ${<F}

$(exp)/$(script) : $(data)

asset  := linear-perturbations.pdf
script := plot-linear-perturbations.py
data   := $(wildcard $(exp)/_output/*/profiles/*)

asset_list += $(exp)/_assets/$(asset)

$(exp) : $(BUILD_DIR)/$(asset)

$(BUILD_DIR)/$(asset) : $(exp)/_assets/$(asset)

$(exp)/_assets/$(asset) : $(exp)/$(script)
	cd ${<D} && python ${<F}

$(exp)/$(script) : $(data)
