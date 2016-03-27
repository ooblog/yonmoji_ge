#! /usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import division,print_function,absolute_import,unicode_literals
import sys
import os
import re
os.chdir(sys.path[0])
from LTsv_printf import *
from LTsv_file   import *
from LTsv_gui    import *
from LTsv_kbd    import *

yonmoji_ltsv,yonmoji_config,yonmoji_sitelist="","",""
yonmoji_fontname,yonmoji_fontsize="kantray5x5comic",10; yonmoji_font="{0},{1}".format(yonmoji_fontname,yonmoji_fontsize)
yonmoji_sitefile,yonmoji_pagefile,yonmoji_siteconfig,yonmoji_inputlist,yonmoji_switchlist="","","","",""
yonmoji_column_len=4; yonmoji_column_site,yonmoji_column_page,yonmoji_column_input,yonmoji_column_switch=0,1,2,3
yonmoji_label_W,yonmoji_entry_W,yonmoji_spin_W=200,530,70
yonmoji_W,yonmoji_H=yonmoji_label_W+yonmoji_entry_W,600
yonmoji_username="ooblog"
yonmoji_pagerename,yonmoji_datarename,yonmoji_userrename="<!pagename!>","<!datename!>","<!username!>"
yonmoji_inputTSV,yonmoji_outputHTML,yonmoji_outputCSS,yonmoji_outputJS,yonmoji_outputXML="pages/<!pagename!>.tsv","../<!pagename!>.html","../<!pagename!>.css","../<!pagename!>.js","../<!pagename!>.xml"
yonmoji_datename,yonmoji_datetag="@000y-@0m-@0d","@000y-@0m"

def yonmoji_configload():
    global yonmoji_ltsv,yonmoji_config,yonmoji_sitelist
    global yonmoji_font,yonmoji_fontname,yonmoji_fontsize
    global yonmoji_username
    yonmoji_ltsv=LTsv_loadfile("yonmoji_ge.tsv")
    yonmoji_config=LTsv_getpage(yonmoji_ltsv,"yonmoji_ge")
    yonmoji_fontname=LTsv_readlinerest(yonmoji_config,"fontname",yonmoji_fontname)
    yonmoji_fontsize=min(max(LTsv_intstr0x(LTsv_readlinerest(yonmoji_config,"fontsize")),5),20)
    yonmoji_font="{0},{1}".format(yonmoji_fontname,yonmoji_fontsize)
    yonmoji_sitelist=LTsv_getpage(yonmoji_ltsv,"sitelist")
    yonmoji_username=LTsv_readlinerest(yonmoji_config,"username",yonmoji_username)

def yonmoji_siteload(sitename):
    global yonmoji_sitefile,yonmoji_pagefile,yonmoji_siteconfig,yonmoji_inputlist,yonmoji_switchlist
    global yonmoji_inputTSV,yonmoji_outputHTML,yonmoji_outputCSS,yonmoji_outputJS,yonmoji_outputXML
    yonmoji_sitefile=LTsv_loadfile(sitename+".tsv")
    if len(yonmoji_sitefile):
        yonmoji_siteconfig=LTsv_getpage(yonmoji_sitefile,"*siteconfig")
        yonmoji_inputTSV=LTsv_readlinerest(yonmoji_siteconfig,"inputTSV","pages/<!pagename!>.tsv")
        yonmoji_outputHTML=LTsv_readlinerest(yonmoji_siteconfig,"outputHTML","../<!pagename!>.html")
        yonmoji_outputCSS=LTsv_readlinerest(yonmoji_siteconfig,"outputCSS","../<!pagename!>.css")
        yonmoji_outputJS=LTsv_readlinerest(yonmoji_siteconfig,"outputJS","../<!pagename!>.js")
        yonmoji_outputXML=LTsv_readlinerest(yonmoji_siteconfig,"outputXML","../<!pagename!>.xml")
        yonmoji_datename=LTsv_readlinerest(yonmoji_siteconfig,"datename","@000y-@0m-@0d")
        yonmoji_datetag=LTsv_readlinerest(yonmoji_siteconfig,"datetag","@000y-@0m")
        yonmoji_inputlist=LTsv_getpage(yonmoji_sitefile,"*inputlist")
    else:
        yonmoji_siteconfig=""
        yonmoji_inputTSV,yonmoji_outputHTML,yonmoji_outputCSS,yonmoji_outputJS,yonmoji_outputXML="pages/<!pagename!>.tsv","../<!pagename!>.html","../<!pagename!>.css","../<!pagename!>.js","../<!pagename!>.xml"
        yonmoji_datename,yonmoji_datetag="@000y-@0m-@0d","@000y-@0m"

