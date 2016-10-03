#-*- coding=utf-8 -*-

'''
作用1：从所有试卷数据合并后的文件中，过滤出含有拆分信息的数据（即选项中含有中文逗号的试题文本对应的数据）
输入：mergeAllPapers_0.py的输出文件，文件名以infilename指定
输出：输出文件名以outfilename指定，输出位置在脚本同目录下

作用2：输出拆分信息相关的统计数据
'''

infilename="merged_146406856066.byPaper.choice.csv"
outfilename="splitData_146406856066.byPaper.choice.csv"

infile=open(infilename)
outfile=open(outfilename,"w")

#拆分信息在原文件表格中的列下标
splitColIndex=3

#所有试题数据行数
allCount=0
#含有拆分信息数据行数
splitCount=0


yCount=0   #所有标记为需要拆分的原始试题数（仅拆分前）
nCount=0   #所有标记为不需要拆分的原始试题数
NoneCount=0  #所有选项不含有逗号的原始试题数
ori_y_Count=0    #需要拆分的试题中，拆分后不需要手工修改（即并列结构左边界正好的选项第一个字）的原始试题数（拆分前的试题数）
mod_y_Count=0    #需要拆分的实体中，拆分后需要手工修改（即并列结构左边界在题目中）的原始试题数（拆分前的试题数）

#写标题
outfile.write(infile.readline())

for line in infile.readlines():
    allCount+=1
    tag=line.split(",")[splitColIndex]
    if tag!="None":
        outfile.write(line)
        splitCount+=1
        if tag=="y":
            yCount+=1
        elif tag=="n":
            nCount+=1
    else:
        NoneCount+=1
        
infile.close()
outfile.close()

print "***以下三行统计考虑所有拆分前、拆分后组合的试题文本***"
print "所有试题数据的行数\t"+str(allCount)
print "含拆分信息的数据行数\t"+str(splitCount)
if allCount!=0:
    print "含拆分信息的数据所占比重\t"+str(splitCount/float(allCount))
print "******************************************"

orisum=NoneCount+yCount+nCount
print "***以下两行统计考虑所有拆分前的原始试题文本***"
print "共有原始选项个数：\t",orisum
print "不含逗号的选项及其所占比例:\t",NoneCount,float(NoneCount)/orisum
print "含逗号但不需拆分的选项及其比例：\t",nCount,float(nCount)/orisum
print "含逗号且需要拆分的选项及其比例：\t",yCount,float(yCount)/orisum
