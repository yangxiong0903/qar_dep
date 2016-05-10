#coding=utf-8
import arrow

def arrow_replace(time_number, int_number, time_type):
    sector_number = arrow.get(time_number, 'YYYYMMDDHHmmss')
    if time_type == 'hours':
        sector_number = sector_number.replace(hours = int_number)
    elif time_type == 'days':
        sector_number = sector_number.replace(days = int_number)
    else:
        return
    sector_number = sector_number.format('YYYYMMDDHHmmss')
    return sector_number