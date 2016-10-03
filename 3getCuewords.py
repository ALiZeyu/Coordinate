#coding=utf-8

import os

def getCuewords():
    cwFileName="cuewordFile.txt"
    cwDict={}

    
    if os.path.exists(cwFileName):
        print "getCuewords-from existing file"
        cwFile=open(cwFileName)
        lastTN=cwFile.readline().decode("utf-8").strip()
        cwDict[lastTN]={}
        for l in cwFile.readlines():
            l=l.decode('utf-8').strip()
            if l=="":
                lastTN=""
            if lastTN=="":
                lastTN=l
                cwDict[lastTN]={}
            else:
                l=l.split(":")
                cwDict[lastTN][l[0]]=int(l[1])
        cwFile.close()
            
    else:
        print "getCuewords-from merged data"
        infile=open("merged_146406856066.byPaper.choice.csv")
        segIndex=8
        fullcwIndex=15
        fullTemplateIndex=13

        infile.readline()
        for l in infile.readlines():
            l=l.decode("utf-8").strip().split(",")
            seg=l[segIndex].split()
            fullcw=l[fullcwIndex].split()
            fullTemplate=l[fullTemplateIndex]

            '''
            print " ".join([str(i)+"_"+w for i,w in enumerate(seg)])
            print fullTemplate
            print fullcw
            '''
                        
            for t_cw in fullcw:
                t_cw=t_cw.split("_")
                if len(t_cw)>2:
                    raise Exception(u"多余的_")

                ti=t_cw[0]  #该模板在完整模板标注中的下标
                wi=t_cw[1]  #该模板的线索词在分词中的下标（可能是单个数字，也可能是一个范围）

                #检查模板下标是否有重复
                if fullTemplate.count("_"+ti)>1:
                    raise Exception(u"重复的模板下标")
                
                tname=""
                cueword=""
                #找到这个模板下标对应的模板的名字
                indexPos=fullTemplate.find("_"+ti)
                if indexPos==-1:  #如果找不到
                    print "".join(seg),fullTemplate
                else:
                    #找到左边界
                    leftIndex1=fullTemplate[:indexPos].rfind(u"）")
                    leftIndex2=fullTemplate[:indexPos].rfind(u"（")
                    leftIndex3=fullTemplate[:indexPos].rfind(u"，")
                    leftIndex4=fullTemplate[:indexPos].rfind(" ")
                    leftIndex=max(leftIndex1,leftIndex2,leftIndex3,leftIndex4)
                    if leftIndex==-1:
                        tname=fullTemplate[:indexPos].strip()
                    else:
                        tname=fullTemplate[leftIndex+1:indexPos].strip()
                        
                    #得到该线索词组合
                    wi=wi.split("-")
                    for i in wi:
                        cueword+=seg[int(i)]+"/"
                    cueword=cueword[:-1]

                    #print tname,cueword

                    if tname not in cwDict:
                        cwDict[tname]={}
                    cwDict[tname][cueword]=cwDict[tname].get(cueword,0)+1

        
        #写入文件
        cwFile=open(cwFileName,"w")
        for tname in cwDict:
            cwFile.write(tname.encode("utf-8")+"\n")
            for cueword in cwDict[tname]:
                cwFile.write(cueword.encode("utf-8")+":"+str(cwDict[tname][cueword])+"\n")
            cwFile.write("\n")
        cwFile.close()
    
    return cwDict

#getCuewords()


