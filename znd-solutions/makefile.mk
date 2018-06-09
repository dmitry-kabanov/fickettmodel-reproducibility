asset  := znd-solutions.pdf
script := plot-znd-solutions.py
data   := $(wildcard $(exp)/_output/*/znd-solution.txt)

asset_list += $(exp)/_assets/$(asset)

$(exp) : $(BUILD_DIR)/$(asset)

$(BUILD_DIR)/$(asset) : $(exp)/_assets/$(asset)

$(exp)/_assets/$(asset) : $(exp)/$(script)
	cd ${<D} && python ${<F}

$(exp)/$(script) : $(data)
