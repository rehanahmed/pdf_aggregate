#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr  1 09:04:43 2025

@author: rahmed
"""

import argparse
import sys
import csv
import os

section_str = '\n\\invisiblesection{%s}\n'
subsection_str = '\\invisiblesubsection{%s}\n'
subsubsection_str = '\\invisiblesubsubsection{%s}\n'

addpdf_str = '\\includepdf[pages=-,rotateoversize, fitpaper]{%s}\n'
addmultipdf_str = '\\includepdf[pages=-,rotateoversize, fitpaper, %s]{%s}\n'
missing_str = '\\Large{%s missing}\\newpage\n'

toccontent_str = '\\addcontentsline{toc}{%s}{%s}\n'

initial_str = '	\\invisiblesection{Title page}\n\
	\\thispagestyle{empty}\
    \\begin{center}\\bf{\Huge{%s}}\\end{center}\n\
    \\vspace{2em}\n\
	\\tableofcontents\n\
	\\vspace*{\\fill}\n\
    \\newpage\n'



latexstring = ''   


class pdffile:
#    def __init__(self, name, section, subsection, subsubsection, note):
    def __init__(self):    
        self.name=None
        self.section=None
        self.subsection=None
        self.subsubsection=None
        self.note=None
    def display(self):
        print('name', self.name, '\nsection', self.section, '\nsubsection', self.subsection, '\nsubsubsection', self.subsubsection, '\nnote', self.note)

section_order= ['section', 'subsection', 'subsubsection']
pdfs_to_add = []

parser = argparse.ArgumentParser(description="Script that accepts either a file or a list of values.")

me_group = parser.add_mutually_exclusive_group(required=True)
op_group = parser.add_argument_group()

me_group.add_argument("-f", "--file", type=str, help="Path to the input csv file. first column has file names, second column onwards have section, subsection, subsubsection")
me_group.add_argument("-l", "--list", nargs='+', help="List of values in the form <pdffile,section,subsection,subsubsection> pdffile is mandatory. rest of the fields are optional")
op_group.add_argument("-t", "--title", type=str , help="The title of the main pdf document")
op_group.add_argument("-n", "--name", type=str , help="The file name of the main pdf document without the extension")

args = parser.parse_args()
file_args = []
if args.file:
    try:
        with open(args.file) as csvfile:
            reader = csv.reader(csvfile, dialect='excel')
            for row in reader:
                file_args.append([v.strip() for v in row])
    except FileNotFoundError:
        print("Error: File not found." + args.file)
        sys.exit(1)
elif args.list:
    for row in args.list:
        file_args.append([v.strip() for v in row.split(',')])
name = args.name.lower().replace('.pdf', '')+'.pdf' if args.name else "combined_doc.pdf"
title = args.title if args.title else ""   
#%%
#filename = 'test.csv'
#with open(filename) as csvfile:
#    reader = csv.reader(csvfile, dialect='excel')
#    for row in reader:
#        file_args.append([v.strip() for v in row])
#%%
# adding the pdffile object in the case where the files exist 
for rnum, row in enumerate(file_args):
    mypdf = pdffile()
    has_note = [i for i,a in enumerate(row) if a.startswith('#')]
    if len(has_note)>0:
        mypdf.note = row[has_note[0]][2:]
        row = [v for i ,v in enumerate(row) if i not in has_note]
    add_file = True    
    for i,v in enumerate(row):
        
        if i> len(section_order):
            print('arguments', row[i:], 'ignored')
            break
        if i==0:
            mypdf.name=v
            if not os.path.isfile(v):
                print('file name %s, which was given as the %dth argument. does not exist. IGNORING'%(mypdf.name, rnum))
                add_file = False
                break
        else:
            setattr(mypdf, section_order[i-1], v)
    if add_file: pdfs_to_add.append(mypdf)
#%%        Getting sections and subsections and the files therein

structure = {}

for pta in pdfs_to_add:
    level=1
    if pta.section not in structure:
        structure[pta.section]={'branch':{}, 'leaves':[]}
    if pta.subsection:
        if pta.subsection not in structure[pta.section]['branch']: 
            structure[pta.section]['branch'][pta.subsection] = {'branch':{}, 'leaves':[]}
        level+=1
        if pta.subsubsection:
            if pta.subsubsection not in structure[pta.section]['branch'][pta.subsection]['branch']: 
                structure[pta.section]['branch'][pta.subsection]['branch'][pta.subsubsection] = {'branch':{}, 'leaves':[]}
            level+=1
    match level:
        case 1:
            structure[pta.section]['leaves'].append({'name':pta.name, 'note':pta.note})
        case 2:
            structure[pta.section]['branch'][pta.subsection]['leaves'].append({'name':pta.name, 'note':pta.note})        
        case 3:
            structure[pta.section]['branch'][pta.subsection]['branch'][pta.subsubsection]['leaves'].append({'name':pta.name, 'note':pta.note})        
        
#%%

latexstring += initial_str%(title)

for key, value in structure.items():
    latexstring += section_str%(key)
    for pdffile in value['leaves']:
        if pdffile['note']: latexstring += toccontent_str%('section',pdffile['note'])
        latexstring += addpdf_str%('../'+pdffile['name'])
        
    for key2, value2 in value['branch'].items():
        latexstring += subsection_str%(key2)
        for pdffile in value2['leaves']:
            if pdffile['note']: latexstring += toccontent_str%('subsection',pdffile['note'])
            latexstring += addpdf_str%('../'+pdffile['name'])
        for key3,value3 in value2['branch']:
            latexstring += subsubsection_str%(key3)
            for pdffile in value3['leaves']:
                if pdffile['note']: latexstring += toccontent_str%('subsubsection',pdffile['note'])
                latexstring += addpdf_str%('../'+pdffile['name'])
            
#%% now tying everything together
os.chdir('latex')
f = open('content.tex', 'w')
f.write(latexstring)
f.close()
os.system('rm *.toc *.pdf *.out *.log *.aux *.gz >/dev/null 2>&1')
os.system('pdflatex document.tex >/dev/null 2>&1')
os.system('pdflatex document.tex >/dev/null 2>&1')
os.system('mv document.pdf ../%s >/dev/null 2>&1'%name)
os.system('rm *.toc *.pdf *.out *.log *.aux *.gz >/dev/null 2>&1')

print(name, 'generated')



        
    




