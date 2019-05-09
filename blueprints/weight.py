from flask import Blueprint, request, url_for, render_template, Response
from common.database import Database
import json

#import error as Errors

weight_blueprint = Blueprint('weight', __name__)


@weight_blueprint.route('/register', methods=['POST', 'GET'])
def register_weight():
    if request.method == 'GET':
        status, avg_values, day_in_week, unit = Database.getHistoryInWeeks(0)
        if status == 'OK' and avg_values and unit:
            return render_template('index.html', last_week_avg=avg_values[0], unit=unit)
        return render_template('index.html')
    elif request.method == 'POST':
        content = request.get_json()
        todays_weight = content['todays_weight']
        unit = content['unit']
        result, last_week_avg = Database.saveToDb(todays_weight, unit)
        if result == 'OK':
            return Response(json.dumps({"weight": todays_weight, "unit": unit, 'last_week_avg': last_week_avg if last_week_avg else None ,"error":None}),status=201, mimetype="application/json")
        else:
            return Response(json.dumps({'error':'There was an error'}), status=500, mimetype="application/json")


@weight_blueprint.route('/history', methods=['GET'])
def show_history():
    options = [i for i in range(1,100)]
    return render_template('history.html', options=options)


@weight_blueprint.route('/historydays', methods=['GET'])
def show_days():
    amount = request.args.get('amount')
    result, values, days, unit = Database.getHistoryInDays(int(amount)-1)
    if result == 'OK':
        return Response(json.dumps({'unit': unit, 'values': values, 'time_unit': days, 'error': None}), status=200, mimetype="application/json")
    else:
        return Response(json.dumps({'error':'There was an error'}), status=500, mimetype="application/json")


@weight_blueprint.route('/historyweeks', methods=['GET'])
def show_weeks():
    amount = request.args.get('amount')
    result, avg_values, day_in_week, unit = Database.getHistoryInWeeks(int(amount)-1)
    if result == 'OK':
        return Response(json.dumps({'unit': unit, 'values': avg_values, 'time_unit': day_in_week, 'error': None}), status=200, mimetype="application/json")
    else:
        return Response(json.dumps({'error':'There was an error'}), status=500, mimetype="application/json")
