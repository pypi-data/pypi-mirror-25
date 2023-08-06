#!/bin/bash
# split.sh -- use fastaq to split FASTA file into chunks.
#
# Usage:  split.sh INFILE CHUNKSIZE
#
stem="${1%.*}"
ext="${1##*.}"
outfile="${stem}-${2}-bp_reads.${ext}"
fastaq chunker --onefile "${1}" - ${2} 1 | fastaq enumerate_names - "${outfile}"
if [ $? -ne 0 ]; then
  echo "ERROR-fastaq failed"
  exit 1
fi
chunks=`fastaq count_sequences "${outfile}"`
echo "$1 split into ${outfile} with ${chunks} ${2}-bp chunks."
