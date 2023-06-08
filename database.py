# 0608 - restful API 구현

import pymysql
from flask import Flask, render_template, request
from flask_restx import Resource, Api

db = pymysql.connect(host="localhost",
                     port=3306,
                     user='root',
                     passwd='', # 업로드 시 삭제
                     db='mysql',
                     charset='utf8')

cursor = db.cursor()

sql = "select * from 제품"

cursor.execute(sql)

data_list = cursor.fetchall()

app = Flask(__name__)
# api = Api(app)

@app.route('/')
def index():
    sql = "select * from 제품"
    cursor.execute(sql)
    data_list = cursor.fetchall()

    return render_template('index.html', data_list=data_list)

if __name__=="__main__":
    app.run(debug=True)