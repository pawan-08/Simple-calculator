from flask import Flask, render_template, request, redirect
import pymysql

app = Flask(__name__)

# Connect to MySQL using XAMPP
def get_db_connection():
    return pymysql.connect(host='localhost',
                           user='root',
                           password='',
                           db='simple calculator',
                           charset='utf8mb4',
                           cursorclass=pymysql.cursors.DictCursor)

@app.route('/', methods=['GET', 'POST'])
def index():
    result = None
    if request.method == 'POST':
        num1 = float(request.form['num1'])
        num2 = float(request.form['num2'])
        operation = request.form['operation']

        if operation == 'add':
            result = num1 + num2
        elif operation == 'subtract':
            result = num1 - num2
        elif operation == 'multiply':
            result = num1 * num2
        elif operation == 'divide':
            result = num1 / num2 if num2 != 0 else 'Error'

        # Save to DB
        conn = get_db_connection()
        with conn.cursor() as cursor:
            sql = "INSERT INTO calculations (num1, num2, operation, result) VALUES (%s, %s, %s, %s)"
            cursor.execute(sql, (num1, num2, operation, str(result)))
            conn.commit()
        conn.close()

    return render_template('index.html', result=result)

if __name__ == '__main__':
    app.run(debug=True)
