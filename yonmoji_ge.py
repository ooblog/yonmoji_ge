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

yonmoji_ltsv,yonmoji_config,yonmoji_inputlist="","",""
yonmoji_fontname,yonmoji_fontsize="kantray5x5comic",12; yonmoji_font="{0},{1}".format(yonmoji_fontname,yonmoji_fontsize)
yonmoji_label_W,yonmoji_entry_W,yonmoji_spin_W=150,350,60
yonmoji_W,yonmoji_H=yonmoji_canvasH=yonmoji_label_W+yonmoji_entry_W,yonmoji_fontsize*2
yonmoji_pagenameTAG,yonmoji_pagenames="[pagename]",[]
yonmoji_inputTSV,yonmoji_outputHTML,yonmoji_outputCSS,yonmoji_outputJS,yonmoji_outputXML="pages/[pagename].tsv","../[pagename].html","../[pagename].css","../[pagename].js","../[pagename].xml"
yonmoji_baseHTML,yonmoji_baseCSS,yonmoji_baseJS,yonmoji_baseXML="","","",""
yonmoji_datename,yonmoji_datetag="@000y-@0m-@0dm@@@bt","@000y-@0m"
yonmoji_username="username"

def yonmoji_pageseek(callback_void=None,callback_ptr=None):
    LTsv_widget_settext(yonmoji_save_entry,yonmoji_pagenames[LTsv_widget_getnumber(yonmoji_path_scale)])
    LTsv_widget_setnumber(yonmoji_path_spin,LTsv_widget_getnumber(yonmoji_path_scale))
    yonmoji_pageload(LTsv_widget_gettext(yonmoji_save_entry))

def yonmoji_pageturn(callback_void=None,callback_ptr=None):
    if LTsv_widget_getnumber(yonmoji_path_scale) != LTsv_widget_getnumber(yonmoji_path_spin):
        LTsv_widget_setnumber(yonmoji_path_scale,LTsv_widget_getnumber(yonmoji_path_spin))

def yonmoji_pagepathcheck(pagename):
    LTsv_putdaytimenow()
    pagename_path=re.sub('[/|\\|:|*|?|"|<|>|\|]','-',pagename)
    pagename_path=re.sub('[ ]','_',pagename_path)
    pagename_path=re.sub('\.+','',pagename_path)
    pagename_path=pagename_path if pagename_path != "" else LTsv_getdaytimestr(yonmoji_datename)
    return pagename_path

def yonmoji_pagefind(callback_void=None,callback_ptr=None):
    pagename=LTsv_widget_gettext(yonmoji_save_entry)
    pagename_path=yonmoji_pagepathcheck(pagename)
    if pagename != pagename_path:
        LTsv_widget_settext(yonmoji_save_entry,pagename_path)
    pagename=LTsv_widget_gettext(yonmoji_save_entry)
    if pagename in yonmoji_pagenames:
        LTsv_widget_setnumber(yonmoji_path_scale,yonmoji_pagenames.index(pagename))
    else:
        yonmoji_pageload(pagename)

def yonmoji_pageload(pagename="index"):
    inputlist_file=LTsv_loadfile(yonmoji_inputTSV.replace(yonmoji_pagenameTAG,pagename))
    if len(inputlist_file):
        for yonmoji_inputlist_num in range(yonmoji_inputlist_deno):
            inputlist_page=LTsv_getpage(inputlist_file,yonmoji_label_T[yonmoji_inputlist_num])
            LTsv_widget_settext(yonmoji_entry[yonmoji_inputlist_num],inputlist_page if yonmoji_entry_H[yonmoji_inputlist_num] > 1 else inputlist_page.strip('"\n'))
    else:
        for yonmoji_inputlist_num in range(yonmoji_inputlist_deno):
            inputdef_name,inputdef_case,inputdef_page,inputdef_html="","","",""
            if len(yonmoji_fix[yonmoji_inputlist_num]):
                inputdef_name=yonmoji_fix[yonmoji_inputlist_num]
            if len(yonmoji_def[yonmoji_inputlist_num]):
                inputdef_name=yonmoji_def[yonmoji_inputlist_num]
            if len(yonmoji_var[yonmoji_inputlist_num]):
                inputdef_html=yonmoji_var[yonmoji_inputlist_num]
                inputdef_html=inputdef_html.replace("<!pagename!>",pagename)
                inputdef_html=inputdef_html.replace("<!datename!>",LTsv_getdaytimestr(yonmoji_datename))
                inputdef_html=inputdef_html.replace("<!username!>",yonmoji_username)
            if len(inputdef_html) == 0:
                inputdef_case=LTsv_getpage(yonmoji_ltsv,inputdef_name)
                for inputdef_case_num in range(LTsv_readlinedeno(inputdef_case)):
                     inputdef_case_line=LTsv_readlinenum(inputdef_case,inputdef_case_num)
                     inputdef_case_first=LTsv_readlinefirsts(inputdef_case_line)
                     if inputdef_case_first == pagename or inputdef_case_first == "*":
                          inputdef_page=LTsv_readlinerest(inputdef_case,inputdef_case_first)
                          break
                inputdef_html=LTsv_getpage(yonmoji_ltsv,inputdef_page)
            LTsv_widget_settext(yonmoji_entry[yonmoji_inputlist_num],inputdef_html)

