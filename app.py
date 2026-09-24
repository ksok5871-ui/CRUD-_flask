import os

from flask import Flask, render_template, request, redirect, url_for
from connection import conn
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = os.path.join('static', 'Uploads', 'Products')
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

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

@app.route('/category/delete/<int:id>', methods=['POST'])
def delete_category(id):
    cursor=conn.cursor()
    cursor.execute("DELETE FROM category WHERE id=%s", (id,))
    conn.commit()
    cursor.close()
    return redirect(url_for('index_category'))


@app.route('/product')
def index_product():
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM products")
    products = cursor.fetchall()
    cursor.close()
    return render_template('products/index.html', products=products)

@app.route('/product/create', methods=['GET', 'POST'])
def create_product():
    if request.method == "POST":
        name = request.form['name']
        price = request.form['price']
        stock = request.form['stock']
        image = request.files.get('image')
        image_name = None
        if image and image.filename and isinstance(image.filename, str):
            image_name = secure_filename(image.filename)
            image_path = os.path.join(app.config['UPLOAD_FOLDER'], image_name)
            image.save(image_path)

        cursor = conn.cursor()
        sql = "INSERT INTO products(name, price, stock, image) VALUES(%s, %s, %s, %s)"
        cursor.execute(sql, (name, price, stock, image_name))
        conn.commit()
        cursor.close()
        return redirect(url_for('index_product'))
    return render_template('products/create.html')

@app.route('/product/update/<int:id>', methods=['GET', 'POST'])
def update_product(id):
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM products WHERE id=%s', (id,))
    product = cursor.fetchone()

    if product is None:
        cursor.close()
        return "Product not Found", 404

    if request.method == "POST":
        newName = request.form['name']
        newPrice = request.form['price']
        newStock = request.form['stock']
        image_file = request.files.get('image')

        old_image = product['image']
        new_image = old_image  # Default to keeping the old image

        # Check if user uploaded a new image
        if image_file and image_file.filename != "":
            filename = secure_filename(image_file.filename)
            new_image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)

            # Save new image
            image_file.save(new_image_path)
            new_image = filename

            # Delete the old image from the folder if it exists
            if old_image:
                old_image_path = os.path.join(app.config['UPLOAD_FOLDER'], old_image)
                if os.path.exists(old_image_path):
                    os.remove(old_image_path)

        # UPDATE query is now outside the file check so it always runs
        cursor.execute("""
            UPDATE products
            SET name=%s, price=%s, stock=%s, image=%s
            WHERE id=%s
        """, (newName, newPrice, newStock, new_image, id))

        conn.commit()
        cursor.close()
        return redirect(url_for('index_product'))

    cursor.close()
    return render_template('products/update.html', product=product)

@app.route('/product/delete/<int:id>', methods=['POST'])
def delete_product(id):
    cursor = conn.cursor()
    cursor.execute('DELETE FROM products WHERE id=%s', (id,))
    conn.commit()
    cursor.close()
    return redirect(url_for('index_product'))
if __name__ == "__main__":
    app.run(debug=True)
