from mftool import Mftool
from utils.utility import get_friday, get_thursday, get_today, get_yesterday_date, is_holiday, is_tuesday
import json
from itertools import islice

mf = Mftool()


def fetch_mf_names(keyword):
    result = []
    keyword = keyword.lower()
    with open('latest-funds.json', 'r') as file:
        funds = json.load(file)
        keyword_list = keyword.split(' ');
        print(keyword_list)
        for key, val in funds.items():
            found = True
            for key_item in keyword_list:
                if key_item not in val.lower():
                    found = False
                    break
            if (found):
                result.append(dict(
                    mf_code= key,
                    mf_name= val
                ))
    
    total_size = len(result)
    top_10_mf = result[:10]
    return True, total_size, top_10_mf


def fetch_scheme_info(code):
    
    if (not mf.is_valid_code(code)):
        return False, 'Is not a valid mutual fund code', '-1'
    
    quote = mf.get_scheme_quote(code)
    return True, quote.get('last_updated'), quote.get('nav')

def calculate_return(code, invested, start, end=None):
    
    if not mf.is_valid_code(code):
        return False, 'Is not a valid mutual fund code'

    data = None
    if (end == None):
        data = mf.get_scheme_historical_nav_for_dates(code=code, start_date=start, end_date=get_today()).get('data')
    else :
        data = mf.get_scheme_historical_nav_for_dates(code=code, start_date=start, end_date=end).get('data')
        
    initial_val = float(data[len(data)-1].get('nav'))
    end_val = float(data[0].get('nav'))
    
    return_val = (end_val/initial_val) * invested
    
    return True, return_val

def get_day_change(code, invested):

    if not mf.is_valid_code(code):
        return False, 'Is not a valid mutual fund code'
        
    today_nav = 0
    yesterday_nav = 0
    
    if is_holiday():
        two_days_datas = mf.get_scheme_historical_nav_for_dates(code, start_date=get_thursday(), end_date=get_friday()).get('data')
        
        today_nav = two_days_datas[1].get('nav')
        yesterday_nav = two_days_datas[0].get('nav')
        
    elif is_tuesday():
        friday_datas = mf.get_scheme_historical_nav_for_dates(code, start_date=get_friday(), end_date=get_today()).get('data')
        
        quote = mf.get_scheme_quote(code)
        today_nav = quote.get('nav')
        
        yesterday_nav = friday_datas[0].get('nav')

    else:
        quote = mf.get_scheme_quote(code)
        today_nav = float(quote.get('nav'))
    
        yesterday_nav = mf.get_scheme_historical_nav_for_dates(code, start_date=get_yesterday_date(), end_date=get_today()).get('data')[0].get('nav')
        yesterday_nav = float(yesterday_nav)
    
    final_daychange_val = (float(today_nav) / float(yesterday_nav)) * invested;
    
    return True, final_daychange_val


def get_day_change_in_unit(code, invested_unit):

    if not mf.is_valid_code(code):
        return False, 'Is not a valid mutual fund code'
        
    today_nav = 0
    yesterday_nav = 0
    
    if is_holiday():
        two_days_datas = mf.get_scheme_historical_nav_for_dates(code, start_date=get_thursday(), end_date=get_friday()).get('data')
        
        today_nav = two_days_datas[1].get('nav')
        yesterday_nav = two_days_datas[0].get('nav')
        
    elif is_tuesday():
        friday_datas = mf.get_scheme_historical_nav_for_dates(code, start_date=get_friday(), end_date=get_today()).get('data')
        
        quote = mf.get_scheme_quote(code)
        today_nav = quote.get('nav')
        
        yesterday_nav = friday_datas[0].get('nav')

    else:
        quote = mf.get_scheme_quote(code)
        today_nav = float(quote.get('nav'))
    
        yesterday_nav = mf.get_scheme_historical_nav_for_dates(code, start_date=get_yesterday_date(), end_date=get_today()).get('data')[0].get('nav')
        yesterday_nav = float(yesterday_nav)
    
    final_daychange_val = (float(today_nav) * invested_unit) - (float(yesterday_nav)* invested_unit);
    
    return True, final_daychange_val