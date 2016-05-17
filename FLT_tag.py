#coding=utf-8

class FLT_tag():
    def __init__(self):
        pass

    def get_FTL_number(self, list_qar, WQAR_conf):
        list_turn = map(list, zip(*list_qar))
        # 多加了一行填到[0]，故可从下标1开始算
        if WQAR_conf == '737_3C':
            list_all_flt = list_turn[504:512]
        else: # '737-7'
            list_all_flt = list_turn[663:671]

        list_flt_2 = list_all_flt[0]
        while '' in list_flt_2:
            list_flt_2.remove('')

        list_flt_1 = list_all_flt[1]
        while '' in list_flt_1:
            list_flt_1.remove('')

        list_flt_4 = list_all_flt[2]
        while '' in list_flt_4:
            list_flt_4.remove('')

        list_flt_3 = list_all_flt[3]
        while '' in list_flt_3:
            list_flt_3.remove('')

        list_flt_6 = list_all_flt[4]
        while '' in list_flt_6:
            list_flt_6.remove('')

        list_flt_5 = list_all_flt[5]
        while '' in list_flt_5:
            list_flt_5.remove('')

        list_flt_8 = list_all_flt[6]
        while '' in list_flt_8:
            list_flt_8.remove('')

        list_flt_7 = list_all_flt[7]
        while '' in list_flt_7:
            list_flt_7.remove('')



        items = dict([(list_flt_2.count(i), i) for i in list_flt_2])
        char_flt_2 = items[max(items.keys())]

        items = dict([(list_flt_1.count(i), i) for i in list_flt_1])
        char_flt_1 = items[max(items.keys())]

        items = dict([(list_flt_3.count(i), i) for i in list_flt_3])
        char_flt_3 = items[max(items.keys())]

        items = dict([(list_flt_4.count(i), i) for i in list_flt_4])
        char_flt_4 = items[max(items.keys())]

        items = dict([(list_flt_6.count(i), i) for i in list_flt_6])
        char_flt_6 = items[max(items.keys())]

        items = dict([(list_flt_5.count(i), i) for i in list_flt_5])
        char_flt_5 = items[max(items.keys())]

        items = dict([(list_flt_7.count(i), i) for i in list_flt_7])
        char_flt_7 = items[max(items.keys())]

        items = dict([(list_flt_8.count(i), i) for i in list_flt_8])
        char_flt_8 = items[max(items.keys())]

        final_number = chr(char_flt_1) + chr(char_flt_2) + chr(char_flt_3) + chr(char_flt_4) \
              + chr(char_flt_5) + chr(char_flt_6) + chr(char_flt_7) + chr(char_flt_8)

        #去除航班号中的空格
        final_number = final_number.replace(' ','')
        return final_number

    def get_RADIO_HEIGHT(self, list_qar, WQAR_conf):
        list_turn = map(list, zip(*list_qar))
        # 多加了一行填到[0]，故可从下标1开始算
        if WQAR_conf == '737_3C':
            # 1~4副帧都合成到201
            list_radio_msp_index = [201, 341, 202, 343]
            list_radio_msp = []
            for index in list_radio_msp_index:
                list_radio_msp.append(list_turn[(index - 1) ])
            list_radio_msp = self.merge_para_list(list_radio_msp)
            list_radio_lsp_index = [203, 342, 204, 344]
            list_radio_lsp = []
            for index in list_radio_lsp_index:
                list_radio_lsp.append(list_turn[(index - 1) ])
            list_radio_lsp = self.merge_para_list(list_radio_lsp)
            # 2,4副帧合到341
            list_turn[341 - 1] = self.map_radio_height(list_turn[341 - 1],list_turn[342 - 1])
            list_turn[343 - 1] = self.map_radio_height(list_turn[343 - 1],list_turn[344 - 1])

            # ENG OIL QTY归一化
            list_OIL_1_index = range(172,180)
            list_OIL_2_index = range(184,192)
            list_OIL = []
            for index in list_OIL_1_index:
                list_OIL.append(list_turn[index])
            list_turn[172] = self.merge_para_list(list_OIL)
            list_OIL = []
            for index in list_OIL_2_index:
                list_OIL.append(list_turn[index])
            list_turn[184] = self.merge_para_list(list_OIL)


        else: # '737-7'
            list_radio_msp = list_turn[219 - 1]
            list_radio_lsp = list_turn[220 - 1]
            list_radio_LRRA = range(312, 328, 1)
            for i in range(4):
                list_turn[list_radio_LRRA[i]] = self.map_radio_height(list_turn[list_radio_LRRA[i]],
                                                                      list_turn[list_radio_LRRA[i] + 4])
            for i in range(8,12,1):
                list_turn[list_radio_LRRA[i]] = self.map_radio_height(list_turn[list_radio_LRRA[i]],
                                                                      list_turn[list_radio_LRRA[i] + 4])

        list_radio_result = self.map_radio_height(list_radio_msp,list_radio_lsp)

        if WQAR_conf == '737_3C':
            list_turn[201 - 1] = list_radio_result
        else:
            list_turn[219 - 1] = list_radio_result
        # vertical_acc
        list_turn = self.vertical_acc(list_turn, WQAR_conf)

        list_result = map(list, zip(*list_turn))

        return list_radio_msp , list_result

    def merge_para_list(self, some_para_list):
        for list_item in some_para_list[1:]:
            for list_index in range(len(list_item)):
                if list_item[list_index] <> '':
                    some_para_list[0][list_index] = list_item[list_index]
        return some_para_list[0]

    def map_radio_height(self, list_radio_msp, list_radio_lsp):
        for index in range(len(list_radio_msp)):
            if list_radio_lsp[index] < 0:
                bit_code = ~(int(list_radio_msp[index]) / 2048)
                bit_code = bit_code & 3
                list_radio_msp[index] = -2048 * bit_code + list_radio_lsp[index]
            else:
                list_radio_msp[index] = list_radio_msp[index] + list_radio_lsp[index]
        list_radio_map = list_radio_msp
        return list_radio_map



    def vertical_acc(self, list_turn, WQAR_conf):

        if WQAR_conf == '737_3C':
            list_ver_index = range(403, 411, 1)
            for index in list_ver_index:
                list_turn[index - 1] = self.minus(list_turn[index - 1], -3.3750111)
        else:
            list_ver_index = range(465, 481, 1)
            for index in list_ver_index:
                list_turn[index - 1] = self.minus(list_turn[index - 1], -3.3750111)

        return list_turn

    def minus(self, list_single, value):
        for index in range(len(list_single)):
            list_single[index] = list_single[index] + value
        return list_single

    def get_GMT_list(self, list_qar, WQAR_conf):
        list_turn = list_qar
        # 多加了一行填到[0]，故可从下标1开始算
        GMT_model_256 = [89, 90, 91]
        GMT_model_512 = [96, 97, 98]
        if WQAR_conf == '737_3C':
            model = GMT_model_256
        elif WQAR_conf == '737_7':
            model = GMT_model_512
        else:
            return

        list_GMT = []
        str_HMS = ''
        for row in list_turn:
            list_HMS =[]
            if row[model[0]-1] == '':
                list_GMT.append(str_HMS)
                continue
            for item in model:
                time_str = (str(int(row[item - 1]))).zfill(2)
                list_HMS.append(time_str)
            seq = ':'
            str_HMS = seq.join(list_HMS)
            list_GMT.append(str_HMS)

        return list_GMT

    def merge_GMT(self, str1, str2):
        result = str1 + ":" + str2
        return result