def yonmoji_pageload(pagename):
    global yonmoji_sitefile,yonmoji_pagefile,yonmoji_siteconfig,yonmoji_inputlist,yonmoji_switchlist
    yonmoji_pagefile=LTsv_loadfile(yonmoji_inputTSV.replace(yonmoji_pagerename,pagename))

def yonmoji_inputread(inputname):
    global yonmoji_sitefile,yonmoji_pagefile,yonmoji_siteconfig,yonmoji_inputlist,yonmoji_switchlist
    yonmoji_switchlist=LTsv_getpage(yonmoji_sitefile,LTsv_readlinerest(yonmoji_sitefile,inputname))

def yonmoji_switchread(switchname):
    global yonmoji_sitefile,yonmoji_pagefile,yonmoji_siteconfig,yonmoji_inputlist,yonmoji_switchlist
    global yonmoji_input_edit
    yonmoji_case=LTsv_getpage(yonmoji_sitefile,LTsv_readlinerest(yonmoji_switchlist,switchname))
    print(switchname)
    print(yonmoji_case)
    LTsv_widget_settext(yonmoji_input_edit,yonmoji_case)

def yonmoji_column_count(column=yonmoji_column_site):
    if column == yonmoji_column_site:
        yonmoji_entry_T[yonmoji_column_site]=list(set(yonmoji_sitelist.strip('\n').split('\n')))
    if column == yonmoji_column_page:
        yonmoji_path=os.path.normpath(yonmoji_inputTSV.replace(yonmoji_pagerename,"index"))
        LTsv_savedir(yonmoji_path)
        yonmoji_entry_T[yonmoji_column_page]=list(map((lambda pages:os.path.splitext(pages)[0]),os.listdir(os.path.dirname(yonmoji_path))))
    if column == yonmoji_column_input:
        yonmoji_entry_T[yonmoji_column_input]=LTsv_readlinefirsts(yonmoji_inputlist).split('\t')
    if column == yonmoji_column_switch:
        yonmoji_entry_T[yonmoji_column_switch]=LTsv_readlinefirsts(yonmoji_switchlist).split('\t')
    yonmoji_entry_T[column].sort()
    LTsv_scale_adjustment(yonmoji_scale[column],widget_s=0,widget_e=max(len(yonmoji_entry_T[column])-1,0))
    LTsv_scale_adjustment(yonmoji_spin[column],widget_s=0,widget_e=max(len(yonmoji_entry_T[column])-1,0))
    if LTsv_widget_getnumber(yonmoji_scale[column]) >= len(yonmoji_entry_T[column]):
        LTsv_widget_setnumber(yonmoji_scale[column],max(len(yonmoji_entry_T[column])-1,0))
    if LTsv_widget_getnumber(yonmoji_spin[column]) >= len(yonmoji_entry_T[column]):
        LTsv_widget_setnumber(yonmoji_spin[column],max(len(yonmoji_entry_T[column])-1,0))
    LTsv_widget_setnumber(yonmoji_scale[column],0)
    LTsv_widget_setnumber(yonmoji_spin[column],0)
    yonmoji_scale_call[column]()

def yonmoji_entry_shell(column):
    def yonmoji_entry_kernel(callback_void=None,callback_ptr=None):
        entry=LTsv_widget_gettext(yonmoji_entry[column])
        if entry in yonmoji_entry_T[column]:
            LTsv_widget_setnumber(yonmoji_scale[column],yonmoji_entry_T[column].index(entry))
    return yonmoji_entry_kernel

def yonmoji_scale_shell(column):
    def yonmoji_scale_kernel(callback_void=None,callback_ptr=None):
        LTsv_widget_setnumber(yonmoji_spin[column],LTsv_widget_getnumber(yonmoji_scale[column]))
        if len(yonmoji_entry_T[column]):
            LTsv_widget_settext(yonmoji_entry[column],yonmoji_entry_T[column][LTsv_widget_getnumber(yonmoji_scale[column])])
        else:
            LTsv_widget_settext(yonmoji_entry[column],"")
        if column == yonmoji_column_site:
            yonmoji_siteload(LTsv_widget_gettext(yonmoji_entry[yonmoji_column_site]))
            yonmoji_column_count(yonmoji_column_page)
        if column == yonmoji_column_page:
            yonmoji_pageload(LTsv_widget_gettext(yonmoji_entry[yonmoji_column_page]))
            yonmoji_column_count(yonmoji_column_input)
        if column == yonmoji_column_input:
            yonmoji_inputread(LTsv_widget_gettext(yonmoji_entry[yonmoji_column_input]))
            yonmoji_column_count(yonmoji_column_switch)
        if column == yonmoji_column_switch:
            yonmoji_switchread(LTsv_widget_gettext(yonmoji_entry[yonmoji_column_switch]))
    return yonmoji_scale_kernel

