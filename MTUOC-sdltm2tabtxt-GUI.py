#    MTUOC-sdltm2tabtxt-GUI
#    Copyright (C) 2022  Antoni Oliver
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.

#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <https://www.gnu.org/licenses/>.


from tkinter import *
from tkinter.ttk import *

import tkinter 
from tkinter.filedialog import askopenfilename
from tkinter.filedialog import asksaveasfilename
from tkinter.filedialog import askdirectory
from tkinter import messagebox
from tkinter import ttk

import sys
import sqlite3
import xml.etree.ElementTree as etree
import codecs
import os
import argparse

import html
import re

from ftfy import fix_encoding

###
def lreplace(pattern, sub, string):
    """
    Replaces 'pattern' in 'string' with 'sub' if 'pattern' starts 'string'.
    """
    return re.sub('^%s' % pattern, sub, string)

def rreplace(pattern, sub, string):
    """
    Replaces 'pattern' in 'string' with 'sub' if 'pattern' ends 'string'.
    """
    return re.sub('%s$' % pattern, sub, string)
    
def FT2ST(segment):
    segmenttagsimple=segment
    segmenttagsimple=re.sub('(<[^>]+?/>)', "<t/>",segmenttagsimple)
    segmenttagsimple=re.sub('(</[^>]+?>)', "</t>",segmenttagsimple)
    segmenttagsimple=re.sub('(<[^/>]+?>)', "<t>",segmenttagsimple)
    return(segmenttagsimple)
    
def FT2NT(segment):
    segmentnotags=re.sub('(<[^>]+>)', " ",segment)
    segmentnotags=' '.join(segmentnotags.split()).strip()
    return(segmentnotags)
    
def sdltm2tabtxt(sdltmfile, fsortida):
    try:
        CBnotagsState=CBnotags.state()
        argsnoTags=False
        if "selected" in CBnotagsState:
            argsnoTags=True
        CBsimpletagsState=CBsimpletags.state()
        argssimpleTags=False
        if "selected" in CBsimpletagsState and not argsnoTags:
            argssimpleTags=True
        CBnoentitiesState=CBnoentities.state()
        argsnoEntities=False
        if "selected" in CBnoentitiesState:
            argsnoEntities=True
        CBfixencodingState=CBfixencoding.state()
        argsfixencoding=False
        if "selected" in CBfixencodingState:
            argsfixencoding=True    
        sortida=codecs.open(fsortida,"w",encoding="utf-8")
        conn=sqlite3.connect(sdltmfile)
        cur = conn.cursor() 
        cur.execute('select source_segment,target_segment from translation_units;')
        data=cur.fetchall()
        for d in data:
            ssxml=d[0]
            tsxml=d[1]
            try:
                rootSL = etree.fromstring(ssxml)
                for text in rootSL.iter('Value'):
                    sltext="".join(text.itertext()).replace("\n"," ")
                rootTL = etree.fromstring(tsxml)
                for text in rootTL.iter('Value'):
                    tltext="".join(text.itertext()).replace("\n"," ")
                if not sltext=="" and not tltext=="":
                    if argsnoEntities:
                        sltext=html.unescape(sltext)
                        tltext=html.unescape(tltext)
                    if argssimpleTags:
                        sltext=FT2ST(sltext)
                        tltext=FT2ST(tltext)
                    if argsnoTags:
                        sltext=FT2NT(sltext)
                        tltext=FT2NT(tltext)
                    if argsfixencoding:
                        sltext=fix_encoding(sltext)
                        tltext=fix_encoding(tltext)
                    cadena=sltext+"\t"+tltext
                    print(cadena)
                    sortida.write(cadena+"\n")
            except:
                print("ERROR",sys.exc_info())
    except:
        pass          
    sortida.close()
###

def select_corpus():
    infile = askopenfilename(initialdir = ".",filetypes =(("SDLTM files", ["*.sdltm"]),("All Files","*.*")),title = "Choose an input file.")
    E1.delete(0,END)
    E1.insert(0,infile)
    E1.xview_moveto(1)
    
def select_output_file():
    outfile = asksaveasfilename(initialdir = ".",filetypes =(("text files", ["*.txt"]),("All Files","*.*")),
                           title = "Choose a output file to store the term candidates.")
    E2.delete(0,END)
    E2.insert(0,outfile)
    E2.xview_moveto(1)
    
def go():
    sdltmfile=E1.get()
    fsortida=E2.get()
    sdltm2tabtxt(sdltmfile, fsortida)


top = Tk()
top.title("MTUOC-sdltm2tabtxt-GUI")

B1=tkinter.Button(top, text = str("Input file"), borderwidth = 1, command=select_corpus,width=14).grid(row=0,column=0)
E1 = tkinter.Entry(top, bd = 5, width=50, justify="right")
E1.grid(row=0,column=1)

B2=tkinter.Button(top, text = str("Output file"), borderwidth = 1, command=select_output_file,width=14).grid(row=1,column=0)
E2 = tkinter.Entry(top, bd = 5, width=50, justify="right")
E2.grid(row=1,column=1)

CBnotags=ttk.Checkbutton(top, text="No tags")
CBnotags.state(['!alternate']) 
CBnotags.grid(sticky="W",row=2,column=0)
CBsimpletags=ttk.Checkbutton(top, text="Simple tags")
CBsimpletags.state(['!alternate']) 
CBsimpletags.grid(sticky="W",row=3,column=0)
CBnoentities=ttk.Checkbutton(top, text="No entities")
CBnoentities.state(['!alternate']) 
CBnoentities.grid(sticky="W",row=4,column=0)
CBfixencoding=ttk.Checkbutton(top, text="Fix encoding")
CBfixencoding.state(['!alternate']) 
CBfixencoding.grid(sticky="W",row=5,column=0)




B5=tkinter.Button(top, text = str("Go!"), borderwidth = 1, command=go,width=14).grid(sticky="W",row=6,column=0)

top.mainloop()
