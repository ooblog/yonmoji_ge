#! /usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import division,print_function,absolute_import,unicode_literals
import sys
import os
import re
os.chdir(sys.path[0])
sys.path.append("LTsv")
from LTsv_printf import *
from LTsv_file   import *
from LTsv_time   import *
#from LTsv_calc   import *
#from LTsv_joy    import *
#from LTsv_kbd    import *
from LTsv_gui    import *

yonmoji_ltsv,yonmoji_config,yonmoji_sitelist="","",""
yonmoji_fontname,yonmoji_fontsize="kantray5x5comic",10; yonmoji_font="{0},{1}".format(yonmoji_fontname,yonmoji_fontsize)
yonmoji_sitefile,yonmoji_pagefile,yonmoji_siteconfig,yonmoji_rewritelist,yonmoji_switchlist="","","","",""
yonmoji_column_len=3; yonmoji_column_site,yonmoji_column_page,yonmoji_column_rewrite=0,1,2
yonmoji_label_W,yonmoji_entry_W,yonmoji_spin_W=200,530,70
yonmoji_W,yonmoji_H=yonmoji_label_W+yonmoji_entry_W,600
yonmoji_username="ooblog"
yonmoji_pagetime,yonmoji_rewritetime="@0h:@0n:@0s","@0h:@0n:@0s"
yonmoji_pagerename,yonmoji_datarename,yonmoji_userrename="<!pagename!>","<!datename!>","<!username!>"
yonmoji_rewriteTSV,yonmoji_outputHTML,yonmoji_outputCSS,yonmoji_outputJS,yonmoji_outputSEARCH="pages/<!pagename!>.tsv","../<!pagename!>.html","../<!pagename!>.css","../<!pagename!>.js","../<!pagename!>.xml"
yonmoji_datename="@000y-@0m-@0dm"

def yonmoji_configload():
    global yonmoji_ltsv,yonmoji_config,yonmoji_sitelist
    global yonmoji_font,yonmoji_fontname,yonmoji_fontsize
    global yonmoji_username
    global yonmoji_pagetime,yonmoji_rewritetime
    yonmoji_ltsv=LTsv_loadfile("yonmoji_ge.tsv")
    yonmoji_config=LTsv_getpage(yonmoji_ltsv,"yonmoji_ge")
    yonmoji_fontname=LTsv_readlinerest(yonmoji_config,"fontname",yonmoji_fontname)
    yonmoji_fontsize=min(max(LTsv_intstr0x(LTsv_readlinerest(yonmoji_config,"fontsize")),5),20)
    yonmoji_font="{0},{1}".format(yonmoji_fontname,yonmoji_fontsize)
    yonmoji_sitelist=LTsv_getpage(yonmoji_ltsv,"sitelist")
    yonmoji_username=LTsv_readlinerest(yonmoji_config,"username",yonmoji_username)
    yonmoji_pagetime=LTsv_readlinerest(yonmoji_config,"pagetime",yonmoji_pagetime)
    yonmoji_rewritetime=LTsv_readlinerest(yonmoji_config,"rewritetime",yonmoji_rewritetime)
    yonmoji_entry_T[yonmoji_column_site]=list(yonmoji_sitelist.strip('\n').split('\n'))

