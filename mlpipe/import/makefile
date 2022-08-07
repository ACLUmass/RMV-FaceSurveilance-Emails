proot := $(shell git rev-parse --show-toplevel)/
proj_dir := $(proot)/mlpipe/import/
in_dir := $(proot)data/src/
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

all : $(out_dir)$(grp)_$(sz)_lines.json

#make lines from raw blocks scraped out of pdfs
$(out_dir)$(grp)_$(sz)_lines.json : $(out_dir)$(grp)_$(sz)_raw.json $(code_dir)raw2lines.py
	touch $(code_dir)raw2lines.py
	python $(mpdb) $(code_dir)raw2lines.py \
		$(grp) \
		$(out_dir)$(grp)_$(sz)_raw.json \
		$(out_dir)$(grp)_$(sz)_lines.json \
		$(dbg_dir)$(grp)_$(sz)_lines.csv \
		$(dmpf)

#scrape pdf sources and make a database of all the pages
$(out_dir)$(grp)_$(sz)_raw.json : $(code_dir)pdf2raw.py
	touch $(code_dir)pdf2raw.py
	python $(mpdb) $(code_dir)pdf2raw.py \
		$(in_dir) \
		$(grp) \
		$(out_dir)$(grp)_$(sz)_raw.json \
		$(out_dir)$(grp)_$(sz)_crv.json \
		$(dbg_dir)$(grp)_$(sz)_raw.csv \
		$(pgs) $(dmpf)

