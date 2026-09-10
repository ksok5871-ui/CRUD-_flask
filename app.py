from flask import Flask,render_template

app=Flask(__name__)
#category
@app.route('/category')
def category():
    return render_template('category/index.html')

@app.route('/product')
def index_product():
    return render_template('products/index.html')


if __name__=="__main__":
    app.run(debug=True)
