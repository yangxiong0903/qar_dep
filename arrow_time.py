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

def arrow_influxdb_format(time_number):
    sector_number = arrow.get(time_number, 'YYYYMMDDHHmmss')
    sector_number = sector_number.format('YYYY-MM-DDTHH:mm:ss')+'Z'
    sector_number = sector_number.encode('utf-8')
    return sector_number

def today_date_for_influxd_sql():
    today = arrow.utcnow().replace(hours=8)
    today_number = today.format('YYYY-MM-DD')
    return today_number