#coding=utf-8
import numpy as np
import pandas as pd


def section_criterion(df, condition, n1_list):
    criterion_result = pd.Series(True, index=df.index)
    if condition == 'flight':
        for n1_order in n1_list:
            criterion = df.iloc[:, n1_order].copy()
            for i in criterion.index[:-4]:
                logic_condition = True
                for t in range(5):
                    if criterion[i + t] > 20:
                        logic_condition = True & logic_condition
                    else:
                        logic_condition = False & logic_condition
                criterion[i] = logic_condition

            for i in criterion.index[-4:]:
                criterion[i] = False
            criterion_result = criterion & criterion_result
        return df[criterion_result]


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

def radio_msp_lsp(x):
    if x[1] < 0:
        x[0] = radio_msp_binary_caculation(x[0])
    x[0] = x[0] + x[1]
    return x[0]

def radio_msp_lsp_caculation(df, msp_order, lsp_order):
    radio = df.iloc[:, [msp_order, lsp_order]]
    df.iloc[:, msp_order]= radio.apply(radio_msp_lsp, axis = 1)
    return df

def flap_cacu(value):
    """
    y = np.array([-112, -40, -1, 0, 1, 2, 5, 10, 15, 25, 30, 40, 112])
    x = np.array([-180, -108.13, -17, 0, 17.58, 30.67, 41.75, 52.62, 64.86, 77.38, 90.44, 108.13, 180])
    polynomial = np.polyfit(x, y, 10)  # 用3次多项式拟合
    """
    polynomial = np.array([ -2.85593573e-18,   5.34870752e-16,   9.45470132e-14,
        -2.29814827e-11,   3.07992481e-10,   1.75352813e-07,
        -1.21685022e-05,   2.72090256e-04,   2.41416423e-03,
        -4.59913906e-02,   9.21541838e-02])
    equation = np.poly1d(polynomial)
    if isinstance(value, float):
        result = equation(value)
        result = round(result, 2)
        return result
    else:
        return value

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
        return str_flt.replace(' ', '')

    def flight_status(self, df, WQAR_conf):
        if WQAR_conf == '737_3C':
            AIR_GROUND_order = [1305, 1307]
        elif WQAR_conf == '737_7':
            AIR_GROUND_order = [1559, 1601]
        else:
            return None
        AIR_GROUND_order = [i - 1 for i in AIR_GROUND_order]
        df_AIR_GROUND_1 = df.iloc[:, AIR_GROUND_order[0]]
        df_AIR_GROUND_2 = df.iloc[:, AIR_GROUND_order[1]]
        if df_AIR_GROUND_1.str.contains('AIR').sum() > 0 or df_AIR_GROUND_2.str.contains('AIR').sum() > 0:
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
        df = self.flap_hand_postion(df, WQAR_conf)
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

    def eng_oil_merge(self, qar_df, WQAR_conf):
        if WQAR_conf == '737_7':
            return qar_df
        elif WQAR_conf == '737_3C':
            list_OIL_1_index = range(172, 180)
            list_OIL_2_index = range(184, 192)
            df = df_combine(qar_df, list_OIL_1_index)
            df = df_combine(df, list_OIL_2_index)
            oil_temp_1 = range(243, 251)
            oil_temp_2 = range(251, 259)
            df = df_combine(df, oil_temp_1)
            df = df_combine(df, oil_temp_2)
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

    def flap_hand_postion(self, qar_df, WQAR_conf):
        if WQAR_conf == '737_3C':
            flap_order = 303
        elif WQAR_conf == '737_7':
            flap_order = 301
        else:
            return qar_df
        df = qar_df
        df.iloc[:,flap_order] = df.iloc[:, flap_order].map(flap_cacu)
        return df