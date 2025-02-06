from services.mf_service import fetch_mf_names, fetch_scheme_info, calculate_return, get_day_change, get_day_change_in_unit
from utils import constants

def get_mf_names(keyword):
    return fetch_mf_names(keyword)

def fetch_scheme_information(code):
    status, last_updated, nav =  fetch_scheme_info(code)
    
    if (status == False):
        return status, constants.NOT_VALID_CODE, '00-00-0000', '-1'
    
    return status, 'Successfully fetched', last_updated, nav

def calculate_return_scheme(code, invested, start, end):
    status, return_value = calculate_return(code, invested, start, end)
    
    if (status == False):
        return status, constants.NOT_VALID_CODE, '-1'
    
    return status, constants.SUCCESSFULL, return_value

def calculate_bulk_return_scheme(datas, start, end):
    
    total_return_amount = 0
    total_invested_amount = 0
    
    for investment_data in datas:
        
        code = investment_data.get('code')
        invested = investment_data.get('invested')
        
        
        total_invested_amount += invested
        status, return_amount = calculate_return(code, invested, start, end)
        
        if (status == False):
            return status, constants.NOT_VALID_CODE, '-1', '-1'
        
        total_return_amount += return_amount

    percentage_change = (total_return_amount / total_invested_amount) * 100;
    
    return True, constants.SUCCESSFULL, total_return_amount, percentage_change

def get_day_change_info(code, invested):
    status, daychange = get_day_change(code, invested)
    
    if (status == False):
        return status, constants.NOT_VALID_CODE, '-1'
    
    return status, constants.SUCCESSFULL, daychange

def get_bulk_day_change_info(datas):

    total_return = 0;
    
    for investement_datas in datas:
        
        invested = investement_datas.get(constants.INVESTED)
        code = investement_datas.get(constants.CODE)
        
        status, return_amount = get_day_change(code, invested)
        
        if (status == False):
            return status, constants.NOT_VALID_CODE, '-1'
        
        total_return += return_amount
        
    return False, constants.SUCCESSFULL, total_return

def get_bulk_day_change_unit_info(datas):

    total_return = 0;
    
    for investement_datas in datas:
        
        invested_unit = investement_datas.get(constants.INVESTED_UNIT)
        code = investement_datas.get(constants.CODE)
        
        status, return_amount = get_day_change_in_unit(code, invested_unit)
        
        if (status == False):
            return status, constants.NOT_VALID_CODE, '-1'
        
        total_return += return_amount
        
    return False, constants.SUCCESSFULL, total_return