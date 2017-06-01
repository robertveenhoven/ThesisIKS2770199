def main():

	with open("19052017.txt", "r") as twitterData:
		counter = 0
		for line in twitterData:
			if counter >= 150:
				break
			with open("test19positive.txt", "a") as writefile1:
				with open("test19negative.txt", "a") as writefile2:
					print(line)
					classify = str(input())
					if classify == "p":
						writefile1.write(line)
						counter+=1
						print(counter)
						continue
					if classify == "n":
						writefile2.write(line)
						counter+=1
						print(counter)
						continue	
					else:
						continue

main()
