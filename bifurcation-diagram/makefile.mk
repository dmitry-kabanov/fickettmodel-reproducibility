asset_1  := bif-diag-N12=1280-comparator=minima-order=1-start_time=900.pdf
script_1 := plot-bif-diag.py
data_1   := $(exp)/_output-cache/bif-data-N12=1280-minima-order=1-start_time=900.npz

asset_list += $(exp)/_assets/$(asset_1)

$(exp) : $(BUILD_DIR)/$(asset_1)

$(BUILD_DIR)/$(asset_1) : $(exp)/_assets/$(asset_1)

$(exp)/_assets/$(asset_1) : $(exp)/$(script_1)
	cd ${<D} && \
	python ${<F} 1280 --comparator=minima --order=1 --start-time=900

$(exp)/$(script_1) : $(data_1) $(exp)/lib_bifdiag.py


asset_2 := time-series-and-phase-portraits-together.pdf
script_2 := plot-time-series-and-phase-portraits-together.py
data_2   := $(wildcard $(exp)/_output-cache/N12=1280/*/detonation-velocity.npz)

$(exp) : $(BUILD_DIR)/$(asset_2)

$(BUILD_DIR)/$(asset_2) : $(exp)/_assets/$(asset_2)

$(exp)/_assets/$(asset_2) : $(exp)/$(script_2)
	cd ${<D} && python ${<F}

$(exp)/$(script_2) : $(data_2) $(exp)/lib_timeseries.py

$(data_2) $(data_3) $(data_4) $(data_5) $(data_6) $(data_7) : $(exp)/time-series.tar.gz
	# Extract archive.
	tar xf $< -C $(<D)
	# Update timestamps of all extracted data to avoid multiple extractions.
	find $(<D)/_output-cache/N12=1280/ -type f -exec touch {} \;

$(exp)/time-series.tar.gz:
	# Download time-series.tar.gz from Zenodo.org because its ~500 MB.
	curl -L \
		https://zenodo.org/record/1286283/files/time-series-fickett-model.tar.gz?download=1 \
		-o $@
