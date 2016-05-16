#coding=utf-8
import pandas

def exchange(list_index):
    for i in range(len(list_index)):
        if i%2 == 0:
            list_index[i], list_index[i + 1] = list_index[i + 1], list_index[i]
    return list_index

class second_process(object):

    def __init__(self):
        pass

    def flight_number(self, df, WQAR_conf):
        if WQAR_conf == '737_3C':
            list_all_flt = exchange(range(504, 512))
        elif WQAR_conf == '737_7': # '737_7'
            list_all_flt = exchange(range(663, 671))
        else:
            return None
        str_flt = ''
        for sq in list_all_flt:
            s_flt = df.iloc[:,sq].value_counts()
            chr_flt = chr(s_flt.index[1])
            str_flt = str_flt + chr_flt
        return str_flt

    def GMT_merge(self, df, WQAR_conf):
        if WQAR_conf == '737_3C':
            list_all_flt = exchange(range(504, 512))
        elif WQAR_conf == '737_7': # '737_7'
            list_all_flt = exchange(range(663, 671))
        else:
            return None
        str_flt = ''
        for sq in list_all_flt:
            s_flt = df.iloc[:,sq].value_counts()
            chr_flt = chr(s_flt.index[1])
            str_flt = str_flt + chr_flt
        return str_flt