def yonmoji_siteload(sitename):
    global yonmoji_sitefile,yonmoji_pagefile,yonmoji_siteconfig,yonmoji_rewritelist,yonmoji_switchlist
    global yonmoji_rewriteTSV,yonmoji_outputHTML,yonmoji_outputCSS,yonmoji_outputJS,yonmoji_outputSEARCH
    global yonmoji_datename
    yonmoji_sitefile=LTsv_loadfile(sitename+".tsv")
    if len(yonmoji_sitefile):
        yonmoji_siteconfig=LTsv_getpage(yonmoji_sitefile,"*siteconfig")
        yonmoji_rewriteTSV=LTsv_readlinerest(yonmoji_siteconfig,"rewriteTSV","pages/<!pagename!>.tsv")
        yonmoji_outputHTML=LTsv_readlinerest(yonmoji_siteconfig,"outputHTML","../<!pagename!>.html")
        yonmoji_outputCSS=LTsv_readlinerest(yonmoji_siteconfig,"outputCSS","../<!pagename!>.css")
        yonmoji_outputJS=LTsv_readlinerest(yonmoji_siteconfig,"outputJS","../<!pagename!>.js")
        yonmoji_outputSEARCH=LTsv_readlinerest(yonmoji_siteconfig,"outputSEARCH","../<!pagename!>.xml")
        yonmoji_datename=LTsv_readlinerest(yonmoji_siteconfig,"datename","@000y-@0m-@0dm")
        yonmoji_rewritelist=LTsv_getpage(yonmoji_sitefile,"*rewritelist")
        yonmoji_path=os.path.normpath(yonmoji_rewriteTSV.replace(yonmoji_pagerename,"index"))
        LTsv_savedir(yonmoji_path)
        yonmoji_entry_T[yonmoji_column_page]=list(map((lambda pages:os.path.splitext(pages)[0]),os.listdir(os.path.dirname(yonmoji_path))))
        if len(yonmoji_entry_T[yonmoji_column_page]) == 0:
            yonmoji_entry_T[yonmoji_column_page] =["index"]
        yonmoji_entry_T[yonmoji_column_rewrite]=LTsv_readlinefirsts(yonmoji_rewritelist).split('\t')
    else:
        yonmoji_siteconfig=""
        yonmoji_rewriteTSV,yonmoji_outputHTML,yonmoji_outputCSS,yonmoji_outputJS,yonmoji_outputSEARCH="pages/<!pagename!>.tsv","../<!pagename!>.html","../<!pagename!>.css","../<!pagename!>.js","../<!pagename!>.xml"
        yonmoji_datename="@000y-@0m-@0dm"
        yonmoji_rewritelist=""
        yonmoji_entry_T[yonmoji_column_page]=[]
        yonmoji_entry_T[yonmoji_column_rewrite]=[]

def yonmoji_pageload(pagename):
    global yonmoji_sitefile,yonmoji_pagefile,yonmoji_siteconfig,yonmoji_rewritelist,yonmoji_switchlist
    global yonmoji_rewriteTSV,yonmoji_outputHTML,yonmoji_outputCSS,yonmoji_outputJS,yonmoji_outputSEARCH
    yonmoji_pagefile=LTsv_loadfile(yonmoji_rewriteTSV.replace(yonmoji_pagerename,pagename))
    if len(yonmoji_pagefile) == 0 and len(yonmoji_sitefile) > 0:
        yonmoji_pagefile=LTsv_newfile("yonmoji_ge.tsv")
        for yonmoji_rewrite in yonmoji_entry_T[yonmoji_column_rewrite]:
            rewrite_name=LTsv_readlinerest(yonmoji_rewritelist,yonmoji_rewrite)
            rewrite_casedata=LTsv_getpage(yonmoji_sitefile,rewrite_name)
            rewrite_pagedata=""
            if len(rewrite_casedata) == 0:
                rewrite_pagedata=rewrite_name
            else:
                rewrite_cases=rewrite_casedata.split('\n')
                for rewrite_case in rewrite_cases:
                    rewrite_case_first=LTsv_readlinefirsts(rewrite_case)
                    rewrite_research=None
                    try:
                        rewrite_research=re.search(re.compile(rewrite_case_first),pagename)
                    except re.error:
                        print("re.error",rewrite_case_first)
                        break
                    else:
                        if rewrite_research:
                            rewrite_pagedata=LTsv_getpage(yonmoji_sitefile,LTsv_readlinerest(rewrite_case,rewrite_case_first))
                            break
            yonmoji_pagefile=LTsv_putpage(yonmoji_pagefile,yonmoji_rewrite,rewrite_pagedata)
    yonmoji_rewriteread(LTsv_widget_gettext(yonmoji_entry[yonmoji_column_rewrite]))
    LTsv_widget_settext(yonmoji_button[yonmoji_column_page],yonmoji_label_T[yonmoji_column_page])

