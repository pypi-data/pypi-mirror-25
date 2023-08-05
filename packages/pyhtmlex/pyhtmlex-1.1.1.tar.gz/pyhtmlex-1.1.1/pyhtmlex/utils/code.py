# -*- coding: UTF-8 -*-
from pyhtmlex.base.head import *
from pyhtmlex.base.body import *


class Code(Div):
    width = 800
    style = Style()
    style.add_class("code", margin=0, display='block', overflow='auto')
    style.add_class("code_line1", background="#ccc")
    style.add_class("code_line2", background="#aca")
    style.add_class("code_key", color="#00a", font_weight="bold")
    style.add_class("code_interpreter", color="#aaa", font_weight="bold")
    style.add_class("code_comment", color="#0a0", font_weight="bold")
    style.add_class("code_plain", color="#000")
    style.add_class("code_str", color="#900")

    def __init__(self, lines):
        super(Code, self).__init__('code')
        pre = Pre()
        pre.set_attributes(style='display:inline-block;')
        ol = Ol()
        div = Div()
        ol.push_back(div)
        div.set_attributes(style='width: %spx;' % self.width)
        pre.push_back(ol)
        cls_name = ['code_line1', 'code_line2']
        for li in self.create(lines, cls_name):
            ol.push_back(li)
        self.children.append(pre)

    def create(self, lines, cls_name):
        pass


class PythonCode(Code):
    def __init__(self, lines):
        self.python_key = [
            'False', 'class', 'finally', 'is', 'return',
            'None', 'continue', 'for', 'lambda', 'try',
            'True', 'def', 'from', 'nonlocal', 'while',
            'and', 'del', 'global', 'not', 'with',
            'as', 'elif', 'if', 'or', 'yield',
            'assert', 'else', 'import', 'pass',
            'break', 'except', 'in', 'raise', 'print'
        ]
        super(PythonCode, self).__init__(lines)

    def create(self, lines, cls_name):
        multi_line_txt = 0
        beg = 0
        raw_line = lines[0].strip()
        if len(raw_line) > 1 and raw_line[:2] == '#!':
            li = Li(cls_name=cls_name[beg])
            raw_line = raw_line.replace('<', '&lt')
            raw_line = raw_line.replace('>', '&gt')
            li.push_back(Span(raw_line, 'code_interpreter'))
            beg = 1
        for i in range(beg, len(lines)):
            line = lines[i]
            line = line.replace('<', '&lt')
            line = line.replace('>', '&gt')
            li = Li(cls_name=cls_name[i % 2])

            multi_line_txt_index = line.find("'''")
            if multi_line_txt_index != -1:
                if multi_line_txt:
                    multi_line_txt = 0
                    words = [line[: multi_line_txt_index+3]]
                    words.extend(self.get_words(line[multi_line_txt_index+3:]))
                else:
                    multi_line_txt = 1
                    words = self.get_words(line[: multi_line_txt_index])
                    words.append(line[multi_line_txt_index:])
            elif multi_line_txt:
                words = [line]
            else:
                words = self.get_words(line)

            for word in words:
                if multi_line_txt and multi_line_txt_index == -1:
                    li.push_back(Span(word, 'code_str'))
                elif len(word) > 0 and word[0] == "#":
                    li.push_back(Span(word, 'code_comment'))
                elif len(word) > 0 and (word[0] in ['"', "'"] or word[-1] in ['"', "'"]):
                    li.push_back(Span(word, 'code_str'))
                elif word.strip() in self.python_key:
                    li.push_back(Span(word, 'code_key'))
                else:
                    li.push_back(Span(word, 'code_plain'))
            yield li

    @staticmethod
    def get_words(line):
        words = []
        i = 0
        while i < len(line):
            start = {}
            for item in ["'", '"', "#"]:
                start[line.find(item, i)] = item
            start.pop(-1, None)

            if not start:
                words.extend([(word + ' ') for word in line[i:].strip('\n').split(' ')])
                words[-1] = words[-1].strip()
                return words

            start = start.items()
            start.sort()
            if start[0][1] == "#":
                words.extend([(word + ' ') for word in line[i: start[0][0]].strip('\n').split(' ')])
                words[-1] = words[-1].strip()
                words.append(line[start[0][0]:])
                return words
            else:
                end = line.find(start[0][1], start[0][0] + 1)
                # print line[start2:end + 1]
                words.extend([(word + ' ') for word in line[i:start[0][0]].strip('\n').split(' ')])
                words[-1] = words[-1].strip()
                words.append(line[start[0][0]: end + 1])
            i = end + 1
        return words


