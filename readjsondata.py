import json

def main():

	tweets_data = []
	tweets_file = open("twitter_data_20052017.txt", "r")
	outputfile= open("20052017.txt", "a")
	for line in tweets_file:
		try:
			tweet = json.loads(line)
			text_tweets = json.dumps(tweet['text'])
			for word in text_tweets.split():
				if word in ['Apple','Iphone','Ipad','Ipod','Iphone7','Iphone6', 'Microsoft','Windows','iphone','ipad','ipod','iphone7','iphone6', 'microsoft',
				'Skype','skype','Windows7','Windows8','Windows10','windows7','windows8','windows10','Xbox','xbox','XBOX','Netflix', 'Amazon','netflix', 'amazon']:
					outputfile.write(text_tweets+'\n')
					continue
		except:
			continue	
	outputfile.close()
main()			
