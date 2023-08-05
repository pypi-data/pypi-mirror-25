import chardet
from code import *
from console import *


def md_parser(div, pathname, title):
    def check_encoding(lines):
        for line in lines:
            line = line.rstrip()
            if len(line) > 0 : #and line[0] not in ['$', '@', '#']:
                encoding = chardet.detect(line)['encoding']
                print 'encoding:', encoding
                return encoding

    def mk_p(line):
        protocol = line.find('://')
        p = P('')
        while protocol != -1:
            if line[:protocol][-5:] == 'https':
                index1 = protocol - 5
            elif line[:protocol][-4:] == 'http':
                index1 = protocol - 4
            else:
                index1 = line.rfind(' ', None, protocol)
            index2 = line.find(' ', protocol)
            if index2 == -1:
                txt1 = line[:index1]
                link = line[index1:]
                line = None
                protocol = -1
            else:
                txt1 = line[:index1]
                link = line[index1: index2]
                line = line[index2:]
                protocol = line.find('://')

            p.push_back(Span(txt1))
            p.push_back(A(link, link, True))

        if line:
            p.push_back(Span(line))
        return p

    class TxtPrint(object):
        @staticmethod
        def code_py(lines):
            return PythonCode(lines)

        @staticmethod
        def code_cpp(lines):
            return CppCode(lines)

        @staticmethod
        def console(lines):
            return Console(lines)

    class ResourcePrint(object):
        @staticmethod
        def code_py(filename):
            with open(filename, 'r') as f:
                return PythonCode(f.readlines())

        @staticmethod
        def code_h(filename):
            with open(filename, 'r') as f:
                return CppCode(f.readlines())

        @staticmethod
        def code_cpp(filename):
            with open(filename, 'r') as f:
                return CppCode(f.readlines())

        @staticmethod
        def console(filename):
            with open(filename, 'r') as f:
                return Console(f.readlines())

    md_style = Style()
    md_style.add_class("split_line", width='100%', height=2, background='#999', margin_top=10, margin_bottom=10)

    f = open(pathname + '/' + title + '.txt', 'r')
    contents = f.readlines()
    f.close()

    if check_encoding(contents) == 'ascii':
        for i in range(len(contents)):
            contents[i] = contents[i].decode('GBK')

    temp = []
    state = 0
    split_line = Div("split_line")
    for line in contents:
        line = line.rstrip()
        if line[:3] == '```':
            if state == 0:
                state = 1
                words = line.split(' ')
                if len(words) == 1:
                    pretty = 'console'
                else:
                    pretty = 'code_' + words[1]
            else:
                state = 0
                res = getattr(TxtPrint, pretty)(temp)
                div.push_back(res)
                temp = []
        elif state == 1:
            temp.append(line)
        elif line[:3] == '<<<':
            words = line.split(' ')
            pretty = words[1].split('.')
            pretty = 'console' if len(pretty) == 1 else ('code_' + pretty[1])
            res = getattr(ResourcePrint, pretty, None)
            if res is None:
                res = getattr(ResourcePrint, 'console', None)
            res = res(pathname + '/code/' + words[1])
            div.push_back(res)
        elif line[:3] in ['---', '***'] or line[:5] in ['- - -', '* * *']:
            div.push_back(split_line)
        elif line[:4] == '=== ':
            http = line[4:].partition(' ')
            div.push_back(A(http[0], http[2], True))
        elif line[:2] == '- ':
            div.push_back(Li(line[2:]))
        else:
            title_cls = line.split(' ')[0]
            if len(title_cls) != 0 and "######".find(title_cls) != -1:
                len_title_cls = len(title_cls)
                div.push_back(H(line[len_title_cls:], len_title_cls))
            else:
                div.push_back(mk_p(line))
    return [Code.style, Console.style, md_style]