class CppCode(Code):
    def __init__(self, lines):
        self.cpp_key = [
            'asm', 'do', 'if', 'return', 'typedef', 'auto', 'double', 'inline', 'short', 'typeid', 'bool',
            'dynamic_cast', 'int', 'signed', 'typename', 'break', 'else', 'long', 'sizeof', 'union', 'case',
            'enum', 'mutable', 'static', 'unsigned', 'catch', 'explicit', 'namespace', 'static_cast', 'using',
            'char', 'export', 'new', 'struct', 'virtual', 'class', 'extern', 'operator', 'switch', 'void', 'const',
            'false', 'private', 'template', 'volatile', 'const_cast', 'float', 'protected', 'this', 'wchar_t',
            'continue', 'for', 'public', 'throw', 'while', 'default', 'friend', 'register', 'true', 'delete',
            'goto', 'reinterpret_cast', 'try', 'alignas', 'alignof', 'char16_t', 'char32_t', 'constexpr', 'decltype',
            'noexcept', 'nullptr', 'static_assert', 'thread_local',
        ]
        super(CppCode, self).__init__(lines)

    def create(self, lines, cls_name):
        multi_line_txt = 0
        for i in range(len(lines)):
            line = lines[i]
            line = line.replace('<', '&lt')
            line = line.replace('>', '&gt')
            li = Li(cls_name=cls_name[i % 2])

            if multi_line_txt:
                multi_line_txt_index = line.find("*/")
            else:
                multi_line_txt_index = line.find("/*")
            if multi_line_txt_index != -1:
                if multi_line_txt:
                    multi_line_txt = 0
                    words = [line[: multi_line_txt_index+2]]
                    words.extend(self.get_words(line[multi_line_txt_index+2:]))
                else:
                    multi_line_txt = 1
                    words = self.get_words(line[: multi_line_txt_index])
                    words.append(line[multi_line_txt_index:])
            elif multi_line_txt:
                words = [line]
            else:
                words = self.get_words(line)
            # print words

            for word in words:
                if multi_line_txt and multi_line_txt_index == -1:
                    li.push_back(Span(word, 'code_comment'))
                elif len(word) > 0 and word[:2] == "//":
                    li.push_back(Span(word, 'code_comment'))
                elif len(word) > 0 and (word[0] in ['"', "'"]):
                    li.push_back(Span(word, 'code_str'))
                elif word.strip() in self.cpp_key:
                    li.push_back(Span(word, 'code_key'))
                else:
                    li.push_back(Span(word, 'code_plain'))
            yield li

    @staticmethod
    def get_words(line):
        words = []
        i = 0
        while i < len(line):
            start = {}
            for item in ["'", '"', "//"]:
                start[line.find(item, i)] = item
            start.pop(-1, None)

            if not start:
                words.extend([(word + ' ') for word in line[i:].strip('\n').split(' ')])
                words[-1] = words[-1].strip(' ')
                return words

            start = start.items()
            start.sort()
            if start[0][1] == "//":
                words.extend([(word + ' ') for word in line[i: start[0][0]].strip('\n').split(' ')])
                words[-1] = words[-1].strip(' ')
                words.append(line[start[0][0]:])
                return words
            else:
                end = line.find(start[0][1], start[0][0] + 1)
                # print line[start2:end + 1]
                words.extend([(word + ' ') for word in line[i:start[0][0]].strip('\n').split(' ')])
                words[-1] = words[-1].strip()
                words.append(line[start[0][0]: end + 1])
            i = end + 1
        return words


