from mftool import Mftool
from utils import utility

mf = Mftool()


def fetch_mf_names(keyword):
    result = mf.get_available_schemes(keyword)
    total_size = len(result)
    top_10_mf = list(result.items())[:10]
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
        data = mf.get_scheme_historical_nav_for_dates(code=code, start_date=start, end_date=utility.get_today()).get('data')
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
    
    if utility.is_holiday():
        two_days_datas = mf.get_scheme_historical_nav_for_dates(code, start_date=utility.get_thursday(), end_date=utility.get_friday()).get('data')
        
        today_nav = two_days_datas[1].get('nav')
        yesterday_nav = two_days_datas[0].get('nav')
        
    elif utility.is_tuesday():
        friday_datas = mf.get_scheme_historical_nav_for_dates(code, start_date=utility.get_friday(), end_date=utility.get_today()).get('data')
        
        quote = mf.get_scheme_quote(code)
        today_nav = quote.get('nav')
        
        yesterday_nav = friday_datas[0].get('nav')

    else:
        quote = mf.get_scheme_quote(code)
        today_nav = float(quote.get('nav'))
    
        yesterday_nav = mf.get_scheme_historical_nav_for_dates(code, start_date=utility.get_yesterday_date(), end_date=utility.get_current_date()).get('data')[0].get('nav')
        yesterday_nav = float(yesterday_nav)
    
    final_daychange_val = (float(today_nav) / float(yesterday_nav)) * invested;
    
    return True, final_daychange_val