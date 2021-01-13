import zipfile
import xml.etree.ElementTree

WORD_NAMESPACE = '{http://schemas.openxmlformats.org/wordprocessingml/2006/main}'
PARA = WORD_NAMESPACE + 'p'
TEXT = WORD_NAMESPACE + 't'
TABLE = WORD_NAMESPACE + 'tbl'
ROW = WORD_NAMESPACE + 'tr'
CELL = WORD_NAMESPACE + 'tc'

with zipfile.ZipFile('data/docx/Memorias.docx') as docx:
    tree = xml.etree.ElementTree.XML(docx.read('word/document.xml'))

for table in tree.iter(TABLE):
    for row in table.iter(ROW):
        for cell in row.iter(CELL):
            print(''.join(node.text for node in cell.iter(TEXT)))
