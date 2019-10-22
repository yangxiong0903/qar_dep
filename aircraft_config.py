#coding=utf-8

class AC_WQAR_CONFIG:

    def __init__(self):
        # 机号构型判断
        self.WQAR_3C_SERISE_list = ["B-2612","B-2613","B-2700",
                                    "B-5201","B-5202","B-5203",
                                    "B-5214","B-5217","B-5220",
                                    "B-5325","B-5327","B-5329",
                                    "B-5390","B-5392","B-5398",
                                    "B-5426","B-5443","B-5477",
                                    "B-5486","B-5496","B-5198",
                                    "B-2649",
                                    "B-5226"]

        self.WQAR_7_SERISE_list = ["B-1976","B-1956","B-5803",
                                    "B-5679","B-1527","B-1738",
                                    "B-5622","B-1942","B-1959",
                                    "B-5682","B-5297","B-5296",
                                    "B-5583","B-1768","B-1765",
                                    "B-1763","B-5582","B-1531",
                                    "B-6496","B-6497","B-7181",
                                    "B-7892","B-7595","B-7596",
                                    "B-7598","B-7597","B-7890",
                                    "B-7893","B-7895","B-7896",
                                    "B-7897","B-7891","B-1417",
                                    "B-1416","B-1419",
                                    "B-1217","B-1458",
                                    "B-1764","B-1769","B-1945",
                                    "B-1947","B-206T","B-5680"]


    def juge_config(self, str_ac_number):
        if str_ac_number in self.WQAR_3C_SERISE_list:
            return "737_3C"
        elif str_ac_number in self.WQAR_7_SERISE_list:
            return "737_7"
        else:
            return False

    def all_aircraft(self):
        aircraft_list = self.WQAR_3C_SERISE_list + self.WQAR_7_SERISE_list
        return aircraft_list