def yonmoji_pagesave(callback_void=None,callback_ptr=None):
    pagename=LTsv_widget_gettext(yonmoji_save_entry)
    pagename_path=yonmoji_pagepathcheck(pagename)
    if pagename != pagename_path:
        LTsv_widget_settext(yonmoji_save_entry,pagename_path)
    pagename=LTsv_widget_gettext(yonmoji_save_entry)
    inputlist_file=LTsv_newfile("yonmoji_ge.tsv")
    inputlist_page=""
    yonmoji_basefile=yonmoji_baseHTML
    for yonmoji_inputlist_num in range(yonmoji_inputlist_deno):
        inputlist_page=LTsv_widget_gettext(yonmoji_entry[yonmoji_inputlist_num])
        inputlist_page=inputlist_page.rstrip('\n')
        yonmoji_basefile=yonmoji_basefile.replace(yonmoji_label_T[yonmoji_inputlist_num],inputlist_page)
        inputlist_page=inputlist_page+"\n" if yonmoji_entry_H[yonmoji_inputlist_num] > 1 else inputlist_page
        inputlist_file=LTsv_putpage(inputlist_file,yonmoji_label_T[yonmoji_inputlist_num],inputlist_page)
    LTsv_savefile(yonmoji_inputTSV.replace(yonmoji_pagenameTAG,pagename),inputlist_file)
    LTsv_saveplain(yonmoji_outputHTML.replace(yonmoji_pagenameTAG,pagename),yonmoji_basefile)
    if not os.path.isfile(yonmoji_outputCSS.replace(yonmoji_pagenameTAG,pagename)):
        LTsv_saveplain(yonmoji_outputCSS.replace(yonmoji_pagenameTAG,pagename),yonmoji_baseCSS)
    if not os.path.isfile(yonmoji_outputJS.replace(yonmoji_pagenameTAG,pagename)):
        LTsv_saveplain(yonmoji_outputJS.replace(yonmoji_pagenameTAG,pagename),yonmoji_baseJS)
    if not os.path.isfile(yonmoji_outputXML.replace(yonmoji_pagenameTAG,pagename)):
        LTsv_saveplain(yonmoji_outputXML.replace(yonmoji_pagenameTAG,pagename),yonmoji_baseXML)
    yonmoji_pagescount(pagename)

def yonmoji_pagescount(pagename):
    global yonmoji_pagenameTAG,yonmoji_pagenames
    yonmoji_pagenames=list(map((lambda path:os.path.splitext(path)[0]),os.listdir(os.path.dirname(yonmoji_inputTSV.replace(yonmoji_pagenameTAG,pagename)))))
    yonmoji_pagenames=list(set(yonmoji_pagenames)); yonmoji_pagenames.sort()
    LTsv_scale_adjustment(yonmoji_path_spin,widget_s=0,widget_e=max(len(yonmoji_pagenames)-1,0))
    LTsv_scale_adjustment(yonmoji_path_scale,widget_s=0,widget_e=max(len(yonmoji_pagenames)-1,0))
    if LTsv_widget_gettext(yonmoji_save_entry) in yonmoji_pagenames:
        LTsv_widget_setnumber(yonmoji_path_scale,yonmoji_pagenames.index(LTsv_widget_gettext(yonmoji_save_entry)))
    else:
        LTsv_widget_setnumber(yonmoji_path_scale,max(len(yonmoji_pagenames)-1,0))
        LTsv_widget_setnumber(yonmoji_path_spin,LTsv_widget_getnumber(yonmoji_path_scale))

