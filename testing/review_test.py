#!/usr/bin/python
# Filename: review_test.py

import numpy
import itertools
import datetime
import math
import json
from sklearn.svm import LinearSVC,SVC
import proximity_tagger


from nltk.corpus import movie_reviews

def median_result(file_to_test,isphrase):

        median_testset=[]
        f = open('train_result/proximity_median_train_result_'+str(isphrase),'r')
        median_testset=json.load(f)
        f.close()
        median_test = proximity_tagger.medianlist(file_to_test,isphrase)
        
        med_pos_val = median_testset[0][0]-median_test[0]                                    
        med_neg_val = median_testset[1][1]-median_test[1]

	if(med_pos_val<med_neg_val):
            return 1
        return -1

def review_test(isphrase):

	bin_testset=[]
	f = open('train_result/proximity_bin_train_result_'+str(isphrase),'r')
	bin_testset=json.load(f)
	f.close()
	
	#clf=SVC()
	clf=LinearSVC()
	clf.fit(bin_testset[0],bin_testset[1])

	pattern_testset=[]
	f = open('train_result/proximity_pattern_train_result_'+str(isphrase),'r')
	pattern_testset=json.load(f)
	f.close()

	#clf2=SVC()
	clf2=LinearSVC()
	clf2.fit(pattern_testset[0],pattern_testset[1])

	count=0
	cnt_var=0
	pat_val=-1
	bin_val=-1
	med_val = median_result('samplereview.txt',isphrase)
	
	temp_class1= clf.predict(proximity_tagger.bin_list('samplereview.txt',isphrase))
	if temp_class1 == [1]:
		bin_val=1
    	
	temp_class2= clf2.predict(proximity_tagger.pattern_list('samplereview.txt',isphrase))
	numsum=sum(temp_class2)
	if numsum > (len(temp_class2)/2):
		pat_val=1


	isreviewpositive = 0
	if (med_val+bin_val+pat_val)>0:
		isreviewpositive = 1

	
	return isreviewpositive


