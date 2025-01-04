from datetime import date, timedelta

today = date.today()

def is_tuesday():
    if date.today().strftime("%a") in ['Tue']:
        return True
    else:
        return False
    
def get_thursday():
    days = {'Sat': 1, 'Sun': 2, 'Mon': 3}
    diff = int(days[date.today().strftime("%a")])
    return (date.today() - timedelta(days=diff+1)).strftime("%d-%m-%Y")

def get_yesterday_date():
    yesterday = today - timedelta(days=2)
    return str(yesterday.strftime('%d-%m-%Y'))

def is_holiday():
    if date.today().strftime("%a") in ['Sat', 'Sun', 'Mon']:
        return True
    else:
        return False

def get_friday():
    days = {'Sat': 1, 'Sun': 2, 'Mon': 3}
    diff = int(days[date.today().strftime("%a")])
    return (date.today() - timedelta(days=diff)).strftime("%d-%m-%Y")

def get_today():
    return (date.today() - timedelta(days=1)).strftime("%d-%m-%Y")
