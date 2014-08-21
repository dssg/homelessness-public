#!/bin/bash

# This script is used by pipeline.py to run Weka in subprocesses.  It takes 3 arguments:
#   - FPATH: the file_path in which to find ${MODELNAME}.csv to convert to ARFF, and in which to put all results
#   - MODELNAME: the name of the CSV to find in FPATH
#   - ALGORITHM: the algorithm to use for Weka: weka.classifiers.${ALGORITHM}

FPATH=$1
MODELNAME=$2
ALGORITHM=$3

# Construct important variables.
CSV=${FPATH%%/}/${MODELNAME}.csv
PREPPEDCSV=${FPATH%%/}/${MODELNAME}_prepped.csv
ARFF=${FPATH%%/}/${MODELNAME}.arff
THRESHOLDS=${FPATH%%/}/${MODELNAME}_thresholds.csv
RESULTS=${FPATH%%/}/${MODELNAME}_results.txt

# Change these if your install of Weka and/or Java is different.
CP='/usr/share/java/weka.jar'
JAVA='/usr/bin/java'

# Replace quoted "?"s, (which Pandas produces,) into unquoted ?s, which Weka understands as missing values
sed 's/"?"/?/g' ${CSV} > ${PREPPEDCSV}
# Convert the CSV into ARFF
${JAVA} -cp ${CP} weka.core.converters.CSVLoader ${PREPPEDCSV} > ${ARFF}
# Run Weka, outputting a threshold-file and detailed results
${JAVA} -cp ${CP} -Xmx4g weka.classifiers.${ALGORITHM} -t ${ARFF} -threshold-file ${THRESHOLDS} -i > ${RESULTS}
