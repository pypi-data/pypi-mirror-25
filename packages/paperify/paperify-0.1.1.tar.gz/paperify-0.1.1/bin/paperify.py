#!/usr/bin/env python

import sys
import os
from subprocess import call

"""
Usage:
    paperify.py doc.md
    paperify.py doc.md paper
    paperify.py doc.md twocols show
    paperify.py doc.md book latex
    paperify.py doc.md web html
    paperify.py doc.md webtoc html
"""

if len(sys.argv) < 2:
    sys.exit('Not enough arguments')

home = os.path.expanduser('~')
cwd = os.getcwd()
tex_template_dir = '/.paperify'

template = 'paper_pandoc.latex'
extension = '.pdf'
tex_filter = home + tex_template_dir + '/custom_tex_filter.py'
algo_filter = home + tex_template_dir + '/algo_filter.py'
ifig_filter = home + tex_template_dir + '/ifig_filter.py'
prefix = ['pandoc', '-F', tex_filter, '-F', algo_filter, '-F', ifig_filter]
suffix = []

bib_file = cwd + '/biblio.bib'
# csl_file = home + tex_template_dir + '/acm.csl'
csl_file = home + tex_template_dir + '/cit.csl'

if os.path.isfile(bib_file):
    prefix.append('--filter')
    prefix.append('pandoc-citeproc')
    prefix.append('--csl')
    prefix.append(csl_file)
    prefix.append('--bibliography')
    prefix.append(bib_file)
    prefix.append('-M')
    prefix.append('link-citations=true')

if len(sys.argv) > 3:
    if 'tex' in sys.argv[3]:
        extension = '.tex'
    elif 'htm' in sys.argv[3]:
        extension = '.html'

if len(sys.argv) > 2:
    if 'ieee' in sys.argv[2]:
        template = 'ieee_two_pandoc.latex'
    elif 'two' in sys.argv[2]:
        template = 'twocols_pandoc.latex'
    elif 'paper' in sys.argv[2]:
        template = 'paper_pandoc.latex'
    elif 'book' in sys.argv[2]:
        template = 'book_pandoc.latex'
    elif 'webpres' in sys.argv[2]:
        template = 'webpres_pandoc.html'
        extension = '.html5'
        prefix.append('-t')
        prefix.append('revealjs')
        prefix.append('--mathjax')
    elif 'webtoc' in sys.argv[2]:
        template = 'web_pandoc.html'
        extension = '.html'
        prefix.append('--toc')
        prefix.append('--toc-depth=1')
        prefix.append('--mathjax')
    elif 'web' in sys.argv[2]:
        template = 'web_pandoc.html'
        extension = '.html'
        prefix.append('--mathjax')
    elif 'pres' in sys.argv[2]:
        template = 'presentation_pandoc.beamer'
        prefix.append('--to=beamer')
    elif 'poster' in sys.argv[2]:
        template = 'poster_pandoc.latex'

md_fname = sys.argv[1]
pdf_fname = md_fname[:-3] + extension

md_fname = cwd + '/' + md_fname
pdf_fname = cwd + '/' + pdf_fname


template = home + tex_template_dir + '/' + template
command = prefix + [md_fname, '-s', '-o', pdf_fname,
                    '--template', template, '--highlight-style', 'haddock'] + suffix
call(command)

if 'show' in sys.argv:
    call([
        'evince',
        pdf_fname,
    ])
