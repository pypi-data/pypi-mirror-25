#!/usr/bin/env bash
# Wrapper script to make running Panseq easier
# Usage: runPanSeq.sh path/to/panseq/fasta/directory
#
# This makes a temporary work directory for panseq, writes a settings file,
# executes the analysis, and copies it back to the current directory with the
# log.
#
# Default options can be overridden by explicitly editing the settings.txt
# file created in /tmp/panseq_out and re-run if desired, but this Wrapper
# is designed to get you most of the way there in a consistent way.
set -e
set -u
set -o pipefail

curdir=`pwd`

export working_dir=/tmp/panseq_out
export working_results_dir=$working_dir/panseq_out-$(date +%F)

genome_src_dir=$1

if [ ! -d $working_dir/genomes ]; then mkdir -p $working_dir/genomes; fi

cp -r $genome_src_dir $working_dir/genomes

# Find the path to each executible in two parts - one to find the path and
# the other to strip the executible name.
blastpath=$(which blastx)
blastpath=${blastpath%blastx}
mummerpath=$(which mummer)
mummerpath=${mummerpath%mummer}
musclepath=$(which muscle)

echo "queryDirectory  $working_dir/genomes
baseDirectory $working_results_dir
numberOfCores 4
mummerDirectory ${mummerpath}
blastDirectory  ${blastpath}
minimumNovelRegionSize  500
novelRegionFinderMode no_duplicates
muscleExecutable  ${musclepath}
fragmentationSize 50
percentIdentityCutoff 85
coreGenomeThreshold $(ls $working_dir/genomes | wc -w)
runMode pan
storeAlleles  1
allelesToKeep 2
nameOrId  name
overwrite 0" > $working_dir/settings.txt

pushd $working_dir  # To avoid leaving annoying tmp files in Drive
panseq.pl $working_dir/settings.txt
popd

# Do some cleanup of the results dir
rm $working_results_dir/panseq_results.zip
gzip $working_results_dir/*.txt $working_results_dir/*.fasta \
  $working_results_dir/*.phyllip
gunzip $working_results_dir/phylip_name_conversion.txt
cp $working_dir/settings.txt $working_results_dir

# Label Tree with phylip_name_conversion.txt
labelTree $working_dir/snp_consensus_tree_neighborjoining1000bootstrap.newick \
  $working_dir/phylip_name_conversion.txt \
  > $working_dir/snp_consensus_tree_neighborjoining1000bootstrap.labelled.newick

# Copy Results back to running dir
cp -r $working_results_dir $curdir
