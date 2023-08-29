from flask import Blueprint, request

from ..extensions import mongo
from ..utils.token import token_required
from ..utils.response import *
from ..utils.helpers import *
from ..models.mood import MoodModel

import datetime, calendar


mood = Blueprint('mood', __name__)


@mood.route('/', methods=['POST'])
@token_required
def add_mood(current_user):
    data = request.get_json()
    
    mood_col = mongo.db.mood
    start_of_day, end_of_day = get_today_time_range()
    
    existing_mood = MoodModel.find_today_mood(mood_col, current_user, start_of_day, end_of_day)
    
    if existing_mood:
        updated_mood = MoodModel.update_existing_mood(mood_col, current_user, existing_mood, data)
        return success_response(updated_mood), 200
    
    new_mood = MoodModel.create_new_mood(mood_col, current_user, data)
    return success_response(new_mood), 201


@mood.route('/<id>', methods=['GET'])
@token_required
def get_mood(current_user, id):
    mood_col = mongo.db.mood
    mood = MoodModel.find_mood_by_id_and_user(mood_col, id, current_user)

    if not mood:
        return error_response('沒有此筆資料'), 404
    
    mood['_id'] = str(mood['_id'])

    return success_response(mood), 200


@mood.route('/today', methods=['GET'])
@token_required
def get_today_mood(current_user):

    start_of_day, end_of_day = get_today_time_range()
    
    mood_col = mongo.db.mood
    mood = MoodModel.find_today_mood(mood_col, current_user, start_of_day, end_of_day)
    
    print(current_user)

    if not mood:
        return error_response('無任何資料'), 404
    
    mood['_id'] = str(mood['_id'])

    return success_response(mood), 200



@mood.route('/<int:mood_id>/<int:year>/<int:month>', methods=['GET'])
@token_required
def get_filtered_moods(current_user, mood_id, year, month):
    start_of_month = datetime.datetime(year, month, 1)
    end_of_month_day = calendar.monthrange(year, month)[1]
    end_of_month = datetime.datetime(year, month, end_of_month_day, 23, 59, 59)

    mood_col = mongo.db.mood
    moods = MoodModel.find_filtered_moods(mood_col, current_user, mood_id, start_of_month, end_of_month)
    
    print(moods)
    for mood in moods:
        mood['_id'] = str(mood['_id'])

    return success_response(moods), 200
