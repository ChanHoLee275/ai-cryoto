from datetime import datetime
import sys
import os

if __name__ == "__main__":
	# check command line is correct
	if len(sys.argv) > 4:
		raise "too many arguments"
	inputFileName = sys.argv[1]
	level = int(sys.argv[2])
	outputFilename = sys.argv[3]
	# check inputFileName is csv file
	particle = inputFileName.split(".csv")
	if particle[-1] != '' or len(particle) == 0:
		raise "file is not csv"
	# check file is exist in current folder
	if not os.path.exists(inputFileName):
		raise "file is not exist"
	# check the number of csv file line
	count = 0
	hashTable = {}
	fs = open(outputFilename, 'a')
	for row in open(inputFileName):
		[price, quantity, order, timestamp] = row.split(',')
		if price == 'price':
			headers = ','.join([price, quantity, order, timestamp])
			fs.write(headers)
			continue
		timestamp = timestamp.split("\n")[0]
		price = int(price)
		if timestamp in hashTable.keys():
			if order == '0':
				hashTable[timestamp]['0'].append([price, quantity, order, timestamp])
			else:
				hashTable[timestamp]['1'].append([price, quantity, order, timestamp])
		else:
			if order == '0':
				hashTable[timestamp] = {'0': [[price, quantity, order, timestamp]], '1': []}
			else:
				hashTable[timestamp] = {'1': [[price, quantity, order, timestamp]], '0': []}
	for key in sorted(list(map(lambda x: datetime.fromisoformat(x), hashTable.keys()))):
		bids = reversed(sorted(hashTable[str(key)]['0'], key=lambda x: x[0])[0:level])
		asks = reversed(sorted(hashTable[str(key)]['1'], key=lambda x: x[0])[-level:])
		total = list(bids) + list(asks)
		for i in total:
			items = list(map(str, i))
			line = ','.join(items) + '\n'
			fs.write(line)
	fs.close()