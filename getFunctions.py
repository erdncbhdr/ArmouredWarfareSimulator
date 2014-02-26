import sys
import importlib

filename = sys.argv[1]

print "Functions in " + str(filename)

a = open(filename).read().split("\n")

for line in a:
	if "def" in line and "_" not in line:
		print line[4:]
		q = a.index(line)
		v = a[q + 1]
		if '"""' in v:
			print v

