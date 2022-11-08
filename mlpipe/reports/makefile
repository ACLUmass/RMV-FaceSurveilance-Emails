proot := $(shell git rev-parse --show-toplevel)/
in_dir := $(proot)mlpipe/add_feats/output/
proj_dir := $(proot)/mlpipe/reports/
code_dir := $(proj_dir)code/
out_dir := $(proj_dir)output/
dbg_dir := $(proj_dir)debug/

ifdef dbg
	mpdb := -mpdb
else ifdef dmp
	dmpf := > $(dmp)
endif

.PHONY: all rpt

#all : $(out_dir)$(grp)_$(sz)_raw.json

$(out_dir)fr_rmv.pdf rpt : $(in_dir)log_info.json $(code_dir)logrpt.py 
	python $(mpdb) $(code_dir)logrpt.py \
	  $(in_dir)log_info.json \
	  $(out_dir)fr_rmv_rpt.pdf \
	  $(out_dir)fr_rmv_rpt.txt

