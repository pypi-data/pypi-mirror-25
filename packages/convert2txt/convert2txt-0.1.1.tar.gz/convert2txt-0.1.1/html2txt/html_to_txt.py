from HTMLParser import HTMLParser
from re import sub
from sys import stderr
from traceback import print_exc


class _DeHTMLParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.__text = []

    def handle_data(self, data):
        text = data.strip()
        if len(text) > 0:
            text = sub('[ \t\r\n]+', ' ', text)
            self.__text.append(text + ' ')

    def handle_starttag(self, tag, attrs):
        if tag == 'p':
            self.__text.append('\n\n')
        elif tag == 'br':
            self.__text.append('\n')

    def handle_startendtag(self, tag, attrs):
        if tag == 'br':
            self.__text.append('\n\n')

    def text(self):
        return ''.join(self.__text).strip()


def html2txt(src_path,desc_path):
    print src_path
    try:
        parser = _DeHTMLParser()
        html_file = open(src_path,'r').read()
        parser.feed(html_file)
        f2 = open(desc_path, "wb")
        f2.write(parser.text() + '\n')
        f2.close()
        parser.close()
        return parser.text()
    except:
        print_exc(file=stderr)
        return 'error'

if __name__ == '__main__':
    html2txt(r'D:\native_repo\conver2txt_change\aa.html',r'D:\native_repo\conver2txt_change\aa.txt')