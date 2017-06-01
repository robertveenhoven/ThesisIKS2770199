#!/usr/bin/python3

import sys
import string
import nltk.classify
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.tokenize import TweetTokenizer
from featx import bag_of_words, high_information_words
from classification import precision_recall
from random import shuffle
from os import listdir  # to read files
from os.path import isfile, join  # to read files



# return all the filenames in a folder
def get_filenames_in_folder(folder):
	return [f for f in listdir(folder) if isfile(join(folder, f))]

def read_files(filemap,categories, stopwordsPunctuationList):
	feats = list()
	print("\n##### Reading files...")
	for category in categories:
		files = get_filenames_in_folder(filemap+ '/' + category)
		num_files = 0
		for tweetsfile in files:
			data = open(filemap+ '/' + category + '/' + tweetsfile, 'r', encoding='UTF-8').read()
			for line in data.split('\n'):
				strippedLine=line.strip('"')
				dataLower = strippedLine.lower()
				tokens = TweetTokenizer(strip_handles=True, reduce_len=True).tokenize(dataLower)
				filteredTokens = [w for w in tokens if not w in stopwordsPunctuationList and w[0] not in ['@','/'] and len(w)>=3 and w[:4] not in ['http','t.co'] 
				and w not in ['Apple','Iphone','Ipad','Ipod','Iphone7','Iphone6', 'Microsoft','Windows','iphone','ipad','ipod','iphone7','iphone6', 'microsoft',
				'Skype','skype','Windows7','Windows8','Windows10','windows7','windows8','windows10','Xbox','xbox','XBOX','Netflix', 'Amazon','netflix', 'amazon']]
				bag = bag_of_words(filteredTokens)
				feats.append((bag, category))
				num_files += 1

			print("  Category %s, %i Documents read" % (category, num_files))

	return feats

#return list of all words to use in get_word_features
def get_words_in_tweets(feats):
	allwords=[]
	for feat in feats:
		category = feat[1]
		bag = feat[0]
		for w in bag.keys():
			allwords.append(w)
	return allwords

#returns a list of words ordered by frequency(FreqDist)
def get_word_features(wordlist):
	hallo = nltk.FreqDist(wordlist)
	word_features = hallo.keys()
	return word_features			

# Calculates the f measure for each category using as input the precisions and recalls
def calculate_f(categories, precisions, recalls):
	f_measures = {}
	for category in categories:
		if precisions[category] is None:
			continue
		else:
			f_measures[category] =  (2 * (precisions[category] * recalls[category])) / (precisions[category] + recalls[category])
	return f_measures


# prints accuracy, precision and recall
def evaluation(classifier, test_feats, categories):
	print("\n##### Evaluation...")
	accuracy = nltk.classify.accuracy(classifier, test_feats)
	print("  Accuracy: %f" % accuracy)
	precisions, recalls = precision_recall(classifier, test_feats)
	f_measures = calculate_f(categories, precisions, recalls)

	print(" |-----------|-----------|-----------|-----------|")
	print(" |%-11s|%-11s|%-11s|%-11s|" % ("category","precision","recall","F-measure"))
	print(" |-----------|-----------|-----------|-----------|")
	for category in categories:
		if precisions[category] is None:
			print(" |%-11s|%-11s|%-11s|%-11s|" % (category, "NA", "NA", "NA"))
		else:
			print(" |%-11s|%-11f|%-11f|%-11s|" % (category, precisions[category], recalls[category], f_measures[category]))
	print(" |-----------|-----------|-----------|-----------|")
	return accuracy
		

# show top 10 most informative features
def analysis(classifier):
	print("\n##### Analysis...")
	classifier.show_most_informative_features(14)


# obtain the high information words
def high_information(feats, categories):
	print("\n##### Obtaining high information words...")
	labelled_words = [(category, []) for category in categories]

	# 1. convert the formatting of our features to that required by high_information_words
	from collections import defaultdict
	words = defaultdict(list)
	all_words = list()
	for category in categories:
		words[category] = list()

	for feat in feats:
		category = feat[1]
		bag = feat[0]
		for w in bag.keys():
			words[category].append(w)
			all_words.append(w)

	labelled_words = [(category, words[category]) for category in categories]
	# print labelled_words

	# 2. calculate high information words
	high_info_words = set(high_information_words(labelled_words, min_score=4.4))

	print("  Number of words in the data: %i" % len(all_words))
	print("  Number of distinct words in the data: %i" % len(set(all_words)))
	print("  Number of distinct 'high-information' words in the data: %i" % len(high_info_words))

	return high_info_words


#filter all high_information_words from all the tweets
def filter_high_information_words(feats, high_information_words):
	newfeats = []
	dictionary = {}
	for tuple in feats:
		for item in tuple[0].keys():
			if item in high_information_words:
				dictionary[item] = True
		newfeats.append((dictionary, tuple[1]))
		dictionary = {}
	return newfeats
	
