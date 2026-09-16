from flask import Flask, render_template, request, redirect, url_for
from connection import conn

app = Flask(__name__)

@app.route('/')
def dashboard():
    return render_template('layout/base.html')

# Category route
@app.route('/category')
def index_category():
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM category")
    categories = cursor.fetchall()
    cursor.close()
    return render_template('category/index.html', categories=categories)

@app.route('/category/create', methods=['GET', 'POST'])
def create_category():
    if request.method == "POST":
        name = request.form['name']
        status = request.form['status']

        db = conn
        cursor = db.cursor()
        cursor.execute("INSERT INTO category(name,status) VALUES(%s, %s)", (name, status))
        db.commit()
        cursor.close()
        return redirect(url_for('index_category')) 
    return render_template('category/create.html')


@app.route('/category/update/<int:id>', methods=['GET', 'POST'])
def update_category(id):
    cursor = conn.cursor()

    if request.method == "POST":
        newName = request.form['name']
        newStatus = request.form['status']

        sql = "UPDATE category SET name=%s, status=%s WHERE id=%s"
        cursor.execute(sql, (newName, newStatus, id))
        conn.commit()
        cursor.close()
        return redirect(url_for('index_category'))

    cursor.execute("SELECT * FROM category WHERE id=%s", (id,))
    category = cursor.fetchone()
    cursor.close()
    if not category:
        return "404 Not Found"

    return render_template('category/update.html', category=category)

@app.route('/product')
def index_product():
    return render_template('products/index.html')


if __name__ == "__main__":
    app.run(debug=True)
