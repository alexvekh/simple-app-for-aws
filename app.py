from flask import Flask, render_template, request, redirect
import mysql.connector

app = Flask(__name__)

# Подключение к RDS
db = mysql.connector.connect(
    host=os.environ.get("DB_HOST"),
    user=os.environ.get("DB_USER"),
    password=os.environ.get("DB_PASSWORD"),
    database="simple_app"
)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        cursor = db.cursor()
        cursor.execute("INSERT INTO users (name, email) VALUES (%s, %s)", (name, email))
        db.commit()
        return redirect('/users')
    return render_template('index.html')

@app.route('/users')
def users():
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM users")
    rows = cursor.fetchall()
    return render_template('users.html', users=rows)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)