def main():
	stopwordsPunctuationList = stopwords.words('english')
	[stopwordsPunctuationList.append(i) for i in string.punctuation]
	categories = ["positive","negative"]
	#filemap= 'trainingset'
	filemap= 'trainingANDdev'
	feats = read_files(filemap, categories, stopwordsPunctuationList)
	high_info_words = high_information(feats, categories)
	newfeats = filter_high_information_words(feats, high_info_words)
	def extract_features(document):
		document_words = set(document)
		features = {}
		for word in word_features:
			if word in document_words:
				features['contains(%s)' % word] = True
		return features
	word_features = get_word_features(get_words_in_tweets(feats))
	training_set = nltk.classify.apply_features(extract_features, newfeats)
	#training with NaiveBayes	
	classifier = nltk.NaiveBayesClassifier.train(training_set)
	#filemap = 'developmentset'
	filemap = 'testset'
	fscorefeats = read_files(filemap, categories, stopwordsPunctuationList)
	test_set = nltk.classify.apply_features(extract_features, fscorefeats)
	#Evaluation
	accscore = evaluation(classifier, test_set, categories)
	#print top 10 most informative features
	analysis(classifier)
	
	#2 lists the program will search for in the tweets
	AppleTriggers = ['Apple','Iphone','Ipad','Ipod','Iphone7','Iphone6','iphone','ipad','ipod','iphone7','iphone6']
	MicrosoftTriggers = ['Microsoft','Windows','Skype','skype','Windows7','Windows8','Windows10','Xbox','xbox','microsoft','windows7','windows8','windows10','XBOX']
	NetflixTriggers= ['Netflix','netflix']
	AmazonTriggers= ['Amazon','amazon']

	twitterData = ["researchdays/01052017research.txt", "researchdays/02052017research.txt", "researchdays/03052017research.txt", "researchdays/04052017research.txt", "researchdays/05052017research.txt"
	, "researchdays/06052017research.txt" , "researchdays/07052017research.txt" , "researchdays/08052017research.txt", "researchdays/09052017research.txt" , "researchdays/10052017research.txt"
	 , "researchdays/11052017research.txt", "researchdays/12052017research.txt"]
	for testfile in twitterData:
		counter=0
		positiveApple, negativeApple = 0,0
		positiveMicrosoft, negativeMicrosoft = 0,0
		positiveNetflix, negativeNetflix = 0,0
		positiveAmazon, negativeAmazon = 0,0
		with open(testfile, "r") as twitterFile:
			for line in twitterFile:
				strippedline=line.strip('"')
				for item in AppleTriggers:
					if item in strippedline.split():
						result = classifier.prob_classify(extract_features(strippedline.split()))
						if result.max() == "positive" and result.prob("positive")>= .7:
							positiveApple += 1
						if result.max() == "negative" and result.prob("negative")>= .7:
							negativeApple += 1
						counter += 1
						break	
					else:
						continue
				for item in MicrosoftTriggers:
					if item in strippedline.split():
						result = classifier.prob_classify(extract_features(strippedline.split()))
						if result.max() == "positive" and result.prob("positive")>= .7:
							positiveMicrosoft += 1
						if result.max() == "negative" and result.prob("negative")>= .7:
							negativeMicrosoft += 1
						counter += 1
						break
					else:
						continue
				for item in NetflixTriggers:
					if item in strippedline.split():
						result = classifier.prob_classify(extract_features(strippedline.split()))
						if result.max() == "positive" and result.prob("positive")>= .7:
							positiveNetflix += 1
						if result.max() == "negative" and result.prob("negative")>= .7:
							negativeNetflix += 1
						counter += 1
						break
					else:
						continue
				for item in AmazonTriggers:
					if item in strippedline.split():
						result = classifier.prob_classify(extract_features(strippedline.split()))
						if result.max() == "positive" and result.prob("positive")>= .7:
							positiveAmazon += 1
						if result.max() == "negative" and result.prob("negative")>= .7:
							negativeAmazon += 1
						counter += 1
						break
					else:
						continue																		
		
		totalApple=positiveApple+negativeApple
		totalMicrosoft=positiveMicrosoft+negativeMicrosoft
		totalAmazon=positiveAmazon+negativeAmazon
		totalNetflix=positiveNetflix+negativeNetflix				
		print("Datafile: {} TotalApple: {} PApple: {} NApple: {} TotalMicrosoft: {} PMicrosoft: {} NMicrosoft: {} TotalNetflix: {} PNetflix: {} NNetflix: {} TotalAmazon: {} PAmazon: {} NAmazon: {} ".format
		(testfile, totalApple, positiveApple, negativeApple, totalMicrosoft, positiveMicrosoft, negativeMicrosoft, totalNetflix, positiveNetflix, negativeNetflix, totalAmazon, positiveAmazon, negativeAmazon))	

main()
