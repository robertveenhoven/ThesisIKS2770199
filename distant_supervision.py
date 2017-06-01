

def main():
	tweets = open("30042017.txt", "r")
	writefile1 = open("positive30.txt", 'a')
	writefile2 = open("negative30.txt", 'a')
	poslist= ['happy',':)',':D','best','good','nice','great','love']
	neglist= ['sad','worse','worst','angry',':(','bad','wrong','dislike','hate', 'mad']
	for line in tweets:
		poscounter,negcounter=0,0
		words = line.split(" ")
		if words[0] == '"RT':
			continue
		itemcounter=0	
		for item in words:
			itemcounter+=1
			if item in poslist and words[itemcounter-1] != 'not':
				poscounter+=1
			if item in neglist and words[itemcounter-1] != 'not':
				negcounter+=1					
		if poscounter !=0 and negcounter == 0:
			writefile1.write(" ".join(words))
		if poscounter == 0 and negcounter != 0:	
			writefile2.write(" ".join(words))
	writefile1.close()
	writefile2.close()
main()		

