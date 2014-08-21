Understanding & Evaluating Pathways to Stable Housing
========

Contributors
---

- Chris Bopp
- Cindy Chen
- Isaac Hollander McCreery
- Carl Shan

Requirements
---

For cleaning, you'll need the standard [Anaconda](http://store.continuum.io) install, plus ... (Young-Jin, please fill
this in: Pandas, what else?).  Modeling is all done in Weka, and you'll need a standard Weka install, (we put ours in
`/usr/share/java/weka.jar`; if you put yours somewhere else you'll have to change the classpath in `run_weka.sh`).

Cleaning the data requires about 16GB of free memory; if you don't have that, you're liable to get memory errors.
Modeling, on a 16-core, 32GB machine, I can run about 8 models at once; 12 often fails.

Usage
---

### Cleaning

Just run `make` to clean the data, which is expected in `/mnt/data/allchicago/data/`, into `./clean`.  You can use `make
-j` to help it run faster by multithreading.  Check out `Makefile` for the data dependencies.

Cleaning is all done with [pandas](http://pandas.pydata.org).  `clean.py` is the script used to clean the raw data.  It
deposits cleaned dataframes into `./clean/pickles/` and `./clean/csvs/`, and provides an easy-to-use data accessor,
`clean.load()`.  After running `make`, check out the `diagnostics.ipynb` notebook for example usage.

### Modeling

All modeling is done in [Weka](http://www.cs.waikato.ac.nz/ml/weka/).  `pipeline.py` wraps Weka's functionality into an
easy-to-use python model, which relies on `run_weka.sh` to run Weka from `bash`.  Check out the `models.ipynb` notebook
for example usage of `pipeline`.  Note that, if you build a Pipeline `p` and run `p.model()`, then you want to look over
the results, you can construct an identical Pipeline and access the results without re-running `p.model()`.
