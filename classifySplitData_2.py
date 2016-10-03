#-*- coding=utf-8 -*-

'''
作用：将含有拆分信息的题目分成三类：
    1、不需要拆分的原试题
    2、需要拆分的原试题，并且并列结构的左边界就是选项第一个词，即拆分后的部分不需要人工修改
    3、需要拆分的原试题，并且并列结构的左边界不是选项第一个词，即拆分后的部分需要人工修改
输入：包含所有拆分数据的文件，即filterSplitData_1.py的输出文件，以infilename指定
输出：三个文件，依次对应上述三种数据，以outfileNamePart指定输出文件的文件名前缀

其他作用：输出三种试题的相关统计信息
'''



yCount=0   #所有标记为需要拆分的原始试题数（仅拆分前）
nCount=0   #所有标记为不需要拆分的原始试题数
ori_y_Count=0    #需要拆分的试题中，拆分后不需要手工修改（即并列结构左边界正好的选项第一个字）的原始试题数（拆分前的试题数）
mod_y_Count=0    #需要拆分的实体中，拆分后需要手工修改（即并列结构左边界在题目中）的原始试题数（拆分前的试题数）


infilename="splitData_146406856066.byPaper.choice.csv"
outfileNamePart="146406856066"
typename=['noSplit','oriSplit','modSplit']
outfiles=[]

#拆分信息在原文件表格中的列下标
splitColIndex=3

infile=open(infilename)
for t in typename:
    f=open(outfileNamePart+"."+t+".csv","w")
    outfiles.append(f)

title=infile.readline()
for f in outfiles:
    f.write(title)

tmp=[]
for line in infile.readlines():
    tag=line.split(",")[splitColIndex]
    if tag=="n" or tag=="y":
        mod=False
        for t in tmp:
            if t.split(",")[splitColIndex]=="ed-mod":
                mod=True
                break
        for t in tmp:
            if mod==True:
                outfiles[2].write(t)
            else:
                outfiles[1].write(t)
        if tmp!=[] and mod==True:
            mod_y_Count+=1
            yCount+=1
        elif tmp!=[] and mod==False:
            ori_y_Count+=1
            yCount+=1
        tmp=[]
        
    if tag=="n":
        outfiles[0].write(line)
        nCount+=1
    else:
        tmp.append(line)
    
mod=False
for t in tmp:
    if t.split(",")[splitColIndex]=="ed-mod":
        mod=True
        break
for t in tmp:
    if mod==True:
        outfiles[2].write(t)
    else:
        outfiles[1].write(t)
if tmp!=[] and mod==True:
    mod_y_Count+=1
    yCount+=1
elif tmp!=[] and mod==False:
    ori_y_Count+=1
    yCount+=1

infile.close()
for f in outfiles:
    f.close()

print "所有试题的数量（拆分前）：\t"+str(nCount+yCount)
print "（type1）不需要拆分的试题数量：\t"+str(nCount)
print "（type1）不需要拆分的试题比例：\t"+str(nCount/float(nCount+yCount))
print "（type2+3）需要拆分的试题数量（在拆分前的试题中计算）：\t"+str(yCount)
print "（type2+3）需要拆分的试题比例（在拆分前的试题中计算）：\t"+str(yCount/float(nCount+yCount))
print ""
print "（type2）拆分后不修改的试题数量（在拆分前的试题中计算）：\t"+str(ori_y_Count)
print "（type2）拆分后不修改的试题比例（在拆分前的试题中计算）：\t"+str(ori_y_Count/float(yCount+nCount))
print "（type3）拆分后需修改的试题数量（在拆分前的试题中计算）：\t"+str(mod_y_Count)
print "（type3）拆分后需修改的试题比例（在拆分前的试题中计算）：\t"+str(mod_y_Count/float(yCount+nCount))


