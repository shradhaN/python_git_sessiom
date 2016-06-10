# - * - coding : utf-8-*-
"""
Simple flask based application
"""
#import sqlite3
import sqlite3

# import flask from flask module
from flask import Flask, render_template, request, redirect, url_for


# app is instance of flask class
print(__name__)  # ---> prints name of terminal

app = Flask(__name__)

def get_connection():
    return  sqlite3.connect('db.sqlite3')


def init_db():

    db_conn = get_connection()
    cur = db_conn.cursor()
    _sql = '''SELECT name FROM sqlite_master
    WHERE type ='table' AND name = 'peoples'   
    '''
    cur.execute(_sql)
    if not cur.fetchone():
        _create_sql = '''CREATE TABLE peoples(
            id integer PRIMARY KEY AUTOINCREMENT,
            firstname text NOT NULL,
            lastname text NULL,
            address text NULL,
            country text NULL) 
        '''
        cur.execute(_create_sql)
        db_conn.commit()


@app.route('/')
def index():
    """
    index page of our web app
    """
    return render_template('home.jinja2')
# to load template html file
# you cannot write new function with the same route. it throws error and
# the first function is overwritten


@app.route('/add', methods=['GET', 'POST'])
def add_people():
    """
    add new people
    """
    print('>' * 5, request.method)
    if request.method == "POST":
        db_conn = get_connection()
        cur = db_conn.cursor()
        # save data to database
        # redirect to list page
        print('>' * 5, request.form)

        firstname = request.form['firstname']
        lastname = request.form['lastname']
        address = request.form['address']
        country = request.form['country']
 
        #check whether the first name is empty or not 
        if firstname.strip():
            #save to db
            _sql = '''INSERT INTO peoples(
            firstname, lastname, address , country)
            VALUES (?,?,?,?)'''
            cur.execute(_sql,(firstname.strip(),
                lastname.strip(),
                address.strip(),
                country.strip()
                ))
            db_conn.commit()
            #redirect to the list page
            return redirect(url_for('list_people'))   
               
        
    return render_template('add.jinja2')


@app.route('/list')
def list_people():
    """
    list all people
    """
    db_conn = get_connection()
    cur = db_conn.cursor()
    _sql = """SELECT 
    id, firstname, lastname, address, country 
    FROM peoples"""
    cur.execute(_sql)
    records = cur.fetchall()
    return render_template('list.jinja2',data = records)

@app.route('/update/<int:pid>', methods = ['GET','POST'])
def update_people(pid):
    """should update any people by given id
    select * from peoples where id = pid
    """ 
    db_conn = get_connection()
    cur = db_conn.cursor()
    if request.method == 'GET':
        
        #render_template('add.jinja2')     
        return redirect(url_for('add_people'))
        
        _update_sql='''SELECT id = pid, 
                    firstname = ?,
                    lastname  = ?,
                    address = ?, 
                    country = ?  WHERE id = pid'''
        cur.execute(_update_sql,(pid,))
        update = cur.fetchone()
        if record:
            return render_template('update.jinja2', data = record)
        else:
            flash ("Sorry! Couldn't get user with id{}")
        db_conn.commit()
        return render_template('list.jinja2', data = update)
    return redirect(url_for('index'))


     

@app.route('/delete_people/<int:pid>')
def delete_people(pid):
    """Delete's the row where id = pid"""

    db_conn = get_connection()
    cur = db_conn.cursor()
    
    cur.execute('DELETE FROM peoples WHERE id =?',(pid,))
    db_conn.commit()
    return render_template('home.jinja2')
    

if __name__ == "__main__":
    # only when __name__ is __main__
    init_db()
    app.run(debug=True)
