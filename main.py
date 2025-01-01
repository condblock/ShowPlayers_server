import sqlite3
from flask_cors import CORS
from configparser import ConfigParser
import logging
from datetime import datetime
import os
from webhook import send_webhook
from db.db import insert_player, get_players

# init
# get webhook url
config = ConfigParser()
config.read('conf.ini')
webhook_url = config['urls']['webhook_url']

# generate log file
current_date = datetime.now().strftime("%Y-%m-%d")
log_file_name = f"app_{current_date}.log"  # 예: app_2024-03-14.log
log_file_path = os.path.join("logs", log_file_name)

# generate log dir
os.makedirs(os.path.dirname(log_file_path), exist_ok=True)

# set handlers
logger = logging.getLogger("Logger")
logger.setLevel(logging.INFO)

console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
file_handler = logging.FileHandler(log_file_path)

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

file_handler.setFormatter(formatter)
console_handler.setFormatter(formatter)

# add handlers
logger.addHandler(console_handler)
logger.addHandler(file_handler)

conn = sqlite3.connect('players.db', check_same_thread=False)
cur = conn.cursor()

# db formatter
def formatter(list):
    text = ''
    for i in list:
        text += f'이름: {i[1]}\t학교: {i[2]}\t시작 가능 시간: {i[3]}\n'
    return text

# create web
from flask import Flask, request, render_template

app = Flask(__name__)
CORS(app)

@app.route("/")
def index():
    datas = get_players(cur=cur, logger=logger)
    return render_template('index.html', data_list=datas)

@app.route('/form', methods=['GET', 'POST'])
def form():
    if request.method == 'POST':
        name = request.form['name']
        school = request.form['school']
        period = request.form['period']
        hour = request.form['hour']
        minute = request.form['minute']
        if period == 'PM':
            hour = str(int(hour) + 12)
        startTime = datetime.now().replace(hour=int(hour), minute=int(minute), second=0, microsecond=0)
        insert_player(cur=cur, logger=logger, name=name, school=school, startTime=startTime)
        send_webhook(webhook_url=webhook_url, message=f"{name}님이 새로 등록했습니다!\n{formatter(get_players(cur=cur, logger=logger))}", logger=logger)
        return render_template('complete.html')
    return render_template('form.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=80)