def yonmoji_configload():
    global yonmoji_ltsv,yonmoji_config,yonmoji_inputlist,yonmoji_basehtml
    global yonmoji_fontname,yonmoji_fontsize
    global yonmoji_pagenameTAG,yonmoji_pagenames
    global yonmoji_inputTSV,yonmoji_outputHTML,yonmoji_outputCSS,yonmoji_outputJS,yonmoji_outputXML
    global yonmoji_baseHTML,yonmoji_baseCSS,yonmoji_baseJS,yonmoji_baseXML
    global yonmoji_datename,yonmoji_datetag
    global yonmoji_username
    yonmoji_ltsv=LTsv_loadfile("yonmoji_ge.tsv")
    yonmoji_config=LTsv_getpage(yonmoji_ltsv,"yonmoji_ge")
    yonmoji_fontname=LTsv_readlinerest(yonmoji_config,"font_name",yonmoji_fontname)
    yonmoji_fontsize=min(max(LTsv_intstr0x(LTsv_readlinerest(yonmoji_config,"font_size")),5),20)
    yonmoji_font="{0},{1}".format(yonmoji_fontname,yonmoji_fontsize)
    yonmoji_pagenameTAG=LTsv_readlinerest(yonmoji_config,"pagename",yonmoji_pagenameTAG)
    yonmoji_inputTSV=LTsv_readlinerest(yonmoji_config,"inputTSV",yonmoji_inputTSV)
    if not os.path.isdir(os.path.dirname(yonmoji_inputTSV.replace(yonmoji_pagenameTAG,"index"))): os.mkdir(os.path.dirname(yonmoji_inputTSV.replace(yonmoji_pagenameTAG,"index")))
    yonmoji_outputHTML=LTsv_readlinerest(yonmoji_config,"outputHTML",yonmoji_outputHTML)
    yonmoji_outputCSS=LTsv_readlinerest(yonmoji_config,"outputCSS",yonmoji_outputCSS)
    yonmoji_outputJS=LTsv_readlinerest(yonmoji_config,"outputJS",yonmoji_outputJS)
    yonmoji_outputXML=LTsv_readlinerest(yonmoji_config,"outputXML",yonmoji_outputXML)
    yonmoji_datename=LTsv_readlinerest(yonmoji_config,"datename",yonmoji_datename)
    yonmoji_datetag=LTsv_readlinerest(yonmoji_config,"datetag",yonmoji_datetag)
    yonmoji_inputlist=LTsv_getpage(yonmoji_ltsv,"inputlist")
    yonmoji_baseHTML=LTsv_getpage(yonmoji_ltsv,"baseHTML")
    yonmoji_baseCSS=LTsv_getpage(yonmoji_ltsv,"baseCSS")
    yonmoji_baseJS=LTsv_getpage(yonmoji_ltsv,"baseJS")
    yonmoji_baseXML=LTsv_getpage(yonmoji_ltsv,"baseXML")
    yonmoji_username=LTsv_readlinerest(yonmoji_config,"username",yonmoji_username)

def yonmoji_exit_configsave(window_objvoid=None,window_objptr=None):
    LTsv_window_exit()

