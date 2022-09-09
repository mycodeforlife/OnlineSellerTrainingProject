from app import app
from flask import render_template, flash, redirect, jsonify
from app.forms import *
from flask_mysqldb import MySQL
import MySQLdb
import hashlib



@app.route('/')
@app.route('/index')
def index():
    user_info = {
        'name':'User'
    }
    return render_template('index.html', user=user_info)


connection = MySQLdb.connect(host="localhost", user="root", passwd="admin", db="inventory")


'''
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'admin'
app.config['MYSQL_DB'] = 'inventory'

mysql = MySQL(app)
'''


@app.route('/login', methods=['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.user_name.data == 'admin' and form.password.data == 'admin':
            flash('login successful')
            return redirect('index')
    return render_template('login.html', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        first_name = form.first_name.data
        last_name = form.last_name.data
        email_address = form.email_address.data
        user_name = form.user_name.data
        password = form.password.data
        d = hashlib.sha1(password.encode())
        d.digest()
        encrypted_pass = d.hexdigest()
        insert_query = "INSERT INTO UserProfile(first_name, last_name, email_address, user_name, pword) values (\""+first_name+"\",\""+last_name+"\",\""+email_address+"\",\""+user_name+"\",\""+encrypted_pass+"\");"
        cursor = connection.cursor()
        try:
            print("running query insert")
            insert_query_result = cursor.execute(insert_query)
            print(insert_query_result)
            #return redirect('register')
        except:
            return render_template('already_registered.html', form=form)
    return render_template('register.html', form=form)

@app.route('/v1/getcategories', methods=['GET'])
def getcategories():
    cursor = connection.cursor()
    cursor.execute("select * from product;")
    db = cursor.fetchall()
    josn_reponse = []
    for data in db:
        product_data = {}
        product_data["category"] = data[0]
        product_data["product"] = data[1]
        product_data["qantity"] = data[2]
        product_data["price"] = data[3]
        josn_reponse.append(product_data)
    json_data = josn_reponse
    return jsonify(json_data)


