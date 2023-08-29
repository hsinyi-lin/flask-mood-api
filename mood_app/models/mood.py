from bson.objectid import ObjectId
from ..utils.helpers import generate_reply, analyze_sentiment

import datetime


class MoodModel:
    @staticmethod
    def find_mood_by_id_and_user(mood_col, mood_id, user_email):
        return mood_col.find_one({'_id': ObjectId(mood_id), 'email': user_email})

    @staticmethod
    def find_today_mood(mood_col, user_email, start_of_day, end_of_day):
        return mood_col.find_one({
            'email': user_email,
            'createTime': {'$gte': start_of_day, '$lte': end_of_day}
        })

    @staticmethod
    def find_filtered_moods(mood_col, user_email, mood_id, start_of_month, end_of_month):
        pipeline = [
            {
                '$match': {
                    'email': user_email,
                    'mood_id': mood_id,
                    'createTime': {'$gte': start_of_month, '$lt': end_of_month}
                }
            }
        ]
        return list(mood_col.aggregate(pipeline))
    
    @staticmethod
    def update_existing_mood(mood_col, current_user, existing_mood, data):
        label_id, label, score = analyze_sentiment(data['content'])
        
        updated_data = {
            'updateTime': datetime.datetime.now(),
            'content': data['content'],
            'score': float(score),
            'mood_id': label_id,
            'mood_label': label,
            'reply': generate_reply(data['content'])
        }

        mood_col.update_one(
            {'_id': existing_mood['_id']}, 
            {'$set': updated_data}
        )

        updated_mood = MoodModel.find_mood_by_id_and_user(mood_col, existing_mood['_id'], current_user)
        updated_mood['_id'] = str(updated_mood['_id'])

        return updated_mood

    @staticmethod
    def create_new_mood(mood_col, current_user, data):
        label_id, label, score = analyze_sentiment(data['content'])
        reply = generate_reply(data['content'])

        current_time = datetime.datetime.now()

        new_mood = {
            'email': current_user,
            'content': data['content'],
            'createTime': current_time,
            'updateTime': current_time,
            'score': float(score),
            'mood_id': label_id,
            'mood_label': label,
            'reply': reply
        }

        insert_result = mood_col.insert_one(new_mood)

        new_mood['_id'] = str(insert_result.inserted_id)
        return new_mood
