# importa los paquetes necesarios
from logging import debug
from os import stat
from flask import Flask, render_template, request, redirect, url_for, flash, redirect, session
import json
import mariadb
from flask.config import Config


config = {
    'host': '127.0.0.1',
    'port': 3306,
    'user': 'root',
    'password': 'qwerty',
    'database': 'python_DB'
}

# crea la aplicacion en flask
app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
app.config["DEBUG"] = True

user = {"username": "eduardo", "password": "qwerty"}


@app.route('/products')
def products():
    conn = mariadb.connect(**config)
    cur = conn.cursor(dictionary=True)
    # ejecutamos un query a base de datos
    cur.execute("select * from tblinventory")
    data = cur.fetchall()
    cur.close()
    return render_template('product_list.html', products=data)


@app.route('/movimientos')
def movimientos():
    conn = mariadb.connect(**config)
    cur = conn.cursor(dictionary=True)
    # ejecutamos un query a base de datos
    cur.execute("""select m.Id, t.Description Producto, c.Description Concepto, c.Tipo, m.Cantidad, movDate, Balance from tblinventoryMovement m
                inner join tblinventory t on m.ItemId=t.Id
                inner join tblconcept c on m.conceptId=c.Id """)
    data = cur.fetchall()
    cur.close()
    return render_template('movement_list.html', movimientos=data)


@app.route('/', methods=['POST', 'GET'])
def index():
    if(request.method == 'POST'):
        username = request.form.get('username')
        password = request.form.get('password')
        if username == user['username'] and password == user['password']:

            session['user'] = username
            return redirect('/products')

        # if the username or password does not matches
        return "<h1>Wrong username or password</h1>"

    return render_template("login.html")


@app.route('/logout')
def logout():
    # session.pop('user') help to remove the session from the browser
    session.pop('user')
    return redirect('/')


@app.route('/add_product', methods=['POST'])
def add_product():
    if request.method == 'POST':
        conn = mariadb.connect(**config)
        descripcion = request.form['descripcion']
        serial = request.form['serial']
        ubicacion = request.form['ubicacion']
        costo = request.form['costo']
        cur = conn.cursor()
        statement = "INSERT INTO tblinventory (description, Serial, location,cost) VALUES (%s,%s,%s,%s)"
        datos = (descripcion, serial, ubicacion, costo)
        cur.execute(statement, datos)
        conn.commit()
        flash('Producto Agregado Existosamente')
        return redirect(url_for('products'))


@app.route('/add_movement', methods=['GET','POST'])
def add_movement():
    if request.method == 'POST':
        conn = mariadb.connect(**config)
        concepto = request.form.get('concepto')
        producto = request.form.get('producto')
        cantidad = request.form.get('cantidad')
        cur = conn.cursor()
        statement = "INSERT INTO tblInventoryMovement (itemId, conceptId, cantidad) VALUES (%s,%s,%s)"
        datos = (producto, concepto, cantidad)
        cur.execute(statement, datos)
        conn.commit()
        flash('Movimiento Agregado Existosamente')
        return redirect(url_for('movimientos'))
    
@app.route('/newproduct', methods=['POST', 'GET'])
def new_product():
    return render_template('add_product.html')


@app.route('/newmovement', methods=['POST', 'GET'])
def new_movement():
    conn = mariadb.connect(**config)
    cur = conn.cursor(dictionary=True)
    # ejecutamos un query a base de datos
    cur.execute("""SELECT Id, Description FROM tblconcept """)
    data = cur.fetchall()
    cur.execute("""SELECT Id, Description FROM tblinventory """)
    inventorydata = cur.fetchall()
    cur.close()
    return render_template('add_movement.html', concepts=data, products=inventorydata)

@app.route('/editproduct/<id>', methods=['POST', 'GET'])
def get_product(id):
    conn = mariadb.connect(**config)
    cur = conn.cursor(dictionary=True)
    datos = (id,)
    statement = "SELECT Id,Description,Serial,Stock,Location,Cost FROM tblinventory WHERE id = %s"
    cur.execute(statement, datos)
    data = cur.fetchall()
    cur.close()
    print(data[0])
    return render_template('edit_product.html', product=data[0])


@app.route('/updateproduct/<id>', methods=['POST'])
def update_product(id):
    if request.method == 'POST':
        statement = "UPDATE tblinventory SET description = %s, Serial = %s, Location = %s,Cost = %s WHERE id = %s"
        descripcion = request.form['Descripcion']
        serial = request.form['Serial']
        ubicacion = request.form['Ubicacion']
        costo = request.form['Costo']
        conn = mariadb.connect(**config)
        cur = conn.cursor()
        datos = (descripcion, serial, ubicacion, costo, id)
        cur.execute(statement, datos)
        flash('Producto Actualizado Exitosamente')
        conn.commit()
        return redirect(url_for('products'))


@app.route('/deleteproduct/<id>', methods=['POST', 'GET'])
def delete_product(id):
    conn = mariadb.connect(**config)
    cur = conn.cursor()
    statement = "DELETE FROM tblinventory WHERE Id=%s"
    datos = (id,)
    cur.execute(statement, datos)
    conn.commit()
    flash('Producto eliminado exitosamente')
    return redirect(url_for('products'))



if(__name__) == "__main__":
    app.run(port=3000, debug=True)
