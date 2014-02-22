import nltk as nl
import numpy as np
from nltk.corpus import movie_reviews as mr

from sentiwordnet import SentiWordNetCorpusReader, SentiSynset
swn_filename = 'SentiWordNet_3.0.0_20100705.txt'
swn = SentiWordNetCorpusReader(swn_filename)

def getWordPolarityList(fileName):
	reviewFile = open(fileName)
	sampleReview = reviewFile.read()
	sampleWordlist = nl.word_tokenize(sampleReview)
	taggedWordlist = nl.pos_tag(sampleWordlist)

	wordList = []
	for word in taggedWordlist:
		if not (word[1] ==  'IN' or word[1] == 'CC' or word[1] == 'CD' or\
		word[1] == 'DT' or word[1] == 'TO' or word[1] == ',' or word[1] == ';'\
		or word[1] == ':'):
			wordList.append(word)
	'''
	print '\nwordList: '
	print wordList
	'''
	i = 0
	newWordlist = []
	for word in wordList:
		if (word[1] == 'NN' or word[1] == 'JJ' or word[1] == 'JJR' or word[1] == 'JJS'\
			or word[1] == 'VB' or word[1] == 'VBG' or word[1] == 'VBD' or word[1] == 'VBN'\
			or word[1] == 'VBP' or word[1] == 'VBZ' or word[1] == 'RB' or word[1] == 'RBR'\
			or word[1] == 'RBS' or word[1] == 'RP'):
			if swn.senti_synsets(word[0]):
				wordValue = swn.senti_synsets(word[0])[0]
				if wordValue.pos_score > wordValue.neg_score:
					value = wordValue.pos_score
				else:
					value = 0 - wordValue.neg_score
				if value != 0:
					newWordlist.append([i,word[0], value])
				i += 1
	return newWordlist


def findMedian(fileName):
	wordList = getWordPolarityList(fileName)
	ppList = []
	nnList = []
	pnList = []
	ppDistanceList = []
	nnDistanceList = []
	pnDistanceList = []
	length = len(wordList) - 1
	for index1 in range(0, length):
		for index2 in range(index1+1, length):
			wordDistance = wordList[index2][0] - wordList[index1][0]
			tempList = [wordList[index1][1], wordList[index2][1], wordDistance]
			if (wordList[index1][2] > 0) and (wordList[index2][2] > 0):
				ppList.append(tempList)
				ppDistanceList.append(wordDistance)
			elif (wordList[index1][2] < 0) and (wordList[index2][2] < 0):
				nnList.append(tempList)
				nnDistanceList.append(wordDistance)
			else:
				pnList.append(tempList)
				pnDistanceList.append(wordDistance)
	'''
	print 'ppList:'
	print ppList
	'''
	'''
	ppDistanceList.sort()
	nnDistanceList.sort()
	pnDistanceList.sort()
	print '\nppDistanceList: '
	print ppDistanceList
	print '\nnnDistanceList: '
	print nnDistanceList
	print '\npnDistanceList: '
	print pnDistanceList
	'''
	return [np.median(ppDistanceList), np.median(nnDistanceList), np.median(pnDistanceList)]


def findTrainingMedian():
	posMedianList = []
	negMedianList = []
	posFileIdList = mr.fileids(categories = 'pos')[0:50]
	negFileIdList = mr.fileids(categories = 'neg')[0:50]
	i = 1
	print '\nTraining with Positive Reviews....'
	for fid in posFileIdList:
		print 'Review ' + `i`
		temporaryMedian = findMedian(mr.abspath(fid))
		posMedianList.append(temporaryMedian)
		i += 1
	i = 1
	print '\nTraining with Negative Reviews....'
	for fid in negFileIdList:
		print 'Review ' + `i`
		temporaryMedian = findMedian(mr.abspath(fid))
		negMedianList.append(temporaryMedian)
		i += 1
	trainingMedianList = [posMedianList, negMedianList]
	return trainingMedianList

'''
filename = 'samplereview.txt'
newWordlist = getWordPolarityList(filename)
print '\nnewWordlist: '
print newWordlist

medianList = findMedian(newWordlist)
print 'Median of ppList: ' + `medianList[0]`
print 'Median of nnList: ' + `medianList[1]`
print 'Median of pnList: ' + `medianList[2]`
'''

#Find the Training Review's Median (Both Positive and Negative)
trainingMedianList = findTrainingMedian()

print '\nMedian List of training reviews is: '
print trainingMedianList

posMedianList = trainingMedianList[0]
negMedianList = trainingMedianList[1]

posMedianSum = [0, 0, 0]
negMedianSum = [0, 0, 0]
listLength = len(posMedianList)
for item in posMedianList:
	posMedianSum[0] += item[0]
	posMedianSum[1] += item[1]
	posMedianSum[2] += item[2]
for item in negMedianList:
	negMedianSum[0] += item[0]
	negMedianSum[1] += item[1]
	negMedianSum[2] += item[2]
posMedian = [posMedianSum[0]/listLength, posMedianSum[1]/listLength, posMedianSum[2]/listLength]
negMedian = [negMedianSum[0]/listLength, negMedianSum[1]/listLength, negMedianSum[2]/listLength]

print 'Positive Median List: ' + `posMedian`
print 'Negative Median List: ' + `negMedian`



