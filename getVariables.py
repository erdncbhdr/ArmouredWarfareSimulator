import sys
import os

print "Getting variables for " + str( sys.argv[1] )


try:
	afile = open(sys.argv[1])
except Exception:
	print "Could not find file. Please give a valid file"

q = afile.read().split("\n")

for line in q:
	if "=" in line:
		b = line.split("=")
		if "(" not in b[0] and "if" not in b[0] and "for" not in b[0] and "while" not in b[0] and "+" not in b[0] and "-" not in b[0]:
			if "self" in b[0]:
				c = b[0].split(".")[1]
				print c.strip()
