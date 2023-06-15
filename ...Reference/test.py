from flask import Flask, render_template, request, jsonify
import pymysql

app = Flask(__name__)

# MySQL 데이터베이스 연결 설정
db = pymysql.connect(
    host="localhost",
                     port=3306,
                     user='root',
                     passwd='sarah164!!', # 업로드 시 삭제
                     db='mysql',
                     charset='utf8',
    cursorclass=pymysql.cursors.DictCursor
)

@app.route('/')
def index():
    return render_template('product_management.html')

@app.route('/add_product', methods=['POST'])
def add_product():
    try:
        # 요청 데이터 가져오기
        name = request.form.get('name')
        price = request.form.get('price')

        cursor = db.cursor()

        # 제품 삽입
        sql_insert = "INSERT INTO your_table_name (name, price) VALUES (%s, %s)"
        cursor.execute(sql_insert, (name, price))
        db.commit()

        cursor.close()

        return jsonify({'message': 'Product added successfully'})

    except Exception as e:
        return jsonify({'error': str(e)})

@app.route('/delete_product', methods=['POST'])
def delete_product():
    try:
        # 요청 데이터 가져오기
        product_id = request.form.get('product_id')

        cursor = db.cursor()

        # 제품 삭제
        sql_delete = "DELETE FROM your_table_name WHERE id = %s"
        cursor.execute(sql_delete, (product_id,))
        db.commit()

        cursor.close()

        return jsonify({'message': 'Product deleted successfully'})

    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    app.run()