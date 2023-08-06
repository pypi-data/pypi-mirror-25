#!/bin/bash
docstring="
genbank_downloader.sh -- downloads Genbank links to a species directory,
                         gunzipping, creating metadata, and making symlinks for uniform naming.

Usage:
 genbank_downloader.sh [-q] [-v] [-t TYPE] [-c CODE] GENBANKDIR 
   where:
     TYPE is one of:
          protein (default)
          rna
          genome
          gff
          cds
          stats
      CODE is an arbitrary naming code to go into a metadata entry.
      GENBANKDIR is the part of the directory URL following after \"genbank\"


Output:
  A subdirectory of the current working directory containing the downloaded file,
  a nicely-named symlink to the downloaded file, and a tab-separated metadata file
  named \"metadata.tsv\".

Example:
  genbank_downloader.sh -t genome -c S.mutans bacteria/Streptococcus_mutans/reference/GCA_000007465.2_ASM746v2 protein


Author:
    Joel Berendzen June 9, 2016
"
# default values
prefix="ftp://ftp.ncbi.nlm.nih.gov/genomes/genbank/"
type="protein"
code=""
verbose=""
quiet=""
#
# process arguments
#
while getopts "hvqt:c:" opt; do
  case $opt in
    h)
     echo "${docstring}"
     exit 0
     ;;
    v)
     verbose="-v"
     ;;
    q)
     quiet="-s"
     ;;
    t)
     type="${OPTARG}"
     ;;
    c)
     code="${OPTARG}"
     ;;
   \?)
     echo "Invalid option -$OPTARG" >&2
     echo "${docstring}"
     exit 1
     ;;
    :)
     echo "ERROR-option -$OPTARG requires an argument." >&2
     echo "${docstring}"
     exit 1
     ;;
  esac
done
#
# process type argument
#
case $type in
  protein)
   suffix="_protein.faa.gz"
   linkname="protein.faa"
   ;;
  rna)
   suffix="_rna_from_genomic.fna.gz"
   linkname="rna.fna"
   ;;
  genome)
   suffix="_genomic.fna.gz"
   linkname="genome.fna"
   ;;
  gff)
   suffix="_genomic.gff.gz"
   linkname="genome.gff"
   ;;
  cds)
   suffix="_cds_from_genomic.fna.gz"
   linkname="cds.fna.gz"
   ;;
  stats)
   suffix="_assembly_stats.txt"
   linkname="assembly_stats.txt"
   ;;
  *)
   echo "ERROR-unknown TYPE "$type" specified." >&2
   echo "${docstring}"
   exit 1
   ;;  
esac
#
# handle positional argument
#
shift $(($OPTIND - 1))
nargs=${#@}
if [ $nargs -ne 1 ]; then
  echo "Must specify a GenBank directory. $nargs" >&2
  echo "${docstring}"
  exit 1
else
  genbank_dir="${1}"
fi
set_prefix="${genbank_dir##*/}"
datafilename="${set_prefix}${suffix}"
unzippedname="${datafilename%*.gz}"
URL="${prefix}${genbank_dir}"
fileURL="${URL}/${datafilename}"
#
# find scientific name, stripping off top-level genbank dir
# as kingdom info for metadata
#
for dir in `echo ${genbank_dir}| tr '/' '\n'`; do
  case $dir in
    archaea)
     kingdom="archaea"
     ;;
    bacteria)
     kingdom="bacteria"
     ;;
    fungi)
     kingdom="fungi"
     ;;
    invertebrate)
     kingdom="invertebrate"
     ;;
    other)
     kingdom="other"
     ;;
    plant)
     kingdom="plant"
     ;;
    protozoa)
     kingdom="protozoa"
     ;;
    vertebrate_mammalian)
     kingdom="mammal"
     continue
     ;;
    vertebrate_other)
     kingdom="vertebrate"
     ;;
    *)
     break
     ;;
  esac
done
scientific_name=`echo $dir | tr '_' ' '`
#
# Print verbose messages, if requested.
#
if [ ! -z $verbose ]; then
  echo "Download URL is ${URL}."
  echo "Symlink name is ${linkname}."
  echo "Download kingdom is ${kingdom}."
  echo "Directory name is ${dir}."
  echo "Scientific name is \"${scientific_name}\"."
  if [ ! -z $code ]; then
    echo "Code is ${code}."
  fi
fi

if [ ! -d $dir ]; then
  echo "Creating directory \"${dir}\"."
  mkdir $dir
fi
#
# Handle creation and deletion of existing output
# directory and files.
#
if [ -f ${dir}/$unzippedname ]; then
  echo "Download file \"${unzippedname}\" already exists, skipping."
  exit 0
fi
linkfile="${dir}/${linkname}"
if [ -L $linkfile ]; then
  echo "Removing existing symlink \"${linkfile}\"."
  rm $linkfile
fi
#
# Download the requested file using curl (for Mac/Windows
# compatibility.
#
cd $dir
curl -O ${quiet} ${verbose} "${fileURL}"
if [ $? -ne 0 ]; then
  echo "ERROR-failed to download \"${fileURL}\".
Sometimes this happens because GenBank decides you are
executing a denial-of-service attack.  Check the URL
and try again."
  exit 1
fi
#
# Gunzip the file and symlink it.
#
gunzip "${datafilename}"
ln -s "${unzippedname}" ${linkname}
#
# Create the metadata file.
#
if [ -f metadata.tsv ]; then
  echo "Removing existing metadata file."
  rm metadata.tsv
fi
echo -e "scientific_name\t${scientific_name}" > metadata.tsv
echo -e "directory_URL\t${URL}" >> metadata.tsv
echo -e "kingdom\t${kingdom}" >> metadata.tsv
datestring=`date`
echo -e "download_date\t${datestring}" >> metadata.tsv
if [ ! -z $code ]; then
    echo -e "code\t${code}" >> metadata.tsv
fi
