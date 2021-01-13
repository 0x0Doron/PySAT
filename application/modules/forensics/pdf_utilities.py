#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from PyPDF2 import PdfFileReader


def get_info(path):
    with open(path, 'rb') as f:
        pdf = PdfFileReader(f)
        info = pdf.getDocumentInfo()
        np = pdf.getNumPages()


    author = info.author
    creator = info.creator
    producer = info.producer
    subject = info.subject
    title = info.title

    print(str(info)+'\n\n')

    print('Nº Pages: {}'.format(np))
    print('\n\nAuthor: {}'.format(author))
    print('Creator: {}'.format(creator))
    print('Producer: {}'.format(producer))
    print('Subject: {}'.format(subject))
    print('title: {}\n\n\n'.format(title))


def text_extractor(path):
    with open(path, 'rb') as f:
        pdf = PdfFileReader(f)
        page = pdf.getPage(0)
        print(page)
        print('Page type: {}'.format(str(type(page))))
        text = page.extractText()
        print(text)

get_info('data/pdf/carta.pdf')
