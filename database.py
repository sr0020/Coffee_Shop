# 0613-0615 - 각 테이블 생성 및 select 구현, UI 작업
# 0627-0629 - 각 테이블 insert, delete 구현 및 전체 프로토타입 완성

import pymysql
from flask import Flask, render_template, request, jsonify, redirect
from pymysql import IntegrityError

db = pymysql.connect(host="localhost",
                     port=3306,
                     user='root',
                     passwd='', # pw
                     db='mysql',
                     charset='utf8')

app = Flask(__name__)

# 메인 페이지
@app.route("/")
def main():
    return render_template("index.html")

"-------------------------------------------------"

# 제품 테이블
@app.route('/product', methods=['GET', 'POST'])
def Product():

    if request.method == 'POST':
        
        # delete
        product_number = request.form.get('product_number')
        delete_product(product_number)
        
        # insert
        product_number = request.form.get('product_number')
        product_name = request.form.get('product_name')
        product_price = request.form.get('product_price')
        expiry_date = request.form.get('date')
        stock = request.form.get('stock')
        insert_product(product_number, product_name, product_price, expiry_date, stock)

        return redirect('/product')

    # select
    cursor_product = db.cursor()
    sql_product = "select * from 제품"
    cursor_product.execute(sql_product)
    product = cursor_product.fetchall()  

    return render_template('product.html', product_data=product)

# insert product
def insert_product(product_number, product_name, product_price, expiry_date, stock):
    
    # insert
    # select해서 현재 테이블에 존재여부 확인 후 insert
    cursor_insert = db.cursor()
    sql_check_insert = "select * from 제품 where 제품번호 = %s"
    cursor_insert.execute(sql_check_insert, (product_number,))
    result = cursor_insert.fetchone()
    print('insert = ', result) 

    if result:
        print("중복된 제품번호가 이미 존재합니다.") # local
        pass
    elif not any(request.form.values()):
        print("모든 입력 값이 Null입니다. 추가할 값이 없습니다.") # local
        pass
    else:
        sql_insert = "insert into 제품 (제품번호, 제품명, 제품가격, 유통기한, 재고량) VALUES (%s, %s, %s, %s, %s)"
        values = (product_number, product_name, product_price, expiry_date, stock)
        cursor_insert.execute(sql_insert, values)
        db.commit()
        print("추가 완료")

# delete product
def delete_product(product_number):

    # 삭제할 제품이 테이블에 존재하는지 확인
    cursor_check_exist = db.cursor()
    sql_check_delete = "select * from 제품 where 제품번호 = %s"
    cursor_check_exist.execute(sql_check_delete, (product_number,))
    result = cursor_check_exist.fetchone()
    print('delete = ', result)

    # 외래키 제약조건 여부 확인 후 해당되는 경우 삭제 불가 알림
    try:
        cursor_check_foreign = db.cursor()
        sql_check_foreign = "select * from 주문 where 제품번호 = %s"
        cursor_check_foreign.execute(sql_check_foreign, (product_number,))
        result = cursor_check_foreign.fetchone()
        if result:
            print("외래키 제약조건으로 인해 삭제할 수 없습니다.")
            return redirect('/product')
        
    except IntegrityError as e:
        print("IntegrityError:", e)
        return redirect('/product')

    # delete
    cursor_delete = db.cursor()
    sql_delete = " delete from 제품 where 제품번호 = %s"
    cursor_delete.execute(sql_delete, (product_number, ))
    db.commit()
    print("삭제 완료")

    return redirect('/product')

"-------------------------------------------------------"

# 고객 테이블
@app.route('/customer', methods=['GET', 'POST'])
def Customer():

    if request.method == 'POST':
            
        # delete
        membership_number = request.form.get('membership_number')
        delete_customer(membership_number)

        # insert
        membership_number = request.form.get('membership_number')
        customer_name = request.form.get('customer_name')
        phone_number = request.form.get('phone_number')
        birthday = request.form.get('birthday')
        insert_customer(membership_number, customer_name, phone_number, birthday)

        return redirect('/customer')

    # select:
    cursor_cus = db.cursor()
    sql_cus = "select * from 고객"
    cursor_cus.execute(sql_cus)
    customer = cursor_cus.fetchall()

    return render_template('customer.html', customer_data=customer)