LTsv_GUI=LTsv_guiinit()
if len(LTsv_GUI) > 0:
    yonmoji_configload()
    yonmoji_inputlist_deno=LTsv_readlinedeno(yonmoji_inputlist)
    yonmoji_label,yonmoji_label_Y,yonmoji_label_T,yonmoji_entry,yonmoji_entry_H=[None]*yonmoji_inputlist_deno,[None]*yonmoji_inputlist_deno,[None]*yonmoji_inputlist_deno,[None]*yonmoji_inputlist_deno,[None]*yonmoji_inputlist_deno
    yonmoji_def,yonmoji_fix,yonmoji_var=[None]*yonmoji_inputlist_deno,[None]*yonmoji_inputlist_deno,[None]*yonmoji_inputlist_deno
    yonmoji_curcor_Y=2
    for yonmoji_inputlist_num in range(yonmoji_inputlist_deno):
        yonmoji_inputlist_line=LTsv_readlinenum(yonmoji_inputlist,yonmoji_inputlist_num)
        yonmoji_label_T[yonmoji_inputlist_num]=LTsv_readlinefirsts(yonmoji_inputlist_line)
        yonmoji_entry_H[yonmoji_inputlist_num]=min(max(LTsv_intstr0x(LTsv_pickdatalabel(yonmoji_inputlist_line,"size")),1),9)
        yonmoji_def[yonmoji_inputlist_num]=LTsv_pickdatalabel(yonmoji_inputlist_line,"def")
        yonmoji_fix[yonmoji_inputlist_num]=LTsv_pickdatalabel(yonmoji_inputlist_line,"fix")
        yonmoji_var[yonmoji_inputlist_num]=LTsv_pickdatalabel(yonmoji_inputlist_line,"var")
        yonmoji_label_Y[yonmoji_inputlist_num]=yonmoji_curcor_Y
        yonmoji_curcor_Y+=yonmoji_entry_H[yonmoji_inputlist_num]
    yonmoji_H=yonmoji_curcor_Y*yonmoji_fontsize*2
    yonmoji_window=LTsv_window_new(widget_t="yonmoji_ge",event_b=LTsv_window_exit,widget_w=yonmoji_W,widget_h=yonmoji_H)
    for yonmoji_inputlist_num in range(yonmoji_inputlist_deno):
        yonmoji_label[yonmoji_inputlist_num]=LTsv_label_new(yonmoji_window,widget_t=yonmoji_label_T[yonmoji_inputlist_num],widget_x=0,widget_y=yonmoji_label_Y[yonmoji_inputlist_num]*yonmoji_fontsize*2,widget_w=yonmoji_label_W,widget_h=yonmoji_entry_H[yonmoji_inputlist_num]*yonmoji_fontsize*2,widget_f=yonmoji_font)
        if yonmoji_entry_H[yonmoji_inputlist_num] > 1:
            yonmoji_entry[yonmoji_inputlist_num]=LTsv_edit_new(yonmoji_window,widget_t="",widget_x=yonmoji_label_W,widget_y=yonmoji_label_Y[yonmoji_inputlist_num]*yonmoji_fontsize*2,widget_w=yonmoji_entry_W,widget_h=yonmoji_entry_H[yonmoji_inputlist_num]*yonmoji_fontsize*2,widget_f=yonmoji_font)
        else:
            yonmoji_entry[yonmoji_inputlist_num]=LTsv_entry_new(yonmoji_window,widget_t="",widget_x=yonmoji_label_W,widget_y=yonmoji_label_Y[yonmoji_inputlist_num]*yonmoji_fontsize*2,widget_w=yonmoji_entry_W,widget_h=yonmoji_entry_H[yonmoji_inputlist_num]*yonmoji_fontsize*2,widget_f=yonmoji_font)
        LTsv_widget_disableenable(yonmoji_entry[yonmoji_inputlist_num],False if len(yonmoji_fix[yonmoji_inputlist_num]) else True)
    yonmoji_save_button=LTsv_button_new(yonmoji_window,widget_t="save",widget_x=0,widget_y=0,widget_w=yonmoji_label_W,widget_h=yonmoji_fontsize*2,widget_f=yonmoji_font,event_b=yonmoji_pagesave)
    yonmoji_save_entry=LTsv_entry_new(yonmoji_window,widget_t="index",widget_x=0,widget_y=yonmoji_fontsize*2,widget_w=yonmoji_label_W,widget_h=yonmoji_fontsize*2,widget_f=yonmoji_font,event_b=yonmoji_pagefind)
    yonmoji_path_scale=LTsv_scale_new(yonmoji_window,widget_x=yonmoji_label_W,widget_y=0,widget_w=yonmoji_entry_W-yonmoji_spin_W,widget_h=yonmoji_fontsize*2*2,widget_s=0,widget_e=4,widget_a=1,event_b=yonmoji_pageseek)
    yonmoji_path_spin=LTsv_spin_new(yonmoji_window,widget_x=yonmoji_W-yonmoji_spin_W,widget_y=0,widget_w=yonmoji_spin_W,widget_h=yonmoji_fontsize*2*2,widget_s=1,widget_e=4,widget_a=1,widget_f=yonmoji_font,event_b=yonmoji_pageturn)
    LTsv_widget_showhide(yonmoji_window,True)
    yonmoji_pagescount("index")
    yonmoji_pageload("index")
    LTsv_window_main(yonmoji_window)


# Copyright (c) 2016 ooblog
# License: MIT
# https://github.com/ooblog/LTsv9yonmoji/blob/master/LICENSE


