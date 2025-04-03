## PDF Aggregator

I am often stuck with several pdfs without lack of a convenient tool to organize them. What I needed was a tool which could create bookmarks and auto-generate a table of contents. This is what the pdf aggregator does. 

You have the capability to organize your pdfs in sections, subsections, and subsubsections. Optionally, you can add a note to a given pdf. This note appears in the generated table of contents.

### Dependencies

- Ubuntu or a similar Unix based OS
- pdflatex with following packages installed: {pdfpages, geometry,hyperref,pdflscape}
- python3 with the following packages installed: {argparase, sys, os, csv}


### Usage

One of the following arguments are mandatory:

- "-f" a csv file with each row specifying <pdffile\>,<section\>,<subsection\>,<subsubsection\>,<#nnote_text\>. All elements section and pdffile are optional. The note element, starting with #n can be placed in any column.
- "-l" spaced separated list of arguments. Each argument, is in itself a list with the format similar to a single row of the csv file. i.e. <pdffile\>,<section\>,<subsection\>,<subsubsection\>,<#nnote_text\>. Care must be taken to not introduce spaces. In case of necessary spaces, the words need to be enclosed in inverted commas.
- "-t" the title which will be added in the generated pdf document. Defaults to an empty string
- "-n" the name of the generated pdf document. Defaults to combined_doc.pdf

### Minimal Example

As a minimal example, run the following command from the root repository folder:

python3 pdf_aggregate.py -f sample.csv -n sample.pdf -t "sample combined pdf document"

this reads sample.csv which includes the following data


sources1/dictionary.pdf,	Dictionaries	#nThis is part of oxford dictionary	
sources1/drylab.pdf	        Academic        Research paper	                     #nActually a newsletter
sources1/example.pdf        Academic        Research paper	                     #nA usenix paper
sources1/invoicesample.pdf	Miscellaneous	Invoices	                         #n This is a sample invoice
sources1/somatosensory.pdf	Academic	    Text book	                         #nAnatomy of the Somatosensory System

Therefore, the 4 pdfs from sources1 folder are added in the appropriate sections and subsections.

The end result is the generation of sample.pdf in the root folder with appropriate sections, subsections and notes. 

![ToC of sample.pdf](latex/pdf_aggregator.png)

