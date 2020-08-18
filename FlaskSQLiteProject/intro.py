#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This is where the flask web application happening.

@author: felixestrella
"""

from flask import Flask, render_template, redirect, url_for, request
import database
import reader
import book
import author

app = Flask(__name__)


# This is the login page for application
@app.route('/', methods=['POST', 'GET'])
def home():
    global db 
    db = database.database
    db.connect()
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        global person
        person = reader.reader(username, password)
        valid = db.checkForUser(person)
        if valid == False:
            error = 'Invalid Credentials. Please try again.'
        else:
            db.userId(person)
            return redirect(url_for('start'))
    return render_template('login.html', error = error)

# This is where a user can register for an account  
@app.route('/register', methods=['POST', 'GET'])
def register():
    
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if db.checkIfNameTaken(username) == False:
            newPerson = reader.reader(username, password)
            try:
                db.addUser(newPerson)
                return redirect(url_for('home'))
            except:
                error = 'Name Taken. Please try again.'
        else:
            error = "Username Taken"
    return render_template('register.html', error = error)

# This is the starting page for the application when a user logs in
@app.route('/informationPage')
def start():
    error = None
    results = None
    try:
        results = db.showBooks(person.getUserId())
    except:
        error = "No Books"
    try:
        data = db.getNumBooks(person.getUserId())
    except:
        data = 0
        
    return render_template('infoPage.html', error = error, results = results, data = data)

# This is the page where a user can add a book to their list
@app.route('/addBook', methods=['POST', 'GET'])
def addBook():
    error = None
    if request.method == 'POST':
        global b
        global writer
        b = book.book(request.form['ISBN'], request.form['title'], request.form['yearPublished'])
        writer = author.author(request.form['firstName'], request.form['lastName'], request.form['country'])
        if (db.bookExist(b) == False):
            try:
                db.addBook(b)
            except:
                error = 'Invalid Data. Please try again.'
            if (db.authorExist(writer) == False):
                try:
                    db.addAuthor(writer)
                except:
                    error = 'Invalid Data. Please try again.'
        try:
            db.authorId(writer)
        except:
            error = 'Author Not Correct For Book. Please try again.'
        if (db.readsExist(person, b) == False):
            try:
                db.addReads(person, b, request.form['rate'])
            except:
                error = 'Error. Please try again.'
        if (db.writesExist(writer, b) == False):
            try:
                db.addWrites(b, writer)
            except:
                error = 'Error HERE. Please try again.'   
            
    return render_template('addBook.html', error = error)

# This is where a user can modify a book from their list
@app.route('/modifyBook', methods=['POST', 'GET'])
def modifyBook():  
    error = None
    if request.method == 'POST':
        try:
            db.updateBook(request.form['ISBN'], request.form['choice'], request.form['info'], person)
        except:
            error = "Error in data"
    return render_template('modBook.html', error = error)

# This is where a user can modify author information
@app.route('/modifyAuthor', methods=['POST', 'GET'])
def modifyAuthor():  
    error = None
    if request.method == 'POST':
        try:
            db.updateAuthor(request.form['curFirst'], request.form['curLast'], request.form['curCountry'], request.form['newFirst'], request.form['newLast'], request.form['newCountry'])
        except:
            error = "Error in data"
    return render_template('modAuthor.html', error = error)

# This is where a user can delete a book
@app.route('/deleteBook', methods=['POST', 'GET'])
def deleteBook():
    error = None
    if request.method == 'POST':
        isbn = request.form['ISBN']
        try:
            db.delReads(isbn, person)
        except:
            error = "Wrong ISBN or Not In List"
        if db.readsStillActive(isbn) == False:
            try:
                num = db.getAId(isbn)
            except:
                error = "Not in List"
            if num == -1:
                return render_template('delBook.html', error = "Not in List")
            try:
                db.delWrites(isbn)
            except:
                error = "Error Writes"
            try:   
                db.delBook(isbn)
            except:
                error = "Error Reads"
            if db.getAuthorWrites(num) == False:
                try:
                    db.delAuthor(num)
                except:
                    error = "Error Author"
            
    return render_template('delBook.html', error = error)

# This is where a user can get an authors rating and see all the books they have read from the author
@app.route('/authorRating', methods=['POST', 'GET'])
def authorRating():
    error = None
    results = None
    data = 0
    if request.method == 'POST':
        try:
            authId = db.getAuthId(request.form['first'], request.form['last'], request.form['country'])
        except:
            error = "Fill in all fields"
        try:
            data = db.getAuthorAvg(authId, person)
        except:
            data = 0
        try:
            results = db.getBooksByAuthor(authId, person)
        except:
            error = "No Books"
        if data == None:
            data = 0
    return render_template('authorRate.html', error = error, results = results, data = data)

# This is where the user can see all the books above thier average rating for all books
@app.route('/aboveAverageBooks', methods=['POST', 'GET'])
def aboveAvgBooks():
    error = None
    results = None
    data = 0
    try:
        results = db.aboveAvg(person.getUserId())
    except:
        error = "No Books"
    try:
        data = db.avgRate(person.getUserId())
    except:
        data = 0
    if data == None:
        data = 0
    return render_template('aboveAvg.html', error = error, results = results, data = data)

# This is when the user logs out
@app.route('/logout')
def logout():
    db.disconnect()
    return render_template('logout.html')

# This is when the user can serach for books based off keywords
@app.route('/searchKeywords', methods=['POST', 'GET'])
def keywordSearch():
    error = None
    results = None
    if request.method == 'POST':
        keyword = request.form['keyword']
        if keyword != "":
            try:
                results = db.keywords(person.getUserId(), keyword)
            except:
                error = "No Books"
    return render_template('keyword.html', error = error, results = results)

# User can search for authors they have rated higher than the author they entered
@app.route('/searchHigherRatedAuthors', methods=['POST', 'GET'])
def higherRatedAuthorSearch():
    error = None
    results = None
    if request.method == 'POST':
        try:
            authId = db.getAuthId(request.form['first'], request.form['last'], request.form['country'])
        except:
            error = "Fill in all fields"
        try:
            results = db.higherRatedAuthors(person.getUserId(), authId)
        except:
            error = "Something went wrong"
    return render_template('aboveAuth.html', error = error, results = results)

# Can see what books they have read that are the same as other users
@app.route('/friendSearch', methods=['POST', 'GET'])
def friendSearch():
    error = None
    results = None
    my = None
    friend = None
    if request.method == 'POST':
        my = person.getUsername()
        friend = request.form['username']
        try:
            results = db.friendSameReads(person.getUserId(), friend)
        except:
            error = "error"
    return render_template('friends.html', error = error, results = results, my = my, friend = friend)