# -*- coding: utf-8 -*-

list_chr = "1234567890ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"


def replace_chr(word):
    temp = ""
    for i in word:
        if i in list_chr:
            temp += i
        else:
            if len(str(ord(i))) == 1:
                v = '0' + str(ord(i))
            else:
                v = str(ord(i))
            temp += '-'+v+'-'
    return temp


def replace_get(word):
    word_lists = word.split('-')
    for count, word_list in enumerate(word_lists):
        if count % 2 == 1:
            if word_list <= 255:
                word_lists[count] = chr(int(word_list))
            else:
                word_list = hex(int(word_list))[2:]
                word_list = word_list if len(word_list) == 4 else '0'*(4-len(word_list)) + word_list
                word_lists[count] = ('\\u'+word_list).decode('unicode-escape')
    return ''.join(word_lists)


def replace_hex(word):
    temp = ""
    for i in word:
        if i in list_chr:
            temp += i
        else:
            if len(hex(ord(i))[2:]) == 1:
                v = '0' + hex(ord(i))[2:]
            else:
                v = hex(ord(i))[2:]
            temp += '%'+v
    return temp