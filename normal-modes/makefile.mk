asset  := normal-modes-carpet.pdf
script := plot-carpet.py
data   :=

asset_list += $(exp)/_assets/$(asset)

$(exp) : $(BUILD_DIR)/$(asset)

$(BUILD_DIR)/$(asset) : $(exp)/_assets/$(asset)

$(exp)/_assets/$(asset) : $(exp)/$(script)
	cd ${<D} && python ${<F} > /dev/null

$(exp)/$(script) : $(data) $(exp)/lib_normalmodes.py

asset  := normal-modes-perturbations.pdf
script := plot-normal-mode-perturbations.py
data   :=

asset_list += $(exp)/_assets/$(asset)

$(exp) : $(BUILD_DIR)/$(asset)

$(BUILD_DIR)/$(asset) : $(exp)/_assets/$(asset)

$(exp)/_assets/$(asset) : $(exp)/$(script)
	cd ${<D} && python ${<F} > /dev/null

$(exp)/$(script) : $(data) $(exp)/lib_normalmodes.py
