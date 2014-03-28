#!/usr/bin/env python
# Filename: proximity_tagger.py

import os
import re
import nltk
import json
import pickle
import numpy
from sets import Set
from nltk.tree import *
from nltk.corpus import stopwords



from sentiwordnet import SentiWordNetCorpusReader, SentiSynset
swn_filename ='SentiWordNet_3.0.0_20130122.txt'
swn = SentiWordNetCorpusReader(swn_filename)

positive=Set([])
negative=Set([])


def taglist(filename):
    fo = open(filename)
    str = fo.read();
    stop=stopwords.words('english')
    tokens=[]
    token = nltk.word_tokenize(str)
    for s in token:
        if s not in stop:
            tokens.append(s)
    tagged = nltk.pos_tag(tokens) 
    wordlist=[]
    for tag in tagged:           
        if not (tag[1]=='IN' or tag[1]=='CC' or tag[1]=='CD'\
        	or tag[1]=='DT' or tag[1]=='TO' or tag[1]==','\
                or tag[1]==';' or tag[1]==':'):
                wordlist.append(tag)


    i=1
    newlist=[]
    temp=[]
    val=0.0
    for word in wordlist:
        temp = word[0].split('_')
        if temp[0]=='phrase' and len(temp)>1:
            newlist.append((i,int(temp[1])))
        elif (word[1]=='JJ' or word[1]=='JJR' or word[1]=='JJS' or word[1]=='R' or word[1]=='RBR' or word[1]=='RBS' \
            or word[1]=='VB' or word[1]=='VBD' or word[1]=='VBG' or word[1]=='VBN' or word[1]=='VBP' or word[1]=='VBZ'):
            if (word[0],0) in positive or (word[0],0) in negative or (word[0],1) in positive or (word[0],1) in negative:
                pol=1;
                if (word[0],0) in negative or (word[0],1) in negative:
                    pol=-1     
                newlist.append((i,pol))
            else:
               if swn.senti_synsets(word[0]):
                    dist=swn.senti_synsets(word[0])[0]
                    if dist.pos_score>dist.neg_score:
                        val=dist.pos_score
                        positive.add((word[0],0))
                    elif dist.pos_score<dist.neg_score:
                        val=0-dist.neg_score
                        negative.add((word[0],0))

                    if val!=0.0:
                        newlist.append((i,val))

        i=i+1
    return newlist



def phrase_polarity(tree_string):


    lp_cnt=tree_string.count(')')
    lp_var_flag=1
    misslist=[]
    while lp_var_flag:
        
        
        i=tree_string.rfind('(')
        j=tree_string[i:len(tree_string)].find(')')
        new_str = tree_string[i:i+j+1]

        sumval=0
        dig_flag=0
        for lp_var in range(len(new_str)):
            if new_str[lp_var].isdigit():
                dig_flag=1
                int_dig=int(new_str[lp_var])
                if new_str[lp_var-1]=='-':
                    int_dig*=-1				
                sumval+=int_dig
        
        if dig_flag:
            repl_val= sumval
        else:
            repl_val=1
            word_str=new_str[new_str.rfind(' ')+1:len(new_str)-1]
            
            if (word_str,0) in positive or (word_str,0) in negative or (word_str,1) in positive or (word_str,1) in negative:
                if (word_str,0) in negative:
                    repl_val=-1
                if (word_str,1) in negative:
                    repl_val=-1
                    misslist.append(word_str)
                if (word_str,1) in positive:
                    misslist.append(word_str)
            elif swn.senti_synsets(word_str):
                dist=swn.senti_synsets(word_str)[0]
                if dist.pos_score<dist.neg_score:
                    repl_val=-1
                    negative.add((word_str,0))
                else:
                    positive.add((word_str,0))
            else:
               misslist.append(word_str)
        tree_string = tree_string.replace(new_str,str(repl_val))
        if tree_string.count('(')==0:
            lp_var_flag=0       
        lp_cnt-=1
    if int(tree_string)>0:
        for missedword in misslist:
            positive.add((missedword,1))
            if (missedword,1) in negative:
                negative.remove((missedword,1))
    else:
        for missedword in misslist:
            negative.add((missedword,1))
            if (missedword,1) in positive:
                positive.remove((missedword,1))
        
    return tree_string




