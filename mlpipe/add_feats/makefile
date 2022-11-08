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

.PHONY: all lns log email

#all : $(out_dir)$(grp)_$(sz)_raw.json

#scrape pdf sources and make a database of all the pages
lns $(out_dir)$(grp)_$(sz)_types.json : $(code_dir)linetypes.py
	touch $(code_dir)linetypes.py
	python $(mpdb) $(code_dir)linetypes.py \
		$(grp) \
		$(in_dir)$(grp)_$(sz)_lines.json \
		$(out_dir)$(grp)_$(sz)_linetypes.json \
		$(dbg_dir)$(grp)_$(sz)_linetypes.csv \
		$(dmpf)

#scrape pdf sources and make a database of all the pages
log $(out_dir)log_info.json : $(code_dir)loginfo.py
	touch $(code_dir)loginfo.py
	python $(mpdb) $(code_dir)loginfo.py \
		$(in_dir)$(grp)_big_enforce_log.json \
		$(out_dir)log_info.json \
		$(dbg_dir)log_info.csv \
		$(dmpf)

#match log entries to their pdf ids
email $(out_dir)$(grp)_$(sz)_email.json : $(code_dir)email2log.py
	touch $(code_dir)email2log.py
	python $(mpdb) $(code_dir)email2log.py \
		$(grp) \
		$(in_dir)$(grp)_big_enforce_log.json \
		$(out_dir)$(grp)_$(sz)_linetypes.json \
		$(out_dir)$(grp)_$(sz)_email2log.json \
		$(out_dir)$(grp)_$(sz)_email_info.json \
		$(dbg_dir)$(grp)_$(sz)_email2log.csv \
		$(dmpf)

