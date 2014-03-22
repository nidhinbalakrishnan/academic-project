#!/usr/bin/python
# Filename: review_test.py

import nltk
import numpy
import itertools
import datetime
import math
import json
#from sklearn.svm import LinearSVC,SVC
import proximity_tagger
import review_train

from nltk.corpus import movie_reviews

def median_result(file_to_test,isphrase):
        alpha=0.4
        beta =0.4
        gamma=0.2

        median_testset=[]
        f = open('train_result/proximity_median_train_result_'+str(isphrase),'r')
        median_testset=json.load(f)
	#print '\nMedian Test Set : ', median_testset
        f.close()
        median_test = proximity_tagger.medianlist(file_to_test,isphrase)
	#print '\nMedian Test : ', median_test

        med_pos_val = median_testset[0][0]-median_test[0]                                    
        med_neg_val = median_testset[1][1]-median_test[1]
        #print 'Values : ', med_pos_val, med_neg_val
        
	if(med_pos_val<med_neg_val):
            return 1

        return -1

def review_test(isphrase):
	#return 1 

	bin_testset=[]
	f = open('train_result/proximity_bin_train_result_'+str(isphrase),'r')
	bin_testset=json.load(f)
	f.close()
	
	#clf=LinearSVC()
	#clf=SVC()
	#clf.fit(bin_testset[0],bin_testset[1])

	pattern_testset=[]
	f = open('train_result/proximity_pattern_train_result_'+str(isphrase),'r')
	pattern_testset=json.load(f)
	f.close()

	#clf2=LinearSVC()
	#clf2=SVC()
	#clf2.fit(pattern_testset[0],pattern_testset[1])

	count=0
	cnt_var=0
 
	pat_val=-1
	bin_val=-1

	med_val = median_result('samplereview.txt',isphrase)
	
	return 1

	'''
	temp_class1= clf.predict(proximity_tagger.bin_list('samplereview.txt',isphrase))
	if temp_class1 == [1]:
		bin_val=1
    	
	temp_class2= clf2.predict(proximity_tagger.pattern_list('samplereview.txt',isphrase))
	numsum=sum(temp_class2)
	if numsum > (len(temp_class2)/2):
		pat_val=1
	'''
	#med_val=0
	pat_val=0
	bin_val=0

	isreviewpositive = 0
	if (med_val+bin_val+pat_val)>0:
		isreviewpositive = 1

	#print 'Result is :', isreviewpositive
	return isreviewpositive