def yonmoji_rewriteread(rewritename):
    global yonmoji_sitefile,yonmoji_pagefile,yonmoji_siteconfig,yonmoji_rewritelist,yonmoji_switchlist
    yonmoji_switchlist=LTsv_getpage(yonmoji_sitefile,LTsv_readlinerest(yonmoji_sitefile,rewritename))
    rewrite_text=""
    if len(yonmoji_sitefile) > 0:
        pagename=LTsv_widget_gettext(yonmoji_entry[yonmoji_column_rewrite])
        if pagename in yonmoji_entry_T[yonmoji_column_rewrite]:
            rewrite_text=LTsv_getpage(yonmoji_pagefile,yonmoji_entry_T[yonmoji_column_rewrite][yonmoji_entry_T[yonmoji_column_rewrite].index(pagename)])
    LTsv_widget_settext(yonmoji_rewrite_edit,rewrite_text)
    LTsv_widget_settext(yonmoji_button[yonmoji_column_rewrite],yonmoji_label_T[yonmoji_column_rewrite])

def yonmoji_column_count(column=yonmoji_column_site):
    LTsv_scale_adjustment(yonmoji_scale[column],widget_s=0,widget_e=max(len(yonmoji_entry_T[column])-1,0))
    LTsv_scale_adjustment(yonmoji_spin[column],widget_s=0,widget_e=max(len(yonmoji_entry_T[column])-1,0))
    LTsv_widget_disableenable(yonmoji_button[yonmoji_column_page],True if len(yonmoji_rewritelist) > 0 else False)
    LTsv_widget_disableenable(yonmoji_button[yonmoji_column_rewrite],True if len(yonmoji_rewritelist) > 0 else False)
    if column == yonmoji_column_site:
        LTsv_widget_setnumber(yonmoji_scale[column],0)
        LTsv_widget_setnumber(yonmoji_spin[column],0)
    else:
        if LTsv_widget_getnumber(yonmoji_scale[column]) >= len(yonmoji_entry_T[column]):
            LTsv_widget_setnumber(yonmoji_scale[column],max(len(yonmoji_entry_T[column])-1,0))
        if LTsv_widget_getnumber(yonmoji_spin[column]) >= len(yonmoji_entry_T[column]):
            LTsv_widget_setnumber(yonmoji_spin[column],max(len(yonmoji_entry_T[column])-1,0))
    yonmoji_scale_call[column]()

def yonmoji_entry_shell(column):
    def yonmoji_entry_kernel(callback_void=None,callback_ptr=None):
        entry=LTsv_widget_gettext(yonmoji_entry[column])
        if entry in yonmoji_entry_T[column]:
            LTsv_widget_setnumber(yonmoji_scale[column],yonmoji_entry_T[column].index(entry))
        else:
            yonmoji_column_count(column)
            if column == yonmoji_column_page:
                entry=yonmoji_pathcheck(entry)
                LTsv_widget_settext(yonmoji_entry[yonmoji_column_page],entry)
                yonmoji_pageload(LTsv_widget_gettext(yonmoji_entry[yonmoji_column_page]))
    return yonmoji_entry_kernel

def yonmoji_pathcheck(path):
    LTsv_putdaytimenow()
    yonmoji_path=re.sub('[/|\\|:|*|?|"|<|>|\|]','',path)
    yonmoji_path=re.sub('[ ]','',yonmoji_path)
    yonmoji_path=re.sub('\.+','',yonmoji_path)
    yonmoji_path=yonmoji_path if yonmoji_path != "" else LTsv_getdaytimestr(yonmoji_datename)
    return yonmoji_path

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
            yonmoji_column_count(yonmoji_column_rewrite)
        if column == yonmoji_column_rewrite:
            yonmoji_rewriteread(LTsv_widget_gettext(yonmoji_entry[yonmoji_column_rewrite]))
    return yonmoji_scale_kernel