def yonmoji_spin_shell(column):
    def yonmoji_spin_kernel(callback_void=None,callback_ptr=None):
        if LTsv_widget_getnumber(yonmoji_scale[column]) != LTsv_widget_getnumber(yonmoji_spin[column]):
            LTsv_widget_setnumber(yonmoji_scale[column],LTsv_widget_getnumber(yonmoji_spin[column]))
    return yonmoji_spin_kernel


LTsv_GUI=LTsv_guiinit()
if len(LTsv_GUI) > 0:
    yonmoji_entry_T=[["site0","siteN"],["psge0","psgeN"],["input0","inputN"],["switch0","switchN"]]
    yonmoji_configload()
    yonmoji_entry_H=yonmoji_fontsize*2; yonmoji_column_H=yonmoji_entry_H*2; yonmoji_column_Y=0
    yonmoji_window=LTsv_window_new(widget_t="yonmoji_ge",event_b=LTsv_window_exit,widget_w=yonmoji_W,widget_h=yonmoji_H)
    yonmoji_label,yonmoji_button,yonmoji_entry,yonmoji_scale,yonmoji_spin=[None]*yonmoji_column_len,[None]*yonmoji_column_len,[None]*yonmoji_column_len,[None]*yonmoji_column_len,[None]*yonmoji_column_len
    yonmoji_scale_call=[None]*yonmoji_column_len
    yonmoji_label_T="site","page(save)","input(memmo)","switch(memo)"
    for column in range(yonmoji_column_len):
        yonmoji_column_Y=yonmoji_column_H*column
        yonmoji_entryID=LTsv_widget_newUUID
        if yonmoji_label_T[column] == "site":
            yonmoji_label[column]=LTsv_label_new(yonmoji_window,widget_t=yonmoji_label_T[column].format(column),widget_x=0,widget_y=yonmoji_column_Y,widget_w=yonmoji_label_W,widget_h=yonmoji_entry_H,widget_f=yonmoji_font)
        else:
            yonmoji_button[column]=LTsv_button_new(yonmoji_window,widget_t=yonmoji_label_T[column].format(column),widget_x=0,widget_y=yonmoji_column_Y,widget_w=yonmoji_label_W,widget_h=yonmoji_entry_H,widget_f=yonmoji_font,event_b=None)
        yonmoji_entry[column]=LTsv_entry_new(yonmoji_window,widget_t=yonmoji_label_T[column],widget_x=0,widget_y=yonmoji_column_Y+yonmoji_entry_H,widget_w=yonmoji_label_W,widget_h=yonmoji_entry_H,widget_f=yonmoji_font,event_b=yonmoji_entry_shell(column))
        yonmoji_scale_call[column]=yonmoji_scale_shell(column)
        yonmoji_scale[column]=LTsv_scale_new(yonmoji_window,widget_x=yonmoji_label_W,widget_y=yonmoji_column_Y,widget_w=yonmoji_entry_W-yonmoji_spin_W,widget_h=yonmoji_column_H,widget_s=0,widget_e=max(len(yonmoji_entry_T[column])-1,0),widget_a=1,event_b=yonmoji_scale_call[column])
        yonmoji_spin[column]=LTsv_spin_new(yonmoji_window,widget_x=yonmoji_W-yonmoji_spin_W,widget_y=yonmoji_column_Y,widget_w=yonmoji_spin_W,widget_h=yonmoji_column_H,widget_s=1,widget_e=max(len(yonmoji_entry_T[column])-1,0),widget_a=1,widget_f=yonmoji_font,event_b=yonmoji_spin_shell(column))
    yonmoji_column_Y=yonmoji_column_H*yonmoji_column_len
    yonmoji_column_Y+=yonmoji_entry_H
    yonmoji_input_edit=LTsv_edit_new(yonmoji_window,widget_t="",widget_x=0,widget_y=yonmoji_column_Y,widget_w=yonmoji_W,widget_h=yonmoji_H-yonmoji_column_Y,widget_f=yonmoji_font)
    LTsv_widget_showhide(yonmoji_window,True)
    yonmoji_column_count()
    LTsv_window_main(yonmoji_window)

