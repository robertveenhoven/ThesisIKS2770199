import random

def main():
	random.seed(10)
	f = open("PositiveTraining.txt", 'r')
	s = open("PositiveTraining8363.txt", 'a')
	lines = random.sample(f.readlines(),8363)
	for item in lines:
		s.write(item)
	s.close()
	
	
main()
