import sys
import os

DAY_SECONDS = 86400

if __name__ == "__main__":
	# check command line is correct
	if len(sys.argv) > 2:
		raise "too many arguments"
	fileName = sys.argv[1]
	# check fileName is csv file
	particle = fileName.split(".csv")
	if particle[-1] != '' or len(particle) == 0:
		raise "file is not csv"
	# check file is exist in current folder
	if not os.path.exists(fileName):
		raise "file is not exist"
	# check the number of csv file line
	count = 0
	for row in open(fileName):
		count += 1
	print("Expected Number of Lines", str(DAY_SECONDS*30))
	print("Number of Lines", fileName, str(count - 1)) # remove header line

	
