#coding = utf-8
# -*- coding: UTF-8 -*-

import os
import arcpy
from arcpy import env

def delete_file_folder(src):  
    '''delete files and folders''' 
    if os.path.isfile(src):  
        try:  
            os.remove(src)  
        except:  
            pass 
    elif os.path.isdir(src):  
        for item in os.listdir(src):  
            itemsrc=os.path.join(src,item)  
            delete_file_folder(itemsrc)  
        try: 
            os.rmdir(src)  
        except: 
            pass 

def  Do(in_path,out_path,out_gdb,fcs):
    #获得输入gdb文件路径列表
    env.workspace = in_path
    gdblist = arcpy.ListWorkspaces()
    
    #输出gdb的绝对路径
    outGDBpath = os.path.join(out_path,out_gdb)
    
    #若输出gdb已结存在，则删除之
    if os.path.exists(outGDBpath):
        delete_file_folder(outGDBpath)
    
    #创建输出gdb
    arcpy.CreateFileGDB_management(out_path,out_gdb)
    
    for fc in fcs:
        #输出fc绝对位置
        fc_out = outGDBpath + os.sep + fc
        #初始化fc列表和fc计数
        fclist = []
        fc_cnt1 = 0
        #按照gdb遍历
        for gdb in gdblist:
            if not gdb[-4:] in [".gdb"]:
                continue
            #输入fc
            fc_from = gdb +os.sep + fc
            if arcpy.Exists(fc_from):
                #fc列表
                fclist.append(fc_from)
                #fc计数
                fc_count = int(arcpy.GetCount_management(fc_from).getOutput(0))
                fc_cnt1 = fc_cnt1 + fc_count
                print fc_from + ': ' + str(fc_count)
            else:
                print fc_from + ' is missing'
        #输入fc总数
        print str(fc_cnt1) + ' fcs input'
        #输入fc合并到输出fc
        arcpy.Merge_management(fclist,fc_out)
        #输出fc计数
        fc_cnt2 = int(arcpy.GetCount_management(fc_out).getOutput(0))
        print str(fc_cnt2) + ' fcs output'
if __name__=="__main__":
    print time.strftime("start:%Y/%m/%d:%H:%M:%S")
    Do(sys.argv[1],sys.argv[2],sys.argv[3],sys.argv[4])
    print time.strftime("done:%Y/%m/%d:%H:%M:%S")
