from flask import Flask, flash, redirect, render_template, request, session, abort
import ibm_db_dbi as dbi
from ibm_db_dbi import SQL_ATTR_DBC_SYS_NAMING, SQL_TRUE
from ibm_db_dbi import SQL_ATTR_TXN_ISOLATION,SQL_TXN_NO_COMMIT

app = Flask(__name__)
options = {
    SQL_ATTR_TXN_ISOLATION: SQL_TXN_NO_COMMIT,
    SQL_ATTR_DBC_SYS_NAMING: SQL_TRUE,
}
conn = dbi.connect()
conn.set_option(options)


@app.route("/")
def hello():
    cur = conn.cursor()
    query = "select * from pgfiles.tfco#5 where tdco# = ? and tdcode = ?"
    company = '00004'
    code = '00004'
    cur.execute(query, (company, code,))
    # for row in cur:
    #     print(row[2])
    print(cur.description)
    name = request.args.get('username')
    return render_template('index.html', name=name, rows=cur)


@app.route('/user/<username>')
def show_user_profile(username):
    # show the user profile for that user
    return render_template('profile.html', name=username)


@app.route("/zip")
def get_zip():
    # name = request.args.get('username')
    return "14526"


@app.route("/formAddSupply")
def form_add_supply():
    if 'user' not in session:
        return redirect("/login")
    cur = conn.cursor()
    sql = "select * from pgfiles.supplyty"
    cur.execute(sql)
    return render_template('index2.html', supply_types=cur)


@app.route('/addSupply', methods=['POST'])
def add_supply():
    # read the posted values from the UI
    cur = conn.cursor()
    supply_name = request.form.get('supply_name')
    supply_brand = request.form.get('supply_brand')
    supplier = request.form.get('supplier-id')
    if supplier:
        supplier = int(supplier)
    else:
        supplier = 0
    supply_type = request.form.get('supply-type')
    in_stock = request.form.get('in-stock')
    conclusion = 'Name: ' + str(supply_name) + ' Brand: ' + str(supply_brand)
    conclusion += ' Type: ' + str(supply_type) + ' In Stock: ' + str(in_stock)
    color = request.form.get('color')
    errors = {}
    if supply_name == '':
        errors['supply_name'] = 'Please enter a value for supply type'
    if supply_brand == '':
        errors['supply_brand'] = 'Please enter a value for supply brand'
    if supplier < 1:
        errors['supplier'] = 'Please enter a value > 0 for supplier'
    sql = "select * from pgfiles.supplyty where supply_type = ?"
    cur.execute(sql, (supply_type,))
    if not cur:
        # Throw error
        pass
    if not errors:
        sql = """INSERT INTO PGFILES/SUPPLIES (supply_brand, supply_type, supplier_id) values(?, ?, ?)"""
        cur.execute(sql, (supply_brand, supply_type, supplier))
        return render_template('index2.html', conclusion=conclusion, color=color)
    else:
        return render_template('index2.html', errors=errors)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        try:
            oconn = dbi.connect(user=username, password=password)
        except:
            errors = 'Invalid login'
            return render_template('login.html', errors=errors)
        session['user'] = username

        return redirect("/formAddSupply")
    else:
        return render_template('login.html')


@app.route('/logout', methods=['GET', 'POST'])
def logout():
    session.clear()
    return redirect("/login")


if __name__ == "__main__":
    app.secret_key = 'sdfjbvbn'
    app.config['SESSION_TYPE'] = 'filesystem'
    app.run(debug=False, host="0.0.0.0", port=9105)
