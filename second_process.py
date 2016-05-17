#coding=utf-8
import numpy as np
import pandas

def exchange(list_index):
    for i in range(len(list_index)):
        if i%2 == 0:
            list_index[i], list_index[i + 1] = list_index[i + 1], list_index[i]
    return list_index

def gmt_process(x):
    for order in range(3):
        x[order] = x[order].zfill(2)
    return x[0] + ':' + x[1] + ':' + x[2]

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
            gmt_order = [88, 89, 90]
        elif WQAR_conf == '737_7': # '737_7'
            gmt_order = [95, 96, 97]
        else:
            return None
        gmt_raw = df.iloc[:, gmt_order]
        gmt_raw = gmt_raw.replace('', np.nan)
        gmt_fill = gmt_raw.fillna(method='ffill')
        print gmt_fill
        gmt_fill = gmt_fill.astype('int32')
        gmt_fill = gmt_fill.astype('S32')
        gmt_s = gmt_fill.apply(gmt_process, axis=1)
        return gmt_s

    def vertical_acc(self, df, WQAR_conf):
        if WQAR_conf == '737_3C':
            list_ver_index = range(403, 411, 1)
        elif WQAR_conf == '737_7':
            list_ver_index = range(465, 481, 1)
        else:
            return None
        for index in list_ver_index:
            order = index - 1
            df.iloc[:,order] = df.iloc[:,order] - 3.3750111
        return df