asset  := verification-nonlinear-steady-state.tex
script := generate-verification-table.py
data   := $(wildcard $(exp)/_output/*/detonation-velocity.npz)

asset_list += $(exp)/_assets/$(asset)

$(exp) : $(BUILD_DIR)/$(asset)

$(BUILD_DIR)/$(asset) : $(exp)/_assets/$(asset)

$(exp)/_assets/$(asset) : $(exp)/$(script)
	cd $(<D) && python $(<F) --save

$(exp)/$(script) : $(data) $(exp)/lib_helpers.py
	touch $@
