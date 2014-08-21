# Makefile for building cleaned CSVs and pickles from raw data

all: master.pkl

master.pkl : clean.py directories \
             providers.pkl \
             master_all.pkl \
             review_details.pkl \
	     entry_disabilities.pkl review_disabilities.pkl \
	     entry_income.pkl exit_income.pkl \
             entry_ncb.pkl exit_ncb.pkl \
             services.pkl
	python clean.py master

providers.pkl : clean.py directories
	python clean.py providers

master_all.pkl : clean.py directories \
                 providers.pkl \
                 review_details.pkl \
	         entry_disabilities.pkl review_disabilities.pkl \
	         entry_income.pkl exit_income.pkl \
                 entry_ncb.pkl exit_ncb.pkl \
                 services.pkl
	python clean.py master_all

entry_details.pkl : clean.py directories
	python clean.py entry_details
entry_disabilities.pkl : clean.py directories
	python clean.py entry_disabilities
entry_income.pkl : clean.py directories
	python clean.py entry_income
entry_ncb.pkl : clean.py directories
	python clean.py entry_ncb

exit_stuff.pkl : clean.py directories
	python clean.py exit_stuff
exit_income.pkl : clean.py directories
	python clean.py exit_income
exit_ncb.pkl : clean.py directories
	python clean.py exit_ncb

review_details.pkl : clean.py directories
	python clean.py review_details
review_disabilities.pkl : clean.py directories
	python clean.py review_disabilities
review_income.pkl : clean.py directories
	python clean.py review_income
review_ncb.pkl : clean.py directories
	python clean.py review_ncb

services.pkl : clean.py directories
	python clean.py services

directories :
	mkdir -p ./clean/pickles
	mkdir -p ./clean/csvs
