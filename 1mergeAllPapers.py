# -*- coding: utf-8 -*-

'''
作用：用于将下载所得的所有试卷数据合并，输出至单个文件中
输入：data_dir为下载的压缩包解压后的目录，其中有多个.csv试卷数据，为输入文件
输出：outfile_name为合并后输出文件的文件名（合并后每行数据的第一列会加上所属试卷名），输出文件与当前脚本同目录
'''

import os

data_dir="146406856066.byPaper.choice"
outfile_name="merged_"+data_dir+".csv"

filenames=os.listdir(data_dir)
outfile=open(outfile_name,"w")

title_flag=False

for fname in filenames:
    infile=open(data_dir+"/"+fname)
    title=infile.readline()
    if title_flag==False:
        outfile.write("试卷名,"+title)
        title_flag=True

    for line in infile.readlines():
        outfile.write(fname.decode("gbk").encode("utf-8").split(".")[0]+","+line)

    infile.close()

outfile.close()
    
    