# insert customer
def insert_customer(membership_number, customer_name, phone_number, birthday):
    
    # insert
    # select해서 현재 테이블에 존재여부 확인 후 insert
    cursor_insert = db.cursor()
    sql_check_insert = "select * from 고객 where 멤버십번호 = %s"
    cursor_insert.execute(sql_check_insert, (membership_number,))
    result = cursor_insert.fetchone()
    print('insert = ', result)

    if result:
        print("중복된 멤버십 번호가 이미 존재합니다.") # local
        pass
    elif not any(request.form.values()):
        print("모든 입력 값이 Null입니다. 추가할 값이 없습니다.") # local
        pass
    else:
        sql_insert = "insert into 고객 (멤버십번호, 이름, 연락처, 생일) VALUES (%s, %s, %s, %s)"
        values = (membership_number, customer_name, phone_number, birthday)
        cursor_insert.execute(sql_insert, values)
        db.commit()
        print("추가 완료")

# delete customer
def delete_customer(membership_number):

    # 삭제할 제품이 테이블에 존재하는지 확인
    cursor_insert = db.cursor()
    sql_check_delete = "select * from 고객 where 멤버십번호 = %s"
    cursor_insert.execute(sql_check_delete, (membership_number,))
    result = cursor_insert.fetchone()
    print('delete = ', result)

    # 외래키 제약조건 여부 확인 후 해당되는 경우 삭제 불가 알림
    try:
        cursor_check_foreign = db.cursor()
        sql_check_foreign = "select * from 주문 where 고객번호 = %s"
        cursor_check_foreign.execute(sql_check_foreign, (membership_number,))
        result = cursor_check_foreign.fetchone()
        if result:
            print("외래키 제약조건으로 인해 삭제할 수 없습니다.")
            return redirect('/customer')
        
    except IntegrityError as e:
        print("IntegrityError:", e)
        return redirect('/customer')

    # delete
    cursor_delete = db.cursor()
    sql_delete = " delete from 고객 where 멤버십번호 = %s"
    cursor_delete.execute(sql_delete, (membership_number, ))
    db.commit()
    print("삭제 완료")

    return redirect('/customer')

"----------------------------------------------------"

# 주문 테이블
@app.route('/order', methods=['GET', 'POST'])
def Order():

    if request.method == 'POST':
        
        # delete
        order_number = request.form.get('order_number')
        delete_order(order_number)

        # insert
        order_number = request.form.get('order_number')
        order_date = request.form.get('order_date')
        payment_method = request.form.get('payment_method')
        order_quantity = request.form.get('order_quantity')
        product_number = request.form.get('product_number')
        employee_number = request.form.get('employee_number')
        customer_number = request.form.get('customer_number')
        insert_order(order_number, order_date, payment_method, order_quantity, product_number, employee_number, customer_number)

        return redirect('/order')

    # select:
    cursor_order = db.cursor()
    sql_order = "select * from 주문"
    cursor_order.execute(sql_order)
    order = cursor_order.fetchall()

    return render_template('order.html', order_data=order)

# insert order
def insert_order(order_number, order_date, payment_method, order_quantity, product_number, employee_number, customer_number):
    
    # insert
    # select해서 현재 테이블에 존재여부 확인 후 insert
    cursor_insert = db.cursor()
    sql_check_insert = "select * from 주문 where 주문번호 = %s"
    cursor_insert.execute(sql_check_insert, (order_number,))
    result = cursor_insert.fetchone()
    print('insert = ', result)

    if result:
        print("중복된 주문 번호가 이미 존재합니다.") # local
        pass
    elif not any(request.form.values()):
        print("모든 입력 값이 Null입니다. 추가할 값이 없습니다.") # local
        pass
    else:
        sql_insert = "insert into 주문 (주문번호, 주문일시, 결제수단, 주문수량, 제품번호, 직원번호, 고객번호) VALUES (%s, %s, %s, %s, %s, %s, %s)"
        values = (order_number, order_date, payment_method, order_quantity, product_number, employee_number, customer_number)
        cursor_insert.execute(sql_insert, values)
        db.commit()
        print("추가 완료")

