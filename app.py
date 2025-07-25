from flask import Flask, render_template, request, flash ,url_for
from flask_mysqldb import MySQL
from werkzeug.utils import redirect
from datetime import datetime

app = Flask(__name__)
app.secret_key='some_random_data'

app.config["MYSQL_PORT"]=3306
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'drinks_db'

mysql = MySQL(app)

@app.route('/')
def home():
    try:
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM drinks")
        drinks = cur.fetchall()
        cur.close()
        app.logger.info(f"Drinks fetched: {drinks}")
        return render_template('index.html', drinks=drinks)
    except Exception as e:
        app.logger.error(f"Database fetch error: {e}")
        flash('Could not load drinks from database.')
        return render_template('index.html', drinks=[])

@app.route('/insert', methods=['POST'])
def insert():
    try:
        name_of_drink = request.form['name_of_drink']
        price = float(request.form['price']) 
        quantity = int(request.form['quantity'])
        expiry_date = request.form['expiry_date']
        batch_no = request.form.get('batch_no', '')
        drink_subtype = request.form.get('drink_subtype', '')

        # Validate date
        datetime.strptime(expiry_date, '%Y-%m-%d')

        cur = mysql.connection.cursor()
        cur.execute('''
            INSERT INTO drinks (name_of_drink, price, quantity, expiry_date, batch_no, drink_subtype)
            VALUES (%s, %s, %s, %s, %s, %s)
        ''', (name_of_drink, price, quantity, expiry_date, batch_no, drink_subtype))
        mysql.connection.commit()
        cur.close()

        flash('Drink added successfully!')
    except Exception as e:
        app.logger.error(f"Insert error: {e}")
        flash(f'Error adding drink: {e}')
    return redirect('/')


@app.route('/edit/<int:id>')
def edit(id):
    try:
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM drinks WHERE id = %s", (id,))
        drink = cur.fetchone()
        cur.close()

        if not drink:
            flash('Drink not found.')
            return redirect(url_for('home'))

        return render_template('edit.html', drink=drink)
    except Exception as e:
        app.logger.error(f"Edit fetch error: {e}")
        flash('Error loading drink for editing.')
        return redirect(url_for('home'))


@app.route('/update', methods=['POST'])
def update():
    try:
        id = int(request.form['id'])
        name_of_drink = request.form['name_of_drink']
        price = float(request.form['price'])
        quantity = int(request.form['quantity'])
        expiry_date = request.form['expiry_date']
        batch_no = request.form.get('batch_no', '')
        drink_subtype = request.form.get('drink_subtype', '')

        # Validate date
        datetime.strptime(expiry_date, '%Y-%m-%d')

        cur = mysql.connection.cursor()
        cur.execute('''
            UPDATE drinks
            SET name_of_drink = %s, price = %s, quantity = %s, expiry_date = %s, batch_no = %s, drink_subtype = %s
            WHERE id = %s
        ''', (name_of_drink, price, quantity, expiry_date, batch_no, drink_subtype, id))
        mysql.connection.commit()
        cur.close()

        flash('Drink updated successfully!')
    except Exception as e:
        app.logger.error(f"Update error: {e}")
        flash(f'Error updating drink: {e}')
    return redirect(url_for('home'))



@app.route('/delete/<int:id>', methods=['POST'])
def delete_confirmed(id):
    try:
        cur = mysql.connection.cursor()
        cur.execute("DELETE FROM drinks WHERE id = %s", (id,))
        mysql.connection.commit()
        cur.close()
        flash('Drink deleted successfully!', 'success')
    except Exception as e:
        app.logger.error(f"Delete error: {e}")
        flash('Error deleting drink.', 'danger')
    return redirect(url_for('home'))


if __name__ == '__main__':
    app.run(debug=True)
