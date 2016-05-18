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

def df_combine(df, list_order):
    for order in list_order:
        df_first = df.iloc[:, list_order[0]].replace('', np.nan)
        df.iloc[:, list_order[0]] = df_first.combine_first(df.iloc[:, order])
    return df

def radio_msp_binary_caculation(x):
    bit_code = ~(int(x/ 2048))
    bit_code = bit_code & 3
    bit_code = bit_code * -2048
    return bit_code

def radio_msp_lsp_caculation(df, msp_order, lsp_order):
    radio_msp = df.iloc[:, msp_order][df.iloc[:, lsp_order] < 0].map(
        radio_msp_binary_caculation)
    df.iloc[:, msp_order][df.iloc[:, lsp_order] < 0] = radio_msp + df.iloc[:, lsp_order][df.iloc[:, lsp_order] < 0]
    df.iloc[:, msp_order][df.iloc[:, lsp_order] >= 0] = df.iloc[:, msp_order][df.iloc[:, lsp_order] >= 0] + df.iloc[:, lsp_order][df.iloc[:, lsp_order] >= 0]
    return df

class flight_information(object):

    def __init__(self):
        pass

    def flight_number(self, df, WQAR_conf):
        if WQAR_conf == '737_3C':
            list_all_flt = exchange(range(504, 512))
        elif WQAR_conf == '737_7':  # '737_7'
            list_all_flt = exchange(range(663, 671))
        else:
            return None
        str_flt = ''
        for sq in list_all_flt:
            s_flt = df.iloc[:, sq].value_counts()
            chr_flt = chr(s_flt.index[1])
            str_flt = str_flt + chr_flt
        return str_flt

    def flight_status(self, df, WQAR_conf):
        if WQAR_conf == '737_3C':
            radio_order = 201 - 1
        elif WQAR_conf == '737_7':
            radio_order = 219 - 1
        else:
            return None
        if df.iloc[:, radio_order].max()>15:
            return 'FLIGHT'
        else:
            return 'GROUND'

class second_process(object):

    def __init__(self):
        pass

    def main(self, qar_df, WQAR_conf):
        df = self.GMT_merge(qar_df, WQAR_conf)
        df = self.vertical_acc(df, WQAR_conf)
        df = self.eng_oil_merge(df, WQAR_conf)
        df = self.radio_calculate(df, WQAR_conf)
        return df

    def GMT_merge(self, df, WQAR_conf):
        if WQAR_conf == '737_3C':
            gmt_order = [88, 89, 90]
            gmt_raw = df.iloc[:, gmt_order]
            gmt_raw = gmt_raw.replace('', np.nan)
            gmt_fill = gmt_raw.fillna(method='bfill')
            gmt_fill = gmt_fill.fillna(method='ffill')
        elif WQAR_conf == '737_7': # '737_7'
            gmt_order = [95, 96, 97]
            gmt_raw = df.iloc[:, gmt_order]
            gmt_raw = gmt_raw.replace('', np.nan)
            gmt_fill = gmt_raw.fillna(method='ffill')
            gmt_fill = gmt_fill.fillna(method='bfill')
        else:
            return df
        gmt_fill = gmt_fill.astype('int32')
        gmt_fill = gmt_fill.astype('S32')
        gmt_s = gmt_fill.apply(gmt_process, axis=1)
        df['$GMT TIME'] = gmt_s
        return df

    def vertical_acc(self, df, WQAR_conf):
        if WQAR_conf == '737_3C':
            list_ver_index = range(403, 411, 1)
        elif WQAR_conf == '737_7':
            list_ver_index = range(465, 481, 1)
        else:
            return df
        for index in list_ver_index:
            order = index - 1
            df.iloc[:,order] = df.iloc[:,order] - 3.3750111
        return df

    def eng_oil_merge(self, df, WQAR_conf):
        if WQAR_conf == '737_7':
            return df
        elif WQAR_conf == '737_3C':
            list_OIL_1_index = range(172, 180)
            list_OIL_2_index = range(184, 192)
            df = df_combine(df, list_OIL_1_index)
            df = df_combine(df, list_OIL_2_index)
        return df

    def radio_calculate(self, qar_df, WQAR_conf):
        if WQAR_conf == '737_3C':
            list_radio_msp_index = [201, 341, 202, 343]
            list_radio_lsp_index = [203, 342, 204, 344]
        elif WQAR_conf == '737_7':
            list_radio_msp_index = [219, 313, 314, 315, 316, 321, 322, 323, 324]
            list_radio_lsp_index = [220, 317, 318, 319, 320, 325, 326, 327, 328]
        else:
            return qar_df
            # compute LRRA
        list_radio_msp_index = map(lambda x: x - 1, list_radio_msp_index)
        list_radio_lsp_index = map(lambda x: x - 1, list_radio_lsp_index)
        df = df_combine(qar_df, list_radio_msp_index)
        df = df_combine(df, list_radio_lsp_index)
        for order in range(len(list_radio_lsp_index)):
            df = radio_msp_lsp_caculation(df,
                                          list_radio_msp_index[order],
                                          list_radio_lsp_index[order])
        return df