import sqlite3
from flask_cors import CORS
from configparser import ConfigParser
import logging
from datetime import datetime
import os
from webhook import send_webhook
from db.db import insert_player, get_players, check_player_ip

# init
# get webhook url
config = ConfigParser()
config.read('conf.ini')
webhook_url = config['urls']['webhook_url']

# generate log file
current_date = datetime.now().strftime("%Y-%m-%d")
log_file_name = f"app_{current_date}.log"
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
        text += f'이름: {i[1]}\t학교: {i[2]}\t시작 가능 시간: {i[3]}\t종료 예정 시간: {i[4]}\n'
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
    user_ip = request.remote_addr
    if check_player_ip(cur=cur, logger=logger, ip_address=user_ip):
        return "You have already submitted the form."
    
    if request.method == 'POST':
        name = request.form['name']
        school = request.form['school']
        start_period = request.form['start_period']
        start_hour = request.form['start_hour']
        start_minute = request.form['start_minute']
        end_period = request.form['end_period']
        end_hour = request.form['end_hour']
        end_minute = request.form['end_minute']
        
        if start_period == 'PM' and start_hour != '12':
            start_hour = str(int(start_hour) + 12)
        elif start_period == 'AM' and start_hour == '12':
            start_hour = '00'
        
        if end_period == 'PM' and end_hour != '12':
            end_hour = str(int(end_hour) + 12)
        elif end_period == 'AM' and end_hour == '12':
            end_hour = '00'
        
        startTime = f"{start_hour.zfill(2)}:{start_minute.zfill(2)}"
        endTime = f"{end_hour.zfill(2)}:{end_minute.zfill(2)}"
        
        insert_player(cur, logger, name, school, startTime, endTime, user_ip)
        send_webhook(webhook_url, message=f"{name}님이 새로 등록했습니다!\n{formatter(get_players(cur=cur, logger=logger))}", logger=logger)
        return render_template('complete.html')
    return render_template('form.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=5000)
