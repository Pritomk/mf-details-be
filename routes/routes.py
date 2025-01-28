from flask import Blueprint, request, jsonify, abort
from controllers.mf_controller import get_mf_names, fetch_scheme_information, calculate_return_scheme, get_day_change_info, calculate_bulk_return_scheme, get_bulk_day_change_info
from utils import constants
from flask_cors import cross_origin

mf_routes = Blueprint('mf_routes',__name__)

@mf_routes.route('/', methods=['GET'])
@cross_origin(supports_credentials=True)
def greet():
    return 'Server is working'

@mf_routes.route('/search', methods=['GET'])
@cross_origin(supports_credentials=True)
def search_mf_names():
    keyword = request.args.get(constants.KEYWORD, default='tata')

    if (len(keyword) < 3):
        abort(404)
        abort(constants.LENGTH_SHORT)
        return
    
    status, total_size, mf_list = get_mf_names(keyword)
    return jsonify({
        'status': status,
        'result': mf_list,
        'size': total_size
    })
    
@mf_routes.route('/latest-info', methods=['GET'])
@cross_origin(supports_credentials=True)
def get_latest_info():
    mf_code = request.args.get('code', default=-1)
    
    if (mf_code == -1):
        abort(404)
        abort(constants.NOT_VALID_CODE)
        return
    
    status, msg, last_updated, nav = fetch_scheme_information(mf_code)
    return jsonify({
        "status": status,
        "lastUpdated": last_updated,
        "nav": nav,
        "message": msg
    })
    
@mf_routes.route('/return', methods=['POST'])
@cross_origin(supports_credentials=True)
def get_return():
    json = request.get_json()
    
    invested = json.get(constants.INVESTED)
    start_date = json.get(constants.START)
    end_date = json.get(constants.END)
    mf_code = json.get(constants.CODE)
    
    
    
    status, msg, total_return = calculate_return_scheme(mf_code, invested, start_date, end_date)
    
    return jsonify({
        "status": status,
        "return": total_return,
        "message": msg
    })

@mf_routes.route('/daychange', methods=['POST'])
@cross_origin(supports_credentials=True)
def get_day_change_information():
    json = request.get_json()
    
    invested = json.get(constants.INVESTED)
    mf_code = json.get(constants.CODE)

    status, msg, day_change = get_day_change_info(mf_code, invested)
    return jsonify({
        "status": status,
        "message": msg,
        "dayChange": day_change
    })

@mf_routes.route('/bulk-return', methods=['POST'])
@cross_origin(supports_credentials=True)
def get_bulk_return():
    json = request.get_json()
    
    datas = json.get(constants.DATAS)
    start = json.get(constants.START)
    end = json.get(constants.END)
    
    status, msg, total_return, percentage_change = calculate_bulk_return_scheme(datas, start, end)
    
    return jsonify({
        "status": status,
        "message": msg,
        "return": total_return,
        "percentageChange": percentage_change
    })   

@mf_routes.route('/bulk-daychange', methods=['POST'])
@cross_origin(supports_credentials=True)
def get_bulk_daychange():
    
    json = request.get_json()
    
    datas = json.get(constants.DATAS)
    
    status, msg, total_return =  get_bulk_day_change_info(datas)
    
    return jsonify({
        "status": status,
        "message": msg,
        "return": total_return
    })

def register_routes(app):
    app.register_blueprint(mf_routes)