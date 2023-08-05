import sys
import pymzml


filename = sys.argv[1]

rt_start = sys.argv[2]

rt_end   = sys.argv[3]


Reader = pymzml.run.Reader(filename)

spec_count = Reader.get_spectrum_count()
target = spec_count / 2

start = 0
while start is not rt_start:
	spec = Reader[target]
	if spec['scan start time'] > rt_start:
		target = target + (spec_count - target) / 2
	else:
		target = 