def parse_to_string(tree_string):


    lp_cnt=tree_string.count(')')
    lp_var_flag=1
    text_string=''
    temp=[]

    while lp_var_flag:

        i=tree_string.rfind('(')
        j=tree_string[i:len(tree_string)].find(')')
        new_str = tree_string[i:i+j+1]
        repl_val = new_str
        temp = new_str.split(' ', 1)
        if len(temp)==2:
            repl_val =temp[1]         
        tree_string = tree_string.replace(new_str,' '+repl_val[:len(repl_val)-1])
        if tree_string.count('(')==0:
            lp_var_flag=0      
        lp_cnt-=1

    temp = tree_string.split(' ', 1)
    if len(temp)==2:    
        tree_string = temp[1]
    tree_string = tree_string[:len(tree_string)-1]
    tree_string=' '.join(tree_string.split())
    
    return tree_string



def cut_adjectives(tree_string):

    cut_list=[]
    temp_string = tree_string

    while temp_string.find('(ADJP')!=-1:
            temp2_string = temp_string            
            p=temp_string.find('(ADJP')
            if p != -1:          
                temp_string = temp_string[p:]
                pcnt=0
                for j in range(len(temp_string)):
                    if temp_string[j]=='(':
                        pcnt+=1
                    elif temp_string[j]==')':
                        pcnt-=1
                    if pcnt==0:
                        q=j
                        break
                temp_string = temp_string[:q+1]
                adjp_count = temp_string.count('(ADJP',0,len(temp_string))            
                        
            new_str=temp_string
            cut_list.append(new_str)
            temp_string = temp2_string[temp2_string.find(new_str)+len(new_str):]

    return cut_list


def phrase_analysis(filepath):
    file_id = open(filepath)
    data = file_id.read()
    sentenceEnders = re.compile('[.!?]')
    sentenceList = sentenceEnders.split(data)
    phrase_pol_list=[]
    cnvrtd_line=''
    fid = open('dynamic_dictionary')
    dict_set=[]
    dict_set = pickle.load(fid)
    
    for item in dict_set[0]:
        positive.add(item)
    for item in dict_set[1]:
        negative.add(item)

    cut_list=[]
    for i in range(len(sentenceList)-1):
        line=sentenceList[i].strip()
        temp_file= open('C:\\parse-test\\tempFile.txt','w')
        temp_file.write(line)
        temp_file.close()

        filepath="C:\\parse-test\\tempFile.txt"
        prsnt_dir = os.getcwd()
        os.chdir("C:\\stanford-parser\\")
        test_line = open(filepath).readlines()
        bracketed=os.popen("lexparser.bat "+filepath).readlines()
        os.chdir(prsnt_dir)
        
        tree_list = []
        for item in bracketed:
            if item == '\n':
                break
            tree_list.append(item)
       
        tree_string=''.join(tree_list)
        #tree_var = Tree.parse(tree_string)
        #tree_var.draw()
        cut_list.append(cut_adjectives(tree_string))
        finflag=1
        while finflag ==1:
            finflag=0
            for in_string in cut_list[i]:
                if in_string.count('(ADJP',0,len(in_string))>1:
                    finflag=1
                    break
            if finflag==0:    
                break

            cut_list[i].remove(in_string)
            for phr in cut_adjectives(in_string[5:]):
                cut_list[i].append(phr)

        for phr in cut_list[i]:
            tree_string = tree_string.replace(phr,'(ADJP phrase_'+phrase_polarity(phr)+')')

        test_str=parse_to_string(tree_string)
        cnvrtd_line+=test_str+' . '

    temp_file2= open('C:\\parse-test\\tempFile.txt','w')
    temp_file2.write(cnvrtd_line)
    temp_file2.close()
    tag_words = []
    tag_words = taglist('C:\\parse-test\\tempFile.txt')


    dict_set=[]
    dict_set.append(positive)
    dict_set.append(negative)
    fid = open('dynamic_dictionary','w')
    pickle.dump(dict_set,fid)
    fid.close()
     
    return tag_words



