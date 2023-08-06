aakbar
======
Amino-Acid k-mer tools for creating, searching, and analyzing phylogenetic signatures from genomes or reads of DNA.

Prerequisites
-------------
A 64-bit Python 3.4 or greater is required.  8 GB or more of memory is recommended.

The python dependencies of aakbar are: biopython, click>=5.0, click_plugins numpy, pandas, pyfaidx,
and pyyaml.  Running the examples also requires the `pyfastaq  https://pypi.python.org/pypi/pyfastaq`
package.

If you don't have a python installed that meets these requirements, I recommend getting
`Anaconda Python <https://www.continuum.io/downloads>` on MacOSX and Windows for the smoothness
of installation and for the packages that come pre-installed.  Once Anaconda python is installed,
you can get the dependencies like this on MacOSX::

    export PATH=~/anaconda/bin:${PATH}    # you might want to put this in your .profile
    conda install click
    conda install --channel https://conda.anaconda.org/IOOS click-plugins
    conda install --channel https://conda.anaconda.org/bioconda pyfaidx
    conda install --channel https://conda.anaconda.org/bioconda pyfastaq  # only required for examples


Installation
------------
This package is tested under Linux and MacOS using Python 3.5 and is available from the PyPI.  To
install via pip (or pip3 under some distributions) : ::

     pip install aakbar

If you wish to develop aakbar,  download a `release <https://github.com/ncgr/aakbar/releases>`_
and in the top-level directory: ::

	pip install --editable .

If you wish to have pip install directly from git, use this command: ::

	pip install git+https://github.com/ncgr/aakbar.git



Usage
-----
Installation puts a single script called ``aakbar`` in your path.  The usage format is::

    aakbar [GLOBALOPTIONS] COMMAND [COMMANDOPTIONS] [ARGS]

A listing of commands is available via ``aakbar --help``.  Current available commands are:

============================= ====================================================
  calculate_peptide_terms     Write peptide terms and histograms.
  conserved_signature_stats   Stats on signatures found in all input genomes.
  define_set                  Define an identifier and directory for a set.
  define_summary              Define summary directory and label.
  demo_simplicity             Demo self-provided simplicity outputs.
  filter_peptide_terms        Remove high-simplicity terms.
  init_config_file            Initialize a configuration file.
  install_demo_scripts        Copy demo scripts to the current directory.
  intersect_peptide_terms     Find intersecting terms from multiple sets.
  label_set                   Define label associated with a set.
  peptide_simplicity_mask     Lower-case high-simplicity regions in FASTA.
  search_peptide_occurrances  Find signatures in peptide space.
  set_letterfreq_window       Define size of letterfreq window.
  set_plot_type               Define label associated with a set.
  set_simplicity_object       Select simplicity-calculation object.
  show_config                 Print location and contents of config file.
  show_context_object         Print the global context object.
  test_logging                Logs at different severity levels.
============================= ====================================================

Examples
--------

Bash scripts that implement examples for calculating and using signature sets for
Firmicutes and Streptococcus, complete with downloading data from GenBank, will
be created in the (empty) current working directory when you issue the command:

    aakbar install_demo_files

On linux and MacOS, follow the instructions to run the demos.  On Windows, you will
need ``bash`` installed for the scripts to work.


Documentation
-------------
- `Readthedocs documentation <https://aakbar.readthedocs.org/en/latest/index.html>`_


License
-------
aakbar is distributed under a `BSD License`.
