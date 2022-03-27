#!/bin/bash

benchmarks=(
# "add_121_mesh_121_blocksize_3_quick"
# "add_81_mesh_81_blocksize_3_quick"
# "qft_40_mesh_49_blocksize_3_quick"
"qft_90_mesh_100_blocksize_3_quick"
"tfim_100_mesh_100_blocksize_3_quick"
"add_71_mesh_81_blocksize_3_quick"
# "qft_100_mesh_100_blocksize_3_quick"
# "qft_50_mesh_64_blocksize_3_quick"
# "shor_42_mesh_49_blocksize_3_quick"
# "tfim_40_mesh_49_blocksize_3_quick"
)

for benchmark in ${benchmarks[@]}
do
	### Check for the number of files
	num_files=$(ls unitaries/$benchmark | wc -l) 
	### Minus to because of structure.pickle and 0 indexing
	max_block=$(($num_files))
	echo $benchmark
	echo $max_block
	sbatch --array=0-$max_block separate_qsearch.kernel $benchmark
done
