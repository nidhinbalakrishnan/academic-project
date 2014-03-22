#!/usr/bin/env python
# Filename: proximity_analysis.py


import datetime
import math
import proximity_tagger
import review_train
import review_test
import os
import json


from sentiwordnet import SentiWordNetCorpusReader, SentiSynset
swn_filename ='SentiWordNet_3.0.0_20130122.txt'
swn = SentiWordNetCorpusReader(swn_filename)

def finish_popup(start_time,end_time):

    import win32api
    import winsound
    
    winsound.Beep(1000,2000)
    finish_msg='Successfully Finished\n\nStart Time   : '+str(start_time)+'\nFinish Time : '+str(end_time)
    win32api.MessageBox(0, finish_msg, 'Result', 0x00001000)


def phrase_analysis_call(llimit,ulimit):

    from nltk.corpus import movie_reviews
    
    testmed = []
    testmed.append(proximity_tagger.phrase_analysis('samplereview.txt'))

    lpcount=0
    testmed=[]
    print '\nNo of -ve reviews trained : '
    for fid in movie_reviews.fileids(categories=['neg'])[llimit:ulimit]:
        if file_exist:
            phrase_medlist[1].append(proximity_tagger.phrase_analysis(movie_reviews.abspath(fid)))
        else:
            testmed.append(proximity_tagger.phrase_analysis(movie_reviews.abspath(fid)))
        lpcount=lpcount+1
        print 'Training -ve review ',lpcount,'.'*10,(float(lpcount)*100/float(totalcount)),'%'

    if not file_exist:
        phrase_medlist.append(testmed)

    fid = open('phrase_analysis_part_file','w')
    json.dump(phrase_medlist,fid)
    fid.close()





start_time = datetime.datetime.now()

trainpath='train_file'
testpath='test_file'




def normaltrain():
    review_train.median_approach(200,700,0,trainpath)
    review_train.bins_svm_approach(200,700,0,trainpath)
    review_train.patterns_approach(200,700,0,trainpath)

def normaltest():
    review_test.review_test(0,100,0,testpath)


def phrase_call():
    llimit=0
    ulimit=100
    phrase_analysis_call(llimit,ulimit)

def reviewtrain():
    llimit=200
    ulimit=700
    review_train.median_approach(llimit,ulimit,1,trainpath)
    review_train.bins_svm_approach(llimit,ulimit,1,trainpath)
    review_train.patterns_approach(llimit,ulimit,1,trainpath)

def reviewtest():
    llimit=0
    ulimit=100
    review_test.review_test(llimit,ulimit,1,testpath)




#Function Calls
    
phrase_call()
#reviewtrain()
#reviewtest()




end_time = datetime.datetime.now()
finish_popup(start_time,end_time)




















