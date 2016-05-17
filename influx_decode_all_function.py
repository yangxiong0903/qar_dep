# coding:UTF-8
# 对文件夹下的所有raw.dat译码GMT、EGT
import os,sys
import struct
import time
import csv
import numpy
from aircraft_config import AC_WQAR_CONFIG

def cur_file_dir():
    # 返回本文件的路径
    return os.path.split(os.path.realpath(__file__))[0]

class WQAR_DECODE():

    def __init__(self):
        pass

    def SUPF_binary_decode(self, filedata, count, ICD_number, ICD_LSB, ICD_MSB, ICD_RES):
        worddata = filedata[count+ICD_number:count+ICD_number+2]
        #到达末尾则不再算超帧数
        if worddata == '':
            return False
        int_word1 = struct.unpack("<h", worddata)[0]

        int_word1 = int_word1 >> (ICD_LSB-1)
        Remove_MSB = 2 ** (ICD_MSB - ICD_LSB + 1) -1
        int_word1 = int_word1 & Remove_MSB
        float_word1 = int_word1
        return float_word1

    def binary_decode(self, filedata, count, ICD_number, ICD_LSB, ICD_MSB, ICD_RES, ICD_SIGN):
        worddata = filedata[count+ICD_number:count+ICD_number+2]
        #print headworddata
        int_word1 = struct.unpack("<h", worddata)[0]
        #print hex(headword & 0xFFFF) , headword
        SIGN = int_word1 >> (ICD_MSB - 1)
        SIGN = SIGN & 1

        int_word1 = int_word1 >> (ICD_LSB-1)
        Remove_MSB = 2 ** (ICD_MSB - ICD_LSB + 1) -1
        int_word1 = int_word1 & Remove_MSB
        if ICD_SIGN == 'S':
            if SIGN == 0:
                float_word1 = int_word1 * ICD_RES
            else:
                float_word1 = - ( 2 ** (ICD_MSB - ICD_LSB + 1) - int_word1 )
                float_word1 = float_word1 * ICD_RES
        elif ICD_SIGN == "":
            float_word1 = int_word1 * ICD_RES
        return float_word1

    def frame(self, frame_number, filedata, ICD_MSB, ICD_LSB, ICD_WORD, ICD_SUBF, ICD_SUPF, ICD_RES, ICD_SIGN):
        ICD_number = (ICD_WORD-1) *2
        list_para = []
        #print type(filedata)
        #print len(filedata)
        for count in range(0, len(filedata), frame_number*2):
            headworddata = filedata[count:count + 2]
            #print headworddata
            headword = struct.unpack("<h", headworddata)[0]
            sycword_list = [583, 1464, 2631, 3512, -32185]
            if headword in sycword_list:
                #print "headword: %d" % headword
                if ICD_SUPF == 0:
                    if ICD_SUBF == 0:
                        float_word1 = self.binary_decode(filedata, count, ICD_number, ICD_LSB, ICD_MSB, ICD_RES, ICD_SIGN)
                        list_para.append(float_word1)
                    else:
                        if ICD_SUBF == (sycword_list.index(headword) + 1 ):
                            float_word1 = self.binary_decode(filedata, count, ICD_number, ICD_LSB, ICD_MSB, ICD_RES, ICD_SIGN)
                            list_para.append(float_word1)
                        else:
                            list_para.append("")
                elif ICD_SUPF <> 0:
                    if frame_number == 512 :
                        SUPF_word = self.SUPF_binary_decode(filedata,
                                                            (int(count/(4*frame_number*2)))*4*frame_number*2,
                                                            (499-1)*2, 9, 12, 1)
                    else:
                        SUPF_word = self.SUPF_binary_decode(filedata,
                                                            (int(count/(4*frame_number*2)))*4*frame_number*2 + 2*frame_number*2,
                                                            (256-1)*2, 9, 12, 1)
                    SUPF_word = SUPF_word +1
                    #print "SUPF_word: %d" % SUPF_word
                    if ICD_SUBF == 0:
                        if SUPF_word == ICD_SUPF:
                            float_word1 = self.binary_decode(filedata, count, ICD_number, ICD_LSB, ICD_MSB, ICD_RES, ICD_SIGN)
                            list_para.append(float_word1)
                        else:
                            list_para.append("")
                    elif ICD_SUBF <> 0:
                        if SUPF_word == ICD_SUPF:
                            #print SUPF_word
                            #print sycword_list.index(headword) + 1
                            if ICD_SUBF == (sycword_list.index(headword) + 1 ):
                                float_word1 = self.binary_decode(filedata, count, ICD_number, ICD_LSB, ICD_MSB, ICD_RES, ICD_SIGN)
                                list_para.append(float_word1)
                            else:
                                list_para.append("")
                        else:
                            list_para.append("")

        return list_para

    def logic_binary_decode(self, filedata, count, ICD_number, \
                            ICD_MSB, ICD_LSB, ICD_ONE_LOGIC, ICD_ZERO_LOGIC):

        worddata = filedata[count+ICD_number:count+ICD_number+2]
        #print headworddata
        int_word1 = struct.unpack("<h", worddata)[0]
        int_word1 = int_word1 >> (ICD_LSB-1)
        Remove_MSB = 2 ** (ICD_MSB - ICD_LSB + 1) -1
        int_word1 = int_word1 & Remove_MSB
        result = 1
        if ICD_ONE_LOGIC <> ICD_ZERO_LOGIC:
            if int_word1 == 1:
                result = ICD_ONE_LOGIC
            elif int_word1 == 0:
                result = ICD_ZERO_LOGIC
        else:
            result = int_word1

        return result

    def frame_logic(self, frame_number, filedata, ICD_MSB, ICD_LSB, ICD_WORD, ICD_SUBF, ICD_SUPF,\
                    ICD_ONE_LOGIC, ICD_ZERO_LOGIC):

        ICD_number = (ICD_WORD-1) *2
        list_para = []
        #print type(filedata)
        #print len(filedata)
        for count in range(0, len(filedata), frame_number*2):
            headworddata = filedata[count:count + 2]
            #print headworddata
            headword = struct.unpack("<h", headworddata)[0]
            sycword_list = [583, 1464, 2631, 3512, -32185]
            if headword in sycword_list:
                #print "headword: %d" % headword
                if ICD_SUPF == 0:
                    if ICD_SUBF == 0:
                        float_word1 = self.logic_binary_decode(filedata, count, ICD_number, \
                                                         ICD_MSB, ICD_LSB, ICD_ONE_LOGIC, ICD_ZERO_LOGIC)
                        list_para.append(float_word1)
                    else:
                        if ICD_SUBF == (sycword_list.index(headword) + 1 ):
                            float_word1 = self.logic_binary_decode(filedata, count, ICD_number, \
                                                         ICD_MSB, ICD_LSB, ICD_ONE_LOGIC, ICD_ZERO_LOGIC)
                            list_para.append(float_word1)
                        else:
                            list_para.append("")
                elif ICD_SUPF <> 0:
                    if frame_number == 512 :
                        SUPF_word = self.SUPF_binary_decode(filedata, \
                                                            (int(count/(4*frame_number*2)))*4*frame_number*2,
                                                            (499-1)*2, 9, 12, 1)
                    else:
                        SUPF_word = self.SUPF_binary_decode(filedata, \
                                                            (int(count/(4*frame_number*2)))*4*frame_number*2 + 2*frame_number*2,
                                                            (256-1)*2, 9, 12, 1)

                    SUPF_word = SUPF_word +1
                    #print "SUPF_word: %d" % SUPF_word
                    if ICD_SUBF == 0:
                        if SUPF_word == ICD_SUPF:
                            float_word1 = self.logic_binary_decode(filedata, count, ICD_number, \
                                                         ICD_MSB, ICD_LSB, ICD_ONE_LOGIC, ICD_ZERO_LOGIC)
                            list_para.append(float_word1)
                        else:
                            list_para.append("")
                    elif ICD_SUBF <> 0:
                        if SUPF_word == ICD_SUPF:
                            #print SUPF_word
                            #print sycword_list.index(headword) + 1
                            if ICD_SUBF == (sycword_list.index(headword) + 1 ):
                                float_word1 = self.logic_binary_decode(filedata, count, ICD_number, \
                                                         ICD_MSB, ICD_LSB, ICD_ONE_LOGIC, ICD_ZERO_LOGIC)
                                list_para.append(float_word1)
                            else:
                                list_para.append("")
                        else:
                            list_para.append("")

        return list_para

