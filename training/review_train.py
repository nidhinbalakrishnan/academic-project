#!/usr/bin/env python
# Filename: review_train.py

import nltk
import numpy
import itertools
from nltk.corpus import movie_reviews
import proximity_tagger
import json

def median_approach(llimit,ulimit,isphrase,pathname):

    posmedlist=[]
    negmedlist=[]
    medians=[]

    lpcount=0
    totalcount=ulimit-llimit
    cnt_var=0
    print '\nNo of +ve reviews trained : '
    for fid in movie_reviews.fileids(categories=['pos'])[llimit:ulimit]:
        testmed=proximity_tagger.medianlist(movie_reviews.abspath(fid),isphrase,cnt_var,0,pathname)
        posmedlist.append(testmed)
        lpcount=lpcount+1
	cnt_var+=1
        print 'Training +ve review ',lpcount,'.'*10,(float(lpcount)*100/float(totalcount)),'%'

    lpcount=0
    cnt_var=0
    print '\nNo of -ve reviews trained : '
    for fid in movie_reviews.fileids(categories=['neg'])[llimit:ulimit]:
        testmed=proximity_tagger.medianlist(movie_reviews.abspath(fid),isphrase,cnt_var,1,pathname)
        negmedlist.append(testmed)
        lpcount=lpcount+1
	cnt_var+=1
        print 'Training -ve review ',lpcount,'.'*10,(float(lpcount)*100/float(totalcount)),'%'

    medians.append([numpy.median(x) for x in itertools.izip(*posmedlist)])
    medians.append([numpy.median(x) for x in itertools.izip(*negmedlist)])

    f = open('train_result\proximity_median_train_result_'+str(isphrase),'w')
    json.dump(medians,f)
    f.close()



def bins_svm_approach(llimit,ulimit,isphrase,pathname):

    posbinlist=[]
    negbinlist=[]
    trainingdata=[]
    trainingclass=[]
    bin_train_set=[]
    totalcount=ulimit-llimit

    lpcount=0
    cnt_var=0
    print '\nNo of +ve reviews scanned for training : '
    for fid in movie_reviews.fileids(categories=['pos'])[llimit:ulimit]:
        testbin=proximity_tagger.bin_list(movie_reviews.abspath(fid),isphrase,cnt_var,0,pathname)
        posbinlist.append(testbin)
        lpcount+=1
	cnt_var+=1
        print 'Scanning +ve review ',lpcount,'.'*10,(float(lpcount)*100/float(totalcount)),'%'
        

    lpcount=0
    cnt_var=0
    print '\nNo of -ve reviews scanned for training : '
    for fid in movie_reviews.fileids(categories=['neg'])[llimit:ulimit]:
        testbin=proximity_tagger.bin_list(movie_reviews.abspath(fid),isphrase,cnt_var,1,pathname)
        negbinlist.append(testbin)
        lpcount+=1
	cnt_var+=1
        print 'Scanning -ve review ',lpcount,'.'*10,(float(lpcount)*100/float(totalcount)),'%'


    lpcount=0
    totalcount=len(posbinlist)
    print '\nNo of +ve reviews trained : '
    trainingdata.extend(posbinlist)
    for i in range(totalcount):
        trainingclass.append(1)
        lpcount+=1
        print 'Training +ve review ',lpcount,'.'*10,(float(lpcount)*100/float(totalcount)),'%'

    lpcount=0
    totalcount=len(negbinlist)
    print '\nNo of -ve reviews trained : '
    trainingdata.extend(negbinlist)
    for i in range(totalcount):
        trainingclass.append(0)
        lpcount+=1
        print 'Training -ve review ',lpcount,'.'*10,(float(lpcount)*100/float(totalcount)),'%'

    bin_train_set.append(trainingdata)
    bin_train_set.append(trainingclass)

    f = open('train_result\proximity_bin_train_result_'+str(isphrase),'w')
    json.dump(bin_train_set,f)
    f.close()


def patterns_approach(llimit,ulimit,isphrase,pathname):

    pos_pattern_list=[]
    neg_pattern_list=[]
    trainingdata=[]
    trainingclass=[]
    pattern_train_set=[]
    totalcount=ulimit-llimit

    lpcount=0
    cnt_var=0
    print '\nNo of +ve reviews scanned for training : '
    for fid in movie_reviews.fileids(categories=['pos'])[llimit:ulimit]:
        test_pattern=proximity_tagger.pattern_list(movie_reviews.abspath(fid),isphrase,cnt_var,0,pathname)
        pos_pattern_list.extend(test_pattern)
        lpcount=lpcount+1
	cnt_var+=1
        print 'Scanning +ve review ',lpcount,'.'*10,(float(lpcount)*100/float(totalcount)),'%'
        

    lpcount=0
    cnt_var=0
    print '\nNo of -ve reviews scanned for training : '
    for fid in movie_reviews.fileids(categories=['neg'])[llimit:ulimit]:
        test_pattern=proximity_tagger.pattern_list(movie_reviews.abspath(fid),isphrase,cnt_var,1,pathname)
        neg_pattern_list.extend(test_pattern)
        lpcount=lpcount+1
	cnt_var+=1
        print 'Scanning -ve review ',lpcount,'.'*10,(float(lpcount)*100/float(totalcount)),'%'


    lpcount=0
    totalcount=len(pos_pattern_list)
    print '\nNo of +ve reviews trained : '
    trainingdata.extend(pos_pattern_list)
    for i in range(totalcount):
        trainingclass.append(1)
        lpcount+=1
        print 'Training +ve patterns ',lpcount,'.'*10,(float(lpcount)*100/float(totalcount)),'%'

    lpcount=0
    totalcount=len(neg_pattern_list)
    print '\nNo of +ve reviews trained : '
    trainingdata.extend(neg_pattern_list)
    for i in range(totalcount):
        trainingclass.append(0)
        lpcount+=1
        print 'Training -ve patterns ',lpcount,'.'*10,(float(lpcount)*100/float(totalcount)),'%'

    pattern_train_set.append(trainingdata)
    pattern_train_set.append(trainingclass)

    f = open('train_result\proximity_pattern_train_result_'+str(isphrase),'w')
    json.dump(pattern_train_set,f)
    f.close()