def yonmoji_spin_shell(column):
    def yonmoji_spin_kernel(callback_void=None,callback_ptr=None):
        if LTsv_widget_getnumber(yonmoji_scale[column]) != LTsv_widget_getnumber(yonmoji_spin[column]):
            LTsv_widget_setnumber(yonmoji_scale[column],LTsv_widget_getnumber(yonmoji_spin[column]))
    return yonmoji_spin_kernel

def yonmoji_button_shell(column):
    def yonmoji_button_kernel(callback_void=None,callback_ptr=None):
        global yonmoji_sitefile,yonmoji_pagefile,yonmoji_siteconfig,yonmoji_rewritelist,yonmoji_switchlist
        global yonmoji_pagerename,yonmoji_datarename,yonmoji_userrename
        if column == yonmoji_column_page:
            LTsv_putdaytimenow()
            entry=LTsv_widget_gettext(yonmoji_entry[yonmoji_column_page])
            entry=yonmoji_pathcheck(entry)
            LTsv_widget_settext(yonmoji_entry[yonmoji_column_page],entry)
            yonmoji_baseHTML=LTsv_getpage(yonmoji_sitefile,"baseHTML")
            for yonmoji_rewrite in yonmoji_entry_T[yonmoji_column_rewrite]:
                rewrite_text=LTsv_getpage(yonmoji_pagefile,yonmoji_rewrite)
                yonmoji_baseHTML=yonmoji_baseHTML.replace(yonmoji_rewrite,rewrite_text.rstrip('\n'))
            yonmoji_baseHTML=yonmoji_rename(yonmoji_baseHTML)
            LTsv_saveplain(yonmoji_rename(yonmoji_outputHTML),yonmoji_baseHTML)
            LTsv_widget_settext(yonmoji_button[yonmoji_column_page],LTsv_getdaytimestr("rewrite({0})".format(yonmoji_pagetime)))
            yonmoji_baseCSS=LTsv_getpage(yonmoji_sitefile,"baseCSS")
            if len(yonmoji_baseCSS):
                if not os.path.isfile(yonmoji_rename(yonmoji_outputCSS)):
                    LTsv_saveplain(yonmoji_rename(yonmoji_outputCSS),yonmoji_baseCSS)
            yonmoji_baseJS=LTsv_getpage(yonmoji_sitefile,"baseJS")
            if len(yonmoji_baseJS):
                if not os.path.isfile(yonmoji_rename(yonmoji_outputJS)):
                    LTsv_saveplain(yonmoji_rename(yonmoji_outputJS),yonmoji_baseJS)
            yonmoji_baseSEARCH=LTsv_getpage(yonmoji_sitefile,"baseSEARCH")
            if len(yonmoji_baseSEARCH):
                if not os.path.isfile(yonmoji_rename(yonmoji_outputSEARCH)):
                    LTsv_saveplain(yonmoji_rename(yonmoji_outputSEARCH),yonmoji_baseSEARCH)
        if column == yonmoji_column_rewrite:
            yonmoji_pagefile=LTsv_putpage(yonmoji_pagefile,yonmoji_entry_T[yonmoji_column_rewrite][LTsv_widget_getnumber(yonmoji_scale[yonmoji_column_rewrite])],LTsv_widget_gettext(yonmoji_rewrite_edit))
            LTsv_savefile(yonmoji_rename(yonmoji_rewriteTSV),yonmoji_pagefile)
            LTsv_widget_settext(yonmoji_button[yonmoji_column_rewrite],LTsv_getdaytimestr("rewrite({0})".format(yonmoji_rewritetime)))
    return yonmoji_button_kernel

def yonmoji_rename(name):
    LTsv_putdaytimenow()
    yonmoji_name=name
    yonmoji_name=yonmoji_name.replace(yonmoji_pagerename,LTsv_widget_gettext(yonmoji_entry[yonmoji_column_page]))
    yonmoji_name=yonmoji_name.replace(yonmoji_datarename,LTsv_getdaytimestr(yonmoji_datename))
    yonmoji_name=yonmoji_name.replace(yonmoji_userrename,yonmoji_username)
    return yonmoji_name

