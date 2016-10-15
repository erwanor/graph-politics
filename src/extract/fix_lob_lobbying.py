# Dataset: dataset/raw/Congress/Lobby/lob_lobbying.txt
# Issue: The column #16 has a broken delimiter
# Example:
# - '|B035CC2E-6E80-4A58-8E46-A1FBF084C2E4|,|CARMEN GROUP INC|,|Carmen Group|,|y|,|POLS        ON, ERIC|,|Polson, Eric|,|Polson, Eric|,0.0,|Y4000|,|     |,|n|,| |,|n|,| |,|2005|        ,|mtn|,|MID-YEAR TERMINATION (NO ACTIVITY)|,||'
# column #16: |,0.0,|
# Should be: |,|0.0|,|

PATH = '/Users/erwan/oss/graph-politics/src/dataset_fix/../../datasets/raw/Congress/Lobby/lob_lobbying.txt'
OUTPUT = '/Users/erwan/oss/graph-politics/src/dataset_fix/../../datasets/raw/Congress/Lobby/fixed_lob_lobbying.txt'

to_write = []

with open(PATH, 'r') as f:
	for line in f:
		parsed = line.split('|')
		if len(parsed) < 15:
			print parsed
			continue
		target = parsed[14]
		split_target = target.split(',')
		if len(split_target) <= 1:
			print parsed
			continue
		split_target[1] = '|' + split_target[1] + '|'
		target_fixed = ','.join(split_target)
		parsed[14] = target_fixed
		line_to_write = '|'.join(parsed)
		to_write.append(line_to_write)

with open(OUTPUT, 'w+') as output:
	for line in to_write:
		output.write(line + '\n')

