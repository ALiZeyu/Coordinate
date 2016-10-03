#coding=utf-8
from _featureExtractor import *
from _featureConfig import *

def convertSingleData(textInfo):
    label=textInfo['split']

    #得到选项和题面分别对应的分词和词性
    xuanxiangStartIndex=None   #选项开始的词在分词结果中对应的下标
    tm_text=None
    tm_seg=None
    tm_postag=None
    xx_text=None
    xx_seg=None
    xx_postag=None

    text=textInfo['text'].split("\t")
    seg=textInfo['seg'].split()
    postag=textInfo['postag'].split()

    for i in range(len(seg)):
        if "".join(seg[:i])==text[0]:
            xuanxiangStartIndex=i

    tm_text=text[0]
    tm_seg=seg[:xuanxiangStartIndex]
    tm_postag=postag[:xuanxiangStartIndex]
    xx_text=text[1]
    xx_seg=seg[xuanxiangStartIndex:]
    xx_postag=postag[xuanxiangStartIndex:]
    '''
    print text[0],'--',text[1]
    print xuanxiangStartIndex
    print " ".join(seg[xuanxiangStartIndex:])
    print " ".join(postag[xuanxiangStartIndex:])
    '''

    #得到选项被逗号拆开后两部分对应的分词、词性
    text_parts=xx_text.split(u"，")
    
    if len(text_parts)!=2:
        raise Exception(u"应该有且只有一个逗号："+xx_text)
    splitPos=xx_seg.index(u"，")

    seg_parts=[xx_seg[:splitPos],xx_seg[splitPos+1:]]
    postag_parts=[xx_postag[:splitPos],xx_postag[splitPos+1:]]
        
    fe=featureExtractor()
    
    featureVec={}
    
    featureVec['wordNumDiff']=fe.wordNumDiff(seg_parts)
    featureVec['charNumDiff']=fe.charNumDiff(text_parts)
    featureVec['postagEditDistance']=fe.editDistanceOfPostag(postag_parts)
    
    lastPosPair=fe.PosComb("last",postag_parts)
    featureVec['lastPosComb']=lastPosPair[0]
    featureVec['lastPosEqual']=lastPosPair[1]
    
    firstPosPair=fe.PosComb("first",postag_parts)
    featureVec['firstPosComb']=firstPosPair[0]
    featureVec['firstPosEqual']=firstPosPair[1]

    featureVec['lastWordInTimian']=fe.lastWordsInTimian(tm_seg,1)
    featureVec['lastTwoWordsInTimian']=fe.lastWordsInTimian(tm_seg,2)
    featureVec['lastPostagInTimian']=tm_postag[-1]

    featureVec['timeCombination']=fe.timeInEachPartComb(tm_seg,seg_parts,textInfo['time'])
    featureVec['containCuewordsComb']=fe.containCuewords(seg_parts,"comb")
    featureVec['containCuewordsMain']=fe.containCuewords(seg_parts,"main")

    featureVec['firstWordInSecondPart']=seg_parts[1][0]
    featureVec['firstPostagInSecondPart']=postag_parts[1][0]
    featureVec['lastWordInFirstPart']=seg_parts[0][-1]

    featureVec['bothContainLonLat']=fe.bothContainLonLat(seg_parts)

    delFe=[]
    for fe in featureVec:
        if fe not in featureNames:
            delFe.append(fe)

    for fe in delFe:
        del featureVec[fe]
    
    data=(featureVec,label)
    return data