LTsv_GUI=LTsv_guiinit()
if len(LTsv_GUI) > 0:
    yonmoji_entry_T=[["site0","siteN"],["psge0","psgeN"],["rewrite0","rewriteN"]]
    yonmoji_configload()
    yonmoji_entry_H=yonmoji_fontsize*2; yonmoji_column_H=yonmoji_entry_H*2; yonmoji_column_Y=0
    yonmoji_window=LTsv_window_new(widget_t="yonmoji_ge",event_b=LTsv_window_exit,widget_w=yonmoji_W,widget_h=yonmoji_H)
    yonmoji_label,yonmoji_button,yonmoji_entry,yonmoji_scale,yonmoji_spin=[None]*yonmoji_column_len,[None]*yonmoji_column_len,[None]*yonmoji_column_len,[None]*yonmoji_column_len,[None]*yonmoji_column_len
    yonmoji_scale_call=[None]*yonmoji_column_len
    yonmoji_label_T="site","page(HTML)","rewrite(TSV)"
    for column in range(yonmoji_column_len):
        yonmoji_column_Y=yonmoji_column_H*column
        yonmoji_entryID=LTsv_widget_newUUID
        if yonmoji_label_T[column] == "site":
            yonmoji_label[column]=LTsv_label_new(yonmoji_window,widget_t=yonmoji_label_T[column].format(column),widget_x=0,widget_y=yonmoji_column_Y,widget_w=yonmoji_label_W,widget_h=yonmoji_entry_H,widget_f=yonmoji_font)
        else:
            yonmoji_button[column]=LTsv_button_new(yonmoji_window,widget_t=yonmoji_label_T[column].format(column),widget_x=0,widget_y=yonmoji_column_Y,widget_w=yonmoji_label_W,widget_h=yonmoji_entry_H,widget_f=yonmoji_font,event_b=yonmoji_button_shell(column))
        yonmoji_entry[column]=LTsv_entry_new(yonmoji_window,widget_t=yonmoji_label_T[column],widget_x=0,widget_y=yonmoji_column_Y+yonmoji_entry_H,widget_w=yonmoji_label_W,widget_h=yonmoji_entry_H,widget_f=yonmoji_font,event_b=yonmoji_entry_shell(column))
        yonmoji_scale_call[column]=yonmoji_scale_shell(column)
        yonmoji_scale[column]=LTsv_scale_new(yonmoji_window,widget_x=yonmoji_label_W,widget_y=yonmoji_column_Y,widget_w=yonmoji_entry_W-yonmoji_spin_W,widget_h=yonmoji_column_H,widget_s=0,widget_e=max(len(yonmoji_entry_T[column])-1,0),widget_a=1,event_b=yonmoji_scale_call[column])
        yonmoji_spin[column]=LTsv_spin_new(yonmoji_window,widget_x=yonmoji_W-yonmoji_spin_W,widget_y=yonmoji_column_Y,widget_w=yonmoji_spin_W,widget_h=yonmoji_column_H,widget_s=1,widget_e=max(len(yonmoji_entry_T[column])-1,0),widget_a=1,widget_f=yonmoji_font,event_b=yonmoji_spin_shell(column))
    yonmoji_column_Y=yonmoji_column_H*yonmoji_column_len
    yonmoji_rewrite_edit=LTsv_edit_new(yonmoji_window,widget_t="",widget_x=0,widget_y=yonmoji_column_Y,widget_w=yonmoji_W,widget_h=yonmoji_H-yonmoji_column_Y,widget_f=yonmoji_font)
    LTsv_widget_showhide(yonmoji_window,True)
    yonmoji_column_count(yonmoji_column_site)
    LTsv_window_main(yonmoji_window)


# Copyright (c) 2016 ooblog
# License: MIT
# https://github.com/ooblog/LTsv9kantray/blob/master/LICENSE
