# 0613 - 테이블 중복 생성, 제품 테이블 insert, delete 가능하게 구현, 함수 중복 사용

import pymysql
from flask import Flask, render_template, request, jsonify
from flask_restx import Resource, Api

db = pymysql.connect(host="localhost",
                     port=3306,
                     user='root',
                     passwd='sarah164!!', # 업로드 시 삭제
                     db='mysql',
                     charset='utf8')

app = Flask(__name__)
# api = Api(app)

# 메인 페이지
@app.route("/")
def main():
    return render_template("index.html")

# 제품 테이블
@app.route('/product')
def Product():
    # select
    cursor_product = db.cursor()
    sql_product = "select * from 제품"
    cursor_product.execute(sql_product)
    product = cursor_product.fetchall()   # fetchall = 결과 가져오는 함수

    # # insert
    # sql_insert = "insert into 제품 (제품명, 제품가격) values (%s, %d)"
    # value_insert = ("초코라떼", "5000")
    # db.commit()

    return render_template('product.html', product_data=product)

# 고객 테이블
@app.route('/customer')
def Customer():
    cursor_cus = db.cursor()
    sql_cus = "select * from 고객"
    cursor_cus.execute(sql_cus)
    customer = cursor_cus.fetchall()

    return render_template('customer.html', customer_data=customer)

# 주문 테이블
@app.route('/order')
def Order():
    cursor_order = db.cursor()
    sql_order = "select * from 주문"
    cursor_order.execute(sql_order)
    order = cursor_order.fetchall()

    return render_template('order.html', order_data=order)

# 직원 테이블
@app.route('/employee')
def Employee():
    cursor_employee = db.cursor()
    sql_employee = "select * from 직원"
    cursor_employee.execute(sql_employee)
    employee = cursor_employee.fetchall()

    return render_template('employee.html', employee_data=employee)

# 판매 테이블
@app.route('/sales')
def Sales():
    cursor_sales = db.cursor()
    sql_sales = "select * from 판매"
    cursor_sales.execute(sql_sales)
    sales = cursor_sales.fetchall()

    return render_template('sales.html', sales_data=sales)

# 재고 테이블
@app.route('/inventory')
def Inventory():
    cursor_inventory = db.cursor()
    sql_inventory = "select * from 재고"
    cursor_inventory.execute(sql_inventory)
    inventory = cursor_inventory.fetchall()

    return render_template('inventory.html', inventory_data=inventory)

if __name__=="__main__":
    app.run(debug=True)