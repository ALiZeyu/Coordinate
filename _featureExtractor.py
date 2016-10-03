#coding=utf-8

#对原始数据抽取各种特征，转换成分类器所需数据
#特征如下：
#拆分成的两部分各自字数差的绝对值
#拆分成的两部分的词性序列的编辑距离
#拆分后两部分的第一个词的词性组合，最后一个词的词性组合
#题面中的最后一个词
#题面中的最后两个词拼接起来（如果只有一个词，前一个词用NULL）
#两个子句是否包含时间词的布尔值组合

class featureExtractor():
    def __init__(self):
        #cuewordFile.txt删掉了时间限定和实体信息陈述两类模板的线索词
        #cuewordFile-sim.txt只保留影响、趋势、因果三类（有提升）
        self.cdict={}
        cf=open("cuewordFile-sim.txt")        
        
        newt=True
        tname=""
        for l in cf.readlines():
            l=l.strip().decode("utf-8")
            if l=="":
                newt=True
                tname=""
                continue
                
            if newt==True:
                self.cdict[l]={}
                tname=l
                newt=False
            elif newt==False:
                #print l
                l=l.split(":")
                self.cdict[tname][l[0]]=int(l[1])
        cf.close()
        
    def wordNumDiff(self,seg_parts):
        #当前假设只有一个逗号
        if len(seg_parts)!=2:
            raise Exception(u"应该只有两个部分："+str(seg_parts))
        return abs(len(seg_parts[0])-len(seg_parts[1]))

    def charNumDiff(self,text_parts):
        #当前假设只有一个逗号
        if len(text_parts)!=2:
            raise Exception(u"应该只有两个部分："+str(text_parts))
        return abs(len(text_parts[0])-len(text_parts[1]))
        

    def editDistanceOfPostag(self,postag_parts):
        '''
            输入的是一个列表，其中每个元素分别对应选项部分被逗号分号后的几个部分的词性列表
        '''
        
        return self.editDistance(postag_parts[0],postag_parts[1])

    #计算两个列表的编辑距离，editDistanceOfPostag的功能函数
    def editDistance(self,arr1,arr2):
        dis=[[0 for i in range(len(arr1)+1)] for j in range(len(arr2)+1)]

        for i in range(len(arr1)+1):
            dis[0][i]=i
        for j in range(len(arr2)+1):
            dis[j][0]=j
        
        for j in range(1,len(arr2)+1):
            for i in range(1,len(arr1)+1):
                if arr1[i-1]==arr2[j-1]:
                    dis[j][i]=dis[j-1][i-1]
                else:
                    dis[j][i]=min(dis[j-1][i]+1,dis[j][i-1]+1,dis[j-1][i-1]+1)

        return dis[-1][-1]

    def PosComb(self,ctype,postag_parts):
        return self.getPosComb(ctype,postag_parts[0],postag_parts[1])

    #返回指定类型的词性组合，以及这对词性是否相同的布尔值；PosComb的功能函数
    def getPosComb(self,ctype,pos1,pos2):
        if len(pos1)==0 or len(pos2)==0:
            raise Exception(u"某个部分词性列表为空:"+str(pos1)+"--"+str(pos2))
        if ctype=="first":
            return pos1[0]+"/"+pos2[0],pos1[0]==pos2[0]
        elif ctype=="last":
            return pos1[-1]+"/"+pos2[-1],pos1[-1]==pos2[-1]

    def lastWordsInTimian(self,tm_seg,wnum):
        if len(tm_seg)==0:
            raise Exception("题面没有词")

        if wnum<=len(tm_seg):
            return "/".join(tm_seg[-wnum:])
        else:
            return "NULL/"*(wnum-len(tm_seg))+"/".join(tm_seg)

    def timeInEachPartComb(self,tm_seg,seg_parts,timeIndexStr):
        #当前假设只有一个逗号
        if len(seg_parts)!=2:
            raise Exception(u"应该只有两个部分："+str(seg_parts))

        part1Time=False
        part2Time=False

        #选项第一个词在整句分词结果中的下标
        txSplitPos=len(tm_seg)
        #选项拆分后，第二个部分的第一个词在整句分词结果中的下标
        part2StartPos=txSplitPos+len(seg_parts[0])
        #整句的总分词数
        totalLen=part2StartPos+len(seg_parts[1])

        timeIndexList=[int(index) for index in timeIndexStr.split()]
        for ti in timeIndexList:
            '''
            print ti
            print txSplitPos,part2StartPos
            print part2StartPos,totalLen
            print txSplitPos<=ti<part2StartPos
            print part2StartPos<=ti<totalLen
            '''
            if txSplitPos<=ti<part2StartPos:
                part1Time=True
            elif part2StartPos<=ti<totalLen:
                part2Time=True

        return str(part1Time)+"/"+str(part2Time)

    def containCuewords(self,seg_parts,ctype):
        #当前假设只有一个逗号
        if len(seg_parts)!=2:
            raise Exception(u"应该只有两个部分："+str(seg_parts))
        
        cInPart=[[],[]]
        
        for index,seg in enumerate(seg_parts):
            for tname in self.cdict:                
                for cw in self.cdict[tname]:
                    cw=cw.split("/")
                    flag=True
                    for x in cw:
                        if x not in seg:
                            flag=False
                    if flag==True:
                        cInPart[index].append(tname)
                        break

        
        if len(cInPart[0])>1 or len(cInPart[1])>1:
            #print " ".join(seg_parts[0])
            #print " ".join(cInPart[0]),"p0"
            #print " ".join(seg_parts[1])
            #print " ".join(cInPart[1]),"p1"
            #print "======"
            pass
        

        c1="None"
        c2="None"
        if len(cInPart[0])>0:
            c1=cInPart[0][0]
        if len(cInPart[1])>0:
            c2=cInPart[1][0]

        if ctype=="comb":
            return c1+"/"+c2
        elif ctype=="main":
            if u"影响" in cInPart[0] or u"影响" in cInPart[1]:
                return u"影响"
            elif u"因果" in cInPart[0] or u"因果" in cInPart[1]:
                return u"因果"
            elif u"条件" in cInPart[0] or u'条件' in cInPart[1]:
                return u'条件'
            elif u"趋势" in cInPart[0] or u'趋势' in cInPart[1]:
                return u'趋势'

    def bothContainLonLat(self,seg_parts):
        text1="".join(seg_parts[0])
        text2="".join(seg_parts[1])
        if u"°" in text1 and u"°" in text2:            
            flag1=False
            flag2=False
            for c in ['E','W','N','S']:
                if c in text1:
                    flag1=True
                if c in text2:
                    flag2=True                
            return flag1 and flag2
        
        return False
                    
            
                