# delete order
def delete_order(order_number):

    # 삭제할 제품이 테이블에 존재하는지 확인
    cursor_insert = db.cursor()
    sql_check_delete = "select * from 주문 where 주문번호 = %s"
    cursor_insert.execute(sql_check_delete, (order_number,))
    result = cursor_insert.fetchone()
    print('delete = ', result)

    # delete
    cursor_delete = db.cursor()
    sql_delete = " delete from 주문 where 주문번호 = %s"
    cursor_delete.execute(sql_delete, (order_number, ))
    db.commit()
    print("삭제 완료")

    return redirect('/order')

"----------------------------------------------------"

# 직원 테이블
@app.route('/employee', methods=['GET', 'POST'])
def Employee():

    if request.method == 'POST':
        
        # delete
        employee_number = request.form.get('employee_number')
        delete_employee(employee_number)

        # insert
        employee_number = request.form.get('employee_number')
        employee_name = request.form.get('employee_name')
        position = request.form.get('position')
        employment_date = request.form.get('employment_date')
        contact = request.form.get('contact')
        account_number = request.form.get('account_number')
        start_time = request.form.get('start_time')
        leave_time = request.form.get('leave_time')
        insert_employee(employee_number, employee_name, position, employment_date, contact, account_number, start_time, leave_time)

        return redirect('/employee')

    # select
    cursor_employee = db.cursor()
    sql_employee = "select * from 직원"
    cursor_employee.execute(sql_employee)
    employee = cursor_employee.fetchall()

    return render_template('employee.html', employee_data=employee)

# insert employee
def insert_employee(employee_number, employee_name, position, employment_date, contact, account_number, start_time, leave_time):
    
    # insert
    # select해서 현재 테이블에 존재여부 확인 후 insert
    cursor_insert = db.cursor()
    sql_check_insert = "select * from 직원 where 직원번호 = %s"
    cursor_insert.execute(sql_check_insert, (employee_number,))
    result = cursor_insert.fetchone()
    print('insert = ', result)

    if result:
        print("중복된 직원 번호가 이미 존재합니다.") # local
        pass
    elif not any(request.form.values()):
        print("모든 입력 값이 Null입니다. 추가할 값이 없습니다.") # local
        pass
    else:
        sql_insert = "insert into 직원 (직원번호, 이름, 직급, 입사일, 연락처, 계좌번호, 출근시간, 퇴근시간) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
        values = (employee_number, employee_name, position, employment_date, contact, account_number, start_time, leave_time)
        cursor_insert.execute(sql_insert, values)
        db.commit()
        print("추가 완료")

# delete employee
def delete_employee(employee_number):

    # 삭제할 제품이 테이블에 존재하는지 확인
    cursor_insert = db.cursor()
    sql_check_delete = "select * from 직원 where 직원번호 = %s"
    cursor_insert.execute(sql_check_delete, (employee_number,))
    result = cursor_insert.fetchone()
    print('delete = ', result)

    # 외래키 제약조건 여부 확인 후 해당되는 경우 삭제 불가 알림
    try:
        cursor_check_foreign = db.cursor()
        sql_check_foreign = "select * from 주문 where 직원번호 = %s"
        cursor_check_foreign.execute(sql_check_foreign, (employee_number,))
        result = cursor_check_foreign.fetchone()
        if result:
            print("외래키 제약조건으로 인해 삭제할 수 없습니다.")
            return redirect('/employee')
        
    except IntegrityError as e:
        print("IntegrityError:", e)
        return redirect('/employee')

    # delete
    cursor_delete = db.cursor()
    sql_delete = " delete from 직원 where 직원번호 = %s"
    cursor_delete.execute(sql_delete, (employee_number, ))
    db.commit()
    print("삭제 완료")

    return redirect('/employee')

"-----------------------------------------------------"

# 판매 테이블
@app.route('/sales', methods=['GET', 'POST'])
def Sales():

    if request.method == 'POST':
            
        # delete
        sales_number = request.form.get('sales_number')
        delete_sales(sales_number)

        # insert
        sales_number = request.form.get('sales_number')
        sales_quantity_by_product = request.form.get('sales_quantity_by_product')
        total_sales = request.form.get('total_sales')
        cash_sales = request.form.get('cash_sales')
        card_sales = request.form.get('card_sales')
        insert_sales(sales_number, sales_quantity_by_product, total_sales, cash_sales, card_sales)

    # select
    cursor_sales = db.cursor()
    sql_sales = "select * from 판매"
    cursor_sales.execute(sql_sales)
    sales = cursor_sales.fetchall()

    return render_template('sales.html', sales_data=sales)

