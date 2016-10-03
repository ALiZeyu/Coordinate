# -*- coding: cp936 -*-
'''
功能：
查看不同数据规模下、不同的训练集划分比例下，训练的结果
输出两个文件：
tmp_res：依次是dataName对应的四种值，每一种值有9*9个数值，对应9种数据规模、9种训练集比例
tmp_f：记录在9*9种数据情况下，判断为Y的F值

'''
import os
from _featureExtractor import *
from _convertDataByFeatureTemplate import *
from _getTrainTestDataset import *
from nltk.classify import maxent

def process():
    print "startProcess"

    plotData={}
    dataName=["YaccuracySeries","NaccuracySeries","YrecallSeries","NrecallSeries"]

    print os.path.exists(os.getcwd()+"/tmp_res.txt")
    if not os.path.exists(os.getcwd()+"/tmp_res.txt"):
        textData,allDataSet=getDataSetForMaxent()

        scaleProp=0.1
        
        for dn in dataName:
            plotData[dn]=[]
            
        for i in range(9):
            print "scaleProp:"+str(scaleProp)
            scaledData=scaleData(allDataSet,scaleProp)
            scaleProp+=0.1
            #balancedDataSet=getBalancedDataSet(scaledData,strategy=0)
            trainProp=0.1

            Yaccuracy=[]
            Naccuracy=[]
            Yrecall=[]
            Nrecall=[]
            x_index=[]

            trainProp=0.1
            for j in range(9):
                print "trainProp:"+str(trainProp)
                train_set,test_set=splitData(scaledData,trainProp)
                trainProp+=0.1
                x_index.append(str(trainProp-0.1))
                #train_set=allDataSet
                #test_set=allDataSet

                encoding = maxent.TypedMaxentFeatureEncoding.train(train_set, count_cutoff=3, alwayson_features=True)
                classifier = maxent.MaxentClassifier.train(train_set, bernoulli=False, encoding=encoding, trace=0)
                classifier.show_most_informative_features(10)
                res=classifier.classify_many([t[0] for t in test_set])
        
                #print res
                rightY=0
                wrongY=0
                rightN=0
                wrongN=0
                for t,r in zip(test_set,res):
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
                
                print "rightY",rightY
                print "wrongY",wrongY
                print "rightN",rightN
                print "wrongN",wrongN
                try:
                    Yaccuracy.append((rightY)/float(rightY+wrongY))
                except:
                    Yaccuracy.append(-0.1)
                try:
                    Naccuracy.append((rightN)/float(rightN+wrongN))
                except:
                    Naccuracy.append(-0.1)
                try:
                    Yrecall.append((rightY)/float(rightY+wrongN))
                except:
                    Yrecall.append(-0.1)
                try:
                    Nrecall.append((rightN)/float(rightN+wrongY))
                except:
                    Nrecall.append(-0.1)
                print "Yaccuracy:",Yaccuracy[-1]
                print "Naccuracy:",Naccuracy[-1]
                print "Yrecall:",Yrecall[-1]
                print "Nrecall:",Nrecall[-1]

            print "###",x_index
            '''
            df=pd.DataFrame({"Yaccuracy":pd.Series(Yaccuracy,index=index),
                         'Naccuracy':pd.Series(Naccuracy,index=index),
                         'Yrecall':pd.Series(Yrecall,index=index),
                         'Nrecall':pd.Series(Nrecall,index=index)})
            print df
            '''

            '''
            plotData["YaccuracySeries"].append(pd.Series(Yaccuracy,index=x_index))
            plotData["NaccuracySeries"].append(pd.Series(Naccuracy,index=x_index))
            plotData["YrecallSeries"].append(pd.Series(Yrecall,index=x_index))
            plotData["NrecallSeries"].append(pd.Series(Nrecall,index=x_index))
            '''

            plotData["YaccuracySeries"].append(Yaccuracy)
            plotData["NaccuracySeries"].append(Naccuracy)
            plotData["YrecallSeries"].append(Yrecall)
            plotData["NrecallSeries"].append(Nrecall)
            
            '''
            ax=plt.subplot(3,4,1)
            ax.set_title("scaleProp="+str(scaleProp-0.1))
            '''
            #break

        '''
        for pdname in plotData:
            plt.figure(figsize=(18,12),dpi=80)
            print pdname
            dfData={}
            for i,series in enumerate(plotData[pdname]):
                dfData[pdname+":"+str(i*0.1+0.1)]=series
                print i
                
                #ax=plt.subplot(3,3,i+1)
                #print series
                #ax.plot(series)
                #ax.set_title("scaleProp="+str(i*0.1+0.1))
                
            ax=plt.subplot(1,1,1)
            ax.set_title(pdname)
            ax.plot(pd.DataFrame(dfData))
            plt.show()
        '''

        tmpf=open("tmp_res.txt","w")
        for pdname in dataName:
            tmpf.write(pdname)
            for d in plotData[pdname]:
                tmpf.write(" ".join([str(x) for x in d])+"\n")
            tmpf.write("\n")
        tmpf.close()
        
    else:
        fres=open("tmp_res.txt")
        for i in range(4):
            plotData[dataName[i]]=[]
            for j in range(9):
                l=fres.readline().strip().split()
                plotData[dataName[i]].append([float(x) for x in l])
            fres.readline()
        
    
        
    #Y_F
    tmpf=open("tmp_f.txt","w")
    for i in range(9):
        for j in range(9):
            #print dataName[2]
            #print i,j
            #print plotData[dataName[2]][i]
            
            p=plotData[dataName[0]][i][j]
            r=plotData[dataName[2]][i][j]
            f=(p*r*2)/(p+r)
            tmpf.write(str(f)+" ")
        tmpf.write("\n")
    tmpf.write("\n")
    
            
    
process()
    
    
    
    
        
        
        
