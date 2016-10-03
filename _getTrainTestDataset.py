#coding=utf-8

from _convertDataByFeatureTemplate import *
from _featureConfig import *

#从原始csv文件中获取分类器所需要的格式的数据
#暂时只考虑拆分成两部分的句子
#不划分训练集测试集，所有样本均返回，返回的样本中没有样本的来源信息
def getDataSetForMaxent():
    print "getDataSetForMaxent"
    infile=open("merged_146406856066.byPaper.choice.csv")
    outfile=open("dataForMaxentInfos.csv","w")
    
    indexDict=dict(sourceIndex=0,
                   textIndex=2,
                   splitIndex=3,
                timeIndex=4,
                locIndex=5,
                segIndex=8,
                postagIndex=10,
                parseIndex=11)

    allDataSet={"y":[],"n":[]}

    #写输出文件的标题
    outfile.write("source,oritext,seg,postag")

    for fvt in featureNames:
        outfile.write(","+fvt)
    outfile.write(",label\n")
    
    index=0
    for l in infile.readlines():
        #print index
        #index+=1
        infos=l.strip().decode("utf-8").split(",")

        split=infos[indexDict['splitIndex']]
        
        if split=="y" or split=="n":
            textInfo={}
            for fieldIndexName in indexDict:
                textInfo[fieldIndexName[:-5]]=infos[indexDict[fieldIndexName]]

            if len(textInfo['text'].split("\t")[1].split(u"，"))>2:
                continue
            
            data=convertSingleData(textInfo)
            #将处理后的结果以及部分原始数据写入中间文件中
            outfile.write(textInfo['source'].encode("utf-8")+",")
            outfile.write(textInfo['text'].encode("utf-8")+",")
            outfile.write(textInfo['seg'].encode("utf-8")+",")
            outfile.write(textInfo['postag'].encode("utf-8"))

            for fvt in featureNames:
                try:
                    outfile.write(","+str(data[0][fvt]).encode("utf-8"))
                except:
                    outfile.write(","+str(data[0][fvt].encode("utf-8")))

            outfile.write(","+data[1].encode("utf-8")+"\n")
            
            allDataSet[data[1]].append({'data':data,'text':textInfo['text']})
            #break
        else:
            continue

    infile.close()
    outfile.close()
    return allDataSet

#对数据做统计和训练集测试集划分
#第3个参数表示将原始数据的多少拿出作为测试集，例如0.1表示将10%的数据作为测试集
#训练集和测试集中，两种类型的数据比例一致
#会返回划分后的数据集中对应在抽取特征时输出的文件中的index（文件中的行数-1）的列表
#可以完成十折交叉验证，foldnum为总的折数（比如十折中是10），foldIndex为其中的第几次
def splitData(dataset,testProp,foldnum,foldIndex):
    #print "splitData: testProp="+str(testProp)
    
    nData=dataset['n']
    yData=dataset['y']
    
    #统计并输出
    #print u"  共有y数据"+str(len(yData))
    #print u"  共有n数据"+str(len(nData))

    #划分数据
    train_set=[]
    test_set=[]

    foldlenN=len(nData)/foldnum
    foldlenY=len(yData)/foldnum
    train_set=nData[:foldlenN*(foldIndex%foldnum)]+nData[foldlenN*(foldIndex%foldnum)+int(len(nData)*testProp):]+\
               yData[:foldlenY*(foldIndex%foldnum)]+yData[foldlenY*(foldIndex%foldnum)+int(len(yData)*testProp):]
    test_set=nData[foldlenN*(foldIndex%foldnum):foldlenN*(foldIndex%foldnum)+int(len(nData)*testProp)]+\
              yData[foldlenY*(foldIndex%foldnum):foldlenY*(foldIndex%foldnum)+int(len(yData)*testProp)]

    #print u"  训练集大小："+str(len(train_set))
    #print u"  测试集大小："+str(len(test_set))
    return train_set,test_set

#dataset={"y":list(range(200)),'n':list(range(200,220))}
#print splitData(dataset,0.1,10,9)

def getBalancedDataSet(dataset,strategy):
    pass

#将dataset中的数据按照remainProp的比例取出一部分返回
#本函数用于考查不同数据规模对于分类器性能的影响大小
def scaleData(dataset,remainProp):
    scaledData={"y":[],"n":[]}
    for c in dataset:
        scaledData[c]=dataset[c][:int(len(dataset[c])*remainProp)]
    return scaledData
