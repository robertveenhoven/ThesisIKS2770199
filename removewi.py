def main():
	tweets = open("researchdays/03052017research.txt", "r")
	writefile1= open("researchdays/03052017.txt", 'a')
	for line in tweets:
		found='0'
		words = line.split(" ")
		for item in words:
			#print(item)
			if item in ['Intel']:
				found='1'
		if found == '0':				
			writefile1.write(" ".join(words))	
	
main()	
