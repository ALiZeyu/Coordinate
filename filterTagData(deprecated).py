#-*- coding=utf-8 -*-

'''
作用1：从所有试卷数据合并后的文件中，过滤出含有拆分信息的数据（即选项中含有中文逗号的试题文本对应的数据）
输入：mergeAllPapers_0.py的输出文件，文件名以infilename指定
输出：输出文件名以outfilename指定，输出位置在脚本同目录下

作用2：输出拆分信息相关的统计数据
'''

infilename="merged_146312775198.byPaper.choice.csv"
outfilename="ContainTagData_146312775198.byPaper.choice.csv"

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
dunCount=0 #所有含有顿号的试题数
douCount=0 #所有含有逗号的试题数
dCount=0   #含有顿号以及逗号的行数


#写标题
outfile.write(infile.readline())

for line in infile.readlines():
    allCount+=1
    tag=line.split(",")[splitColIndex]
    text=line.split(",")[2]

    if tag=="y":
        yCount+=1
    elif tag=="n":
        nCount+=1
    text=text.decode("utf-8")
    if u"、" in text and u"，" in text:
        dunCount+=1
        douCount+=1
        dCount+=1
        outfile.write(line)
    elif u"，" in text:
        douCount+=1
        outfile.write(line)
    elif u"、" in text:
        dunCount+=1
        outfile.write(line)

infile.close()
outfile.close()

print "***以下三行统计考虑所有拆分前、拆分后组合的试题文本***"
print "所有试题数据的行数\t"+str(allCount)
print "n的行数\t"+str(nCount)
print "y的行数\t"+str(yCount)
print "含有逗号的行数\t"+str(douCount)
print "含有顿号的行数\t"+str(dunCount)
print "同时含有逗号顿号的行数\t"+str(dCount)
