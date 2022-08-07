proot := $(shell git rev-parse --show-toplevel)/
in_dir := $(proot)mlpipe/import/output/
proj_dir := $(proot)/mlpipe/add_feats/
code_dir := $(proj_dir)code/
out_dir := $(proj_dir)output/
dbg_dir := $(proj_dir)debug/

ifdef big
  sz := big
else
  sz := small
endif
ifeq ($(sz), small)
  pgs := -f 2
endif

ifdef fr
  grp := fr
else
  grp := msp
endif

ifdef dbg
	mpdb := -mpdb
else ifdef dmp
	dmpf := > $(dmp)
endif

.PHONY: all

#all : $(out_dir)$(grp)_$(sz)_raw.json

#scrape pdf sources and make a database of all the pages
$(out_dir)$(grp)_$(sz)_types.json : $(code_dir)linetypes.py
#$(grp) : $(code_dir)pdf2raw.py
	touch $(code_dir)linetypes.py
	python $(mpdb) $(code_dir)linetypes.py \
		$(grp) \
		$(in_dir)$(grp)_$(sz)_lines.json \
		$(out_dir)$(grp)_$(sz)_linetypes.json \
		$(dbg_dir)$(grp)_$(sz)_linetypes.csv \
		$(dmpf)

