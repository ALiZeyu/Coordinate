#coding=utf-8

import os
from _featureExtractor import *
from _convertDataByFeatureTemplate import *
from _getTrainTestDataset import *
from _featureConfig import *
from nltk.classify import maxent

def getTrainTestData():
    allDataSet=getDataSetForMaxent()
    datafile=open("dataForMaxentInfos.csv")

    testFile=[u'2011-北京',u'2012-北京',u'2013-北京',u'2014-北京',u'2015-北京']

    testSet=[]
    trainSet=[]
    title=datafile.readline().strip().split(",")
    indexDict=dict(sourceIndex=0,
                   textIndex=2,
                   splitIndex=3,
                timeIndex=4,
                locIndex=5,
                segIndex=8,
                postagIndex=10,
                parseIndex=11)
    for l in datafile.readlines():
        l=l.strip().decode('utf-8').split(",")
        data={}
        for fe in featureNames:
            #print title.index(fe)
            data[fe]=l[title.index(fe)]
        label=l[-1]
        source=l[0]
        text=l[1]
        if source in testFile:
            testSet.append({'data':(data,label),'text':text})
        else:
            trainSet.append({'data':(data,label),'text':text})
    datafile.close()
    return trainSet,testSet

def trainAndTest():        
    train_set,test_set=getTrainTestData()
    
    fout=open("predict_result_specificTestData.csv","w")  #foldnum次的测试结果都在同一个文件中
    train_data=[x['data'] for x in train_set]
    train_text=[x['text'] for x in train_set]
    test_data=[x['data'] for x in test_set]
    test_text=[x['text'] for x in test_set]
        
    encoding = maxent.TypedMaxentFeatureEncoding.train(train_data, count_cutoff=3, alwayson_features=True)
    classifier = maxent.MaxentClassifier.train(train_data, bernoulli=False, encoding=encoding, trace=0)
    classifier.show_most_informative_features(10)
    res=classifier.classify_many([t[0] for t in test_data])

    fout.write("oritext,real_label,predoct_label,isRight")
    for fvt in featureNames:
        fout.write(","+fvt)
    fout.write("\n")
    for t,d,r in zip(test_text,test_data,res):
        fout.write(t.encode('utf-8')+",")
        fout.write(d[1].encode('utf-8')+",")
        fout.write(r.encode('utf-8')+",")
        fout.write(str(d[1]==r))
        for fvt in featureNames:
            try:
                fout.write(","+str(d[0][fvt]).encode("utf-8"))
            except:
                fout.write(","+str(d[0][fvt].encode("utf-8")))
        fout.write("\n")        
    
    #print res
    rightY=0
    wrongY=0
    rightN=0
    wrongN=0
    for t,r in zip(test_data,res):
        if t[1]=="y":
            if r=="y":
                rightY+=1
            else:
                wrongN+=1
        else:
            if r=="y":
                wrongY+=1
            else:
                rightN+=1
    '''        
    print "rightY",rightY
    print "wrongY",wrongY
    print "rightN",rightN
    print "wrongN",wrongN
    '''
    Yaccuracy=0
    Naccuracy=0
    Yrecall=0
    Nrecall=0
    totalAccuracy=0
    
    try:
        Yaccuracy=rightY/float(rightY+wrongY)
    except:
        Yaccuracy=-0.1
    try:
        Naccuracy=rightN/float(rightN+wrongN)
    except:
        Naccuracy=-0.1
    try:
        Yrecall=rightY/float(rightY+wrongN)
    except:
        Yrecall=-0.1
    try:
        Nrecall=rightN/float(rightN+wrongY)
    except:
        Nrecall=-0.1
    try:
        totalAccuracy=(rightY+rightN)/float(rightY+rightN+wrongY+wrongN)
    except:
        totalAccuracy=-0.1
    
    print "Yaccuracy:",Yaccuracy
    print "Naccuracy:",Naccuracy
    print "Yrecall:",Yrecall
    print "Nrecall:",Nrecall
    print "totalAccuracy:",totalAccuracy
    '''
    resFile.write("Yaccuracy:"+str(Yaccuracy)+"\n")
    resFile.write("Naccuracy:"+str(Naccuracy)+"\n")
    resFile.write("Yrecall:"+str(Yrecall)+"\n")
    resFile.write("Nrecall:"+str(Nrecall)+"\n")
    resFile.write("totalAccuracy:"+str(totalAccuracy)+"\n")
    forMeanAcc+=totalAccuracy
    resFile.write("######################\n")
    '''
    fout.close()

trainAndTest()