# insert sales
def insert_sales(sales_number, sales_quantity_by_product, total_sales, cash_sales, card_sales):
    
    # insert
    # select해서 현재 테이블에 존재여부 확인 후 insert
    cursor_insert = db.cursor()
    sql_check_insert = "select * from 판매 where 판매번호 = %s"
    cursor_insert.execute(sql_check_insert, (sales_number,))
    result = cursor_insert.fetchone()
    print('insert = ', result)

    if result:
        print("중복된 판매 번호가 이미 존재합니다.") # local
        pass
    elif not any(request.form.values()):
        print("모든 입력 값이 Null입니다. 추가할 값이 없습니다.") # local
        pass
    else:
        sql_insert = "insert into 판매 (판매번호, 제품별판매량, 총매출, 현금판매액, 카드판매액) VALUES (%s, %s, %s, %s, %s)"
        values = (sales_number, sales_quantity_by_product, total_sales, cash_sales, card_sales)
        cursor_insert.execute(sql_insert, values)
        db.commit()
        print("추가 완료")

# delete sales
def delete_sales(sales_number):

    # 삭제할 제품이 테이블에 존재하는지 확인
    cursor_insert = db.cursor()
    sql_check_delete = "select * from 판매 where 판매번호 = %s"
    cursor_insert.execute(sql_check_delete, (sales_number,))
    result = cursor_insert.fetchone()
    print('delete = ', result)

    # delete
    cursor_delete = db.cursor()
    sql_delete = " delete from 판매 where 판매번호 = %s"
    cursor_delete.execute(sql_delete, (sales_number, ))
    db.commit()
    print("삭제 완료")

    return redirect('/sales')

"-----------------------------------------------------"

# 재고 테이블
@app.route('/inventory', methods=['GET', 'POST'])
def Inventory():

    if request.method == 'POST':
            
        # delete
        material_number = request.form.get('material_number')
        delete_inventory(material_number)

        # insert
        material_number = request.form.get('material_number')
        material_product_name = request.form.get('material_product_name')
        material_product_price = request.form.get('material_product_price')
        inventory_quantity = request.form.get('inventory_quantity')
        size = request.form.get('size')
        supply_company = request.form.get('supply_company')
        insert_inventory(material_number, material_product_name, material_product_price, inventory_quantity, size, supply_company)

        return redirect('/inventory')

    # select
    cursor_inventory = db.cursor()
    sql_inventory = "select * from 재고"
    cursor_inventory.execute(sql_inventory)
    inventory = cursor_inventory.fetchall()

    return render_template('inventory.html', inventory_data=inventory)

# insert inventory
def insert_inventory(material_number, material_product_name, material_product_price, inventory_quantity, size, supply_company):  
    
    # insert
    # select해서 현재 테이블에 존재여부 확인 후 insert
    cursor_insert = db.cursor()
    sql_check_insert = "select * from 재고 where 원재료제품번호 = %s"
    cursor_insert.execute(sql_check_insert, (material_number,))
    result = cursor_insert.fetchone()
    print('insert = ', result)

    if result:
        print("중복된 원재료 번호가 이미 존재합니다.") # local
        pass
    elif not any(request.form.values()):
        print("모든 입력 값이 Null입니다. 추가할 값이 없습니다.") # local
        pass
    else:
        sql_insert = "insert into 재고 (원재료제품번호, 제품이름, 판매가격, 재고량, 사이즈, 구매업체) VALUES (%s, %s, %s, %s, %s, %s)"
        values = (material_number, material_product_name, material_product_price, inventory_quantity, size, supply_company)
        cursor_insert.execute(sql_insert, values)
        db.commit()
        print("추가 완료")

# delete inventory
def delete_inventory(material_number):

    # 삭제할 제품이 테이블에 존재하는지 확인
    cursor_insert = db.cursor()
    sql_check_delete = "select * from 재고 where 원재료제품번호 = %s"
    cursor_insert.execute(sql_check_delete, (material_number,))
    result = cursor_insert.fetchone()
    print('delete = ', result)

    # delete
    cursor_delete = db.cursor()
    sql_delete = " delete from 재고 where 원재료제품번호 = %s"
    cursor_delete.execute(sql_delete, (material_number, ))
    db.commit()
    print("삭제 완료")

    return redirect('/inventory')

if __name__=="__main__":
    app.run(debug=True)