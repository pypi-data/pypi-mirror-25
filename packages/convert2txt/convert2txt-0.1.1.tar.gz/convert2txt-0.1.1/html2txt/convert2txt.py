# -*- coding: cp936 -*-
import doc_to_txt
import pdf_to_txt
import html_to_txt
import fnmatch
import sys
reload(sys)
sys.setdefaultencoding('gbk')




# 其他文件格式转txt格式
# src_path:原文件路径，带扩展名（.doc/.docx/.html/.pdf）
# desc_path:目的文件路径，扩展名.txt
# def convert2txt(self, src_path, desc_path):
def convert2txt( src_path, desc_path):
    if fnmatch.fnmatch(src_path, '*.doc') or fnmatch.fnmatch(src_path, '*.wps') or fnmatch.fnmatch(src_path, '*.docx'):
        doc_to_txt.doc2txt(src_path, desc_path)
        print 'doc file transfer completed!'
    elif fnmatch.fnmatch(src_path, '*.pdf'):
        pdf_to_txt.Pdf2Txt(src_path, desc_path)
        print 'pdf file transfer completed!'
    elif fnmatch.fnmatch(src_path, '*.html'):
        html_to_txt.html2txt(src_path,desc_path)
        print 'html file transfer completed!'
    else:
        print 'this is not a doc , pdf ,html file'

if __name__ == '__main__':
    convert2txt(r'D:\native_repo\conver2txt_change\guangdong-attach-000010-000.doc',
                r'D:\native_repo\conver2txt_change\guangdong-attach-000010-000.txt')
    convert2txt(r'D:\native_repo\conver2txt_change\guangdong-attach-000003-000.pdf',
            r'D:\native_repo\conver2txt_change\guangdong-attach-000003-000.txt')
    convert2txt(r'D:\native_repo\conver2txt_change\aa.html',r'D:\native_repo\conver2txt_change\aa.txt')