def medianlist(filename,isphrase):


    if isphrase:    
        newlist=phrase_analysis(filename)
    else:
        newlist=taglist(filename)
    i=0
    ppmedlist=[]
    pnmedlist=[]
    nnmedlist=[]
    ppval=0
    nnval=0
    pnval=0
    

    while(i<=len(newlist)):
        seglist=newlist[i:i+100]
        pp_distance_list=[]
        nn_distance_list=[]
        pn_distance_list=[]
        for word1 in seglist:
            for word2 in seglist:
                if(word2[0]>word1[0]):
                    if(word1[1]>0 and word2[1]>0):
                        pp_distance_list.append(word2[0]-word1[0])
                    elif(word1[1]<0 and word2[1]<0):
                        nn_distance_list.append(word2[0]-word1[0])
                    else:
                        pn_distance_list.append(word2[0]-word1[0])

        if len(pp_distance_list) !=0:
            ppval=1
        if len(nn_distance_list) !=0:
            nnval=1
        if len(pn_distance_list) !=0:
            nnval=1
                    
        ppmedlist.append(numpy.median(pp_distance_list))
        pnmedlist.append(numpy.median(pn_distance_list))
        nnmedlist.append(numpy.median(nn_distance_list))
        i=i+100


    if ppval==0:
        ppmed=0
    else:
        ppmed=numpy.median(ppmedlist)

    if nnval==0:
        nnmed=0
    else:
        nnmed=numpy.median(nnmedlist)

    if pnval==0:
        pnmed=0
    else:
        pnmed=numpy.median(pnmedlist)


    elt=(ppmed,nnmed,pnmed)     
    return elt





def bin_list(filename,isphrase):

    if isphrase:    
        newlist=phrase_analysis(filename)
    else:
        newlist=taglist(filename)
        
    i=0
    binsize=5
    
    ppbinlist=[]
    pnbinlist=[]
    nnbinlist=[]
    
    for i in range(500):
        ppbinlist.append(0)
        pnbinlist.append(0)
        nnbinlist.append(0)

    for word1 in newlist:
        for word2 in newlist:
            if(word2[0]>word1[0]):
                temp=(word2[0]-word1[0])/binsize
                if(word1[1]>0 and word2[1]>0):
                    ppbinlist[temp]+=1
                elif(word1[1]<=0 and word2[1]<=0):
                    nnbinlist[temp]+=1
                else:
                    pnbinlist[temp]+=1

    elt=[]
    elt.extend(ppbinlist)
    elt.extend(nnbinlist)
    elt.extend(pnbinlist)
    return elt


def pattern_list(filename,isphrase):

    if isphrase:    
        newlist=phrase_analysis(filename)
    else:
        newlist=taglist(filename)
    
    pattern=[]
    pat_len=20
    for i in range(pat_len):
        pattern.append(1)
        
    elt=[]

    i=0
    for word in newlist:
        if word[1]<=0:
            pattern[i]=0
        i=(i+1)%pat_len
        if i==0:
            elt.append(pattern)
            pattern=[]
            for j in range(pat_len):
                pattern.append(1)
         
    if i!=0:
        elt.append(pattern)

    if len(elt) ==0:
        temp_pat=[]
        for j in range(pat_len):
            temp_pat.append((j+1)%2)
        elt.append(temp_pat)
        
    return elt