class MERGE_DECODE_LIST():

    def __init__(self):
        pass

    def open_csv_and_merge(self, filedata, csv_file_name, plane_config, num_logic):
        wqar_decode = WQAR_DECODE()
        list_all_para = []
        #读取csv逻辑参数列表，解码大量逻辑参数
        f = open(csv_file_name,'rb')
        reader = csv.reader(f)
        #对参数ID号统一排序
        if num_logic == "logic":
            if plane_config == 256 :
                para_id_number = 475
            else:
                para_id_number = 633
        else:
            para_id_number = 1
        oil_1_list = range(275,276,1)
        #oil_2_list = range(173,181,1)
        #oil_1_list.extend(oil_2_list)
        #oil_1_list.append(199)
        #need_list_1 = range(233,243,1)
        #need_list_1.append(184)
        #oil_1_list.extend(need_list_1)
        need_list = [50,54,275]
        #print need_list
        for row in reader:
            if reader.line_num == 1:
                    continue
            #if para_id_number in need_list:
            if True:
                #读取csv参数列表，解码数值参数
                if num_logic == 'number':
                    list_single_para = wqar_decode.frame(plane_config, filedata,
                                                     ICD_MSB=int(row[2]),
                                                     ICD_LSB=int(row[3]),
                                                     ICD_WORD=int(row[4]),
                                                     ICD_SUBF=int(row[5]),
                                                     ICD_SUPF=int(row[6]),
                                                     ICD_RES=float(row[9]),
                                                    ICD_SIGN=row[1])
                    #插入单位
                    list_single_para.insert(0, row[7])
                #读取csv参数列表，解码逻辑值值参数
                elif num_logic == 'logic':
                    list_single_para = wqar_decode.frame_logic(plane_config, filedata,
                                                            ICD_MSB = int(row[1]),
                                                            ICD_LSB = int(row[2]),
                                                            ICD_WORD = int(row[3]),
                                                            ICD_SUBF = int(row[4]),
                                                            ICD_SUPF = int(row[5]),
                                                            ICD_ONE_LOGIC = row[6],
                                                            ICD_ZERO_LOGIC = row[7])
                    #插入空行，作为单位行
                    list_single_para.insert(0, '')

                para_name = str(para_id_number) + ':' + row[0]
                list_single_para.insert(0, para_name)
                list_all_para.append(list_single_para)
            para_id_number = para_id_number + 1
        return list_all_para


    def all_decode_list(self, path, file_name):

        allstarttime = time.time()
        merge_decode_list = MERGE_DECODE_LIST()

        #单位电脑路径
        WQAR512_SERISE_list = AC_WQAR_CONFIG().WQAR_7_SERISE_list
        WQAR256_SERISE_list = AC_WQAR_CONFIG().WQAR_3C_SERISE_list

        #初始化缓存列表
        list_single_para = []
        list_all_para = []
        single_path = path + '/' + file_name + '/' + 'raw.dat'
        if os.path.exists(single_path):
            file_object = open(single_path,'rb')
            filedata = file_object.read()
            file_object.close()
        else:
            print u"there is no raw.dat:" + file_name
            return

        if file_name[0:6] in WQAR512_SERISE_list:
            starttime = time.clock()
            #读取csv参数列表，解码大量数值参数
            list_number = merge_decode_list.open_csv_and_merge(filedata,
                                                               os.path.join(cur_file_dir(), '737-7 numeric.csv'),
                                                               512,
                                                               'number')

            #读取csv逻辑参数列表，解码大量逻辑参数
            list_logic = merge_decode_list.open_csv_and_merge(filedata,
                                                              os.path.join(cur_file_dir(), '737-7 LOGIC.csv'),
                                                              512,
                                                              'logic')
            list_number.extend(list_logic)
            list_all_para = list_number

        if file_name[0:6] in WQAR256_SERISE_list:
            starttime = time.clock()
            #读取csv参数列表，解码大量数值参数
            list_number = merge_decode_list.open_csv_and_merge(filedata,
                                                               os.path.join(cur_file_dir(), '737-3C NUM.csv'),
                                                               256,
                                                               'number')

            #读取csv逻辑参数列表，解码大量逻辑参数
            list_logic = merge_decode_list.open_csv_and_merge(filedata,
                                                              os.path.join(cur_file_dir(), '737-3C LOGIC.csv'),
                                                              256,
                                                              'logic')
            list_number.extend(list_logic)
            list_all_para = list_number

        list_all_para_turn = map(list, zip(*list_all_para))
        return list_all_para_turn



    def save_to_csv(self, list_all_para_turn, file):
        numpy_arr = numpy.array(list_all_para_turn)
        xlsx_start_time = time.clock()
        #df_s = DataFrame(numpy_arr)
        #df_s.to_excel(file + '.xlsx', sheet_name='Sheet1')
        numpy.savetxt(file + '.csv', numpy_arr, fmt="%s", delimiter=",")
        xlsx_end_time = time.clock()
        print "%s save csv cost：%f" % (file, xlsx_end_time - xlsx_start_time)

'''
if __name__=="__main__":
    decode_list = MERGE_DECODE_LIST()
    list_turn = decode_list.all_decode_list(r'G:\QAR_DATA\append_upload', 'B-5202_20160516035349.wgl')
    decode_list.save_to_csv(list_turn, '5202_CA1638')
'''