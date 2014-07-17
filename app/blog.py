#!/usr/bin/env python

import os
import os.path

from database import connect_db

from io import BytesIO
from flask import Flask, request, session, g, redirect, url_for, abort,\
        render_template, flash

from java.sql  import SQLException
#import java.net.IDN

### Config
DATABASE = os.path.join(os.path.dirname(__file__), "database.db")
JDBC_URL    = "jdbc:sqlite:%s"  % DATABASE
JDBC_DRIVER = "org.sqlite.JDBC"

app = Flask(__name__)
app.config.from_object(__name__)
app.secret_key = "THIS IS SECRET"

app.config.update(dict(
    DATABASE=DATABASE,
    JDBC_URL=JDBC_URL,
    JDBC_DRIVER=JDBC_DRIVER,
    DEBUG=False,
    USERNAME='admin',
    PASSWORD='admin'
))
app.config.from_envvar('BLOG_SETTINGS',silent=True)

### DB
def get_db():
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db(app.config["JDBC_URL"], app.config["JDBC_DRIVER"])
    return g.sqlite_db

@app.teardown_appcontext
def close_db(error):
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()

### View
@app.route('/')
def show_entries():
    db = get_db()
    stmt = db.createStatement()
    try:
        resultSet = stmt.executeQuery('select id, title, text from entries order by id desc')
    except SQLException, msg:
        print msg
        sys.exit(1)
    entries = []
    while resultSet.next():
        id_ = resultSet.getInt("id")
        title = resultSet.getString("title")
        text = resultSet.getString("text")
        entries.append({"id":id_, "title":title, "text": text})
    return render_template('show_entries.html', entries=entries)

@app.route('/add', methods=['POST'])
def add_entry():
    if not session.get('logged_in'):
        abort(401)
    db = get_db()
    try:
        preppedStmt = db.prepareStatement('insert into entries (title, text) values (?,?)')
        preppedStmt.setString(1,request.form['title'])
        preppedStmt.setString(2,request.form['text'])
        preppedStmt.addBatch()
        db.setAutoCommit(False)
        preppedStmt.executeBatch()
        db.setAutoCommit(True)
    except SQLException, msg:
        print msg
        sys.exit(1)
    flash('New entry was successfully posted')
    return redirect(url_for('show_entries'))

@app.route('/del', methods=['POST'])
def del_entry():
    if not session.get('logged_in'):
        abort(401)
    db = get_db()
    print "delete: ",request.form['id']
    try:
        preppedStmt = db.prepareStatement('delete from entries where id = ?')
        preppedStmt.setString(1,request.form['id'])
        preppedStmt.addBatch()
        db.setAutoCommit(False)
        preppedStmt.executeBatch()
        db.setAutoCommit(True)
    except SQLException, msg:
        print msg
        flash('Failed to Delete')
        return redirect(url_for('show_entries'))
    flash('The entry was successfully deleted')
    return redirect(url_for('show_entries'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != app.config['USERNAME']:
            error = 'Invalid username'
        elif request.form['password'] != app.config['PASSWORD']:
            error = 'Invalid password'
        else:
            session['logged_in'] = True
            flash('You were logged in')
            return redirect(url_for('show_entries'))
    return render_template('login.html', error=error)

@app.route('/logout')
def logout():
    session.pop('logged_in',None)
    flash('You were logged out')
    return redirect(url_for('show_entries'))

