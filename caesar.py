#!/usr/bin/python
import sys, getopt

allChars = 'abcdefghijklmnopqrstuvwxyz0123456789'

def printUsage():
	usage = '\nusage: %s [-e|-d] -k <key> -t <text> -i <iterations>' % sys.argv[0]
	usage += '\n\t-e: encode (default)'
	usage += '\n\t-d: decode'
	usage += '\n\t-k: key'
	usage += '\n\t-t: text'
	usage += '\n\t-i: iterations'
	usage += '\nEncode example: %s -e -k "cipher key" -t "text to encode" -i 3' % sys.argv[0]
	usage += '\nDecode example: %s -d -k "cipher key" -t "neunnreigrxe" -i 3' % sys.argv[0]
	print(usage)

def genShiftedChars(key):
	pruned = pruneKey(key)
	return pruned + ''.join([j for i, j in enumerate(allChars) if j not in allChars[:i] and j not in pruned])

def genEncodeLookup(key):
	return dict(zip(allChars, genShiftedChars(key)))
	
def genDecodeLookup(key):
	return dict(zip(genShiftedChars(key), allChars))

def pruneKey(key):
	return ''.join([j for i, j in enumerate(key) if j not in key[:i]]).replace(' ', '')
	
def encode(lookup, raw):
	return ''.join([lookup[j] for i, j in enumerate(raw) if j in allChars])
	
def decode(lookup, encoded):
	return ''.join([lookup[j] for i, j in enumerate(encoded) if j in allChars])
	
def main(argv):
	try:
		opts, args = getopt.getopt(argv[1:], 'hedk:t:i:')
	except getopt.error as msg:
		sys.stdout = sys.stderr
		print(msg)
		printUsage()
		sys.exit(2)
	
	key = ''
	text = ''
	func = encode
	lookupFunc = genEncodeLookup

	for opt, arg in opts:
		if '-h' == opt:
			printUsage()
			sys.exit()
		elif '-k' == opt:
			key = arg
		elif '-t' == opt:
			text = arg
		elif '-d' == opt:
			func = decode
			lookupFunc = genDecodeLookup
		elif '-i' == opt:
			try:
				iterations = int(float(arg))
			except ValueError:
				print('Error: reveived invalid value [%s] for iterations, expects integer value' % arg)
				sys.exit(2)
	
	result = text
	for i in range(0, iterations):
		result = func(lookupFunc(key), result)
	
	if (len(result) > 0):
		print(result)
	else:
		print('Error: yielded zero length result')
	
if __name__ == "__main__":
	main(sys.argv)