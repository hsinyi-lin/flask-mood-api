from transformers import pipeline, BertTokenizerFast, AutoModelForSequenceClassification
import datetime, os, openai


def generate_reply(content):
    with open('openai_key.txt', 'r') as file:
        api_key = file.read().strip()

    openai.api_key = api_key

    completion = openai.ChatCompletion.create(
        model='gpt-3.5-turbo',
        messages=[
                {'role': 'system', 'content': '你是一位心理諮商師，專門鼓勵他人，內容不超過40字'},
                {'role': 'user', 'content': '以下為使用者的今日心情，請根據內容給予使用者鼓勵，內容不超過40字' + content}
            ]
    )

    response_message = completion['choices'][0]['message']['content'].strip()
    return response_message


def analyze_sentiment(text_to_analyze):
    tokenizer = BertTokenizerFast.from_pretrained('bert-base-chinese')

    model_path = './mood_app/utils/analysis_model'
    my_model = AutoModelForSequenceClassification.from_pretrained(model_path)
    my_pipe = pipeline(
        'sentiment-analysis',
        model=my_model,
        tokenizer=tokenizer,
    )

    result = my_pipe(text_to_analyze)
    print(result)

    # [{'label': 'neutral', 'score': 0.8533678650856018}]
    label = result[0]['label']
    score = result[0]['score']
    
    labels = ['positive', 'neutral', 'negative']
    label2id = {label: idx for idx, label in enumerate(labels)}

    return label2id[label], label, score


def get_today_time_range():
    today = datetime.datetime.now().date()
    start_of_day = datetime.datetime.combine(today, datetime.datetime.min.time())
    end_of_day = datetime.datetime.combine(today, datetime.datetime.max.time())
    return start_of_day, end_of_day


