#coding=utf-8

from influxdb import DataFrameClient
from IP_judge import LOCAL

def add_sign(string1):
    string2 ="\"" + str(string1) + "\""
    return string2

def add_single_quotes(string1):
    string2 = "'" + str(string1) + "'"
    return string2

def merge_str(str1, str2):
    result = str1 + "," + str2
    return result

class influxDB_interface():

    def __init__(self):
        pass

    def DFclient(self, dbname):
        str_IP_address = LOCAL().server_ip()
        user = ''
        password = ''
        clientdb = DataFrameClient(str_IP_address, 8086, user, password, dbname)
        return clientdb

    def inf_query(self, dbname, value, mes, where_str = ''):
        sql_str = "SELECT " + value + " FROM " + mes + where_str + " ORDER BY time DESC "
        result = self.DFclient(dbname).query(sql_str)
        return result

    def limit_query(self, dbname, value, mes):
        sql_str = "SELECT " + value + " FROM " + mes + " ORDER BY time DESC LIMIT 7"
        result = self.DFclient(dbname).query(sql_str)
        return result

    def list_query(self, dbname, list, mes, AC_sector):
        index_str = add_sign('index') + ","
        GMT_str = add_sign('$GMT TIME') + ","
        value_str = reduce(merge_str, map(add_sign, list))
        mes_str = add_sign(mes)
        where_str = " WHERE \"AC_sector\" =" + add_single_quotes(AC_sector)
        sql_str = "SELECT " + index_str + GMT_str + value_str + " FROM " + mes_str + where_str
        result = self.DFclient(dbname).query(sql_str)
        result = result[mes]
        return result

    def show_fields(self, dbname, mes):
        sql_str = "SHOW FIELD KEYS FROM " + mes
        result = self.DFclient(dbname).query(sql_str)
        result = result[mes]
        return result