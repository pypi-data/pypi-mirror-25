This directory contains some BASH scripts that download from GenBank, then
calculates and evaluates sets of peptide signatures. The scripts have been
verified to work under linux and MacOSX.

These scripts (though not aakbar itself) depend on the "pyfastaq" package
to chop genomes up into chunks for testing sensitivity.  Pyfastaq is available
from PYPI: https://pypi.python.org/pypi/pyfastaq.  

There is a single top-level example script "strep10.sh" which calculates
signatures based on 10 Streptococci.  Streptococci is a genus within the
Firmicutes that include medically-important bacteria (the "strep" of strep
throat).  The sensitivity of this set ranges between 3% and 50%, high enough
to be useful. This example takes about an hour to run on a modern laptop,
mostly in searching the non-included genome.

The three helper scripts called by the top-level example script are:
   genbank_downloader.sh - downloads and prepares data using curl
   calculate_signatures.sh - shows how to calculate signatures using aakbar
   split.sh - splits a genome into non-overlapping non-random chunks using fastaq
Each of these helper scripts can be used standalone and includes help that
can be obtained via the '-h' option.

Run "./strep10.sh" when you are ready to see a full demo.