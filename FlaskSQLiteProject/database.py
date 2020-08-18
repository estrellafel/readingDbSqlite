#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Where all the queries to the database happen. Also where the database calls to connect and disconnect.
Uses SQLite as the database.

@author: felixestrella
"""
import sqlite3


class database:
    
    # A constructor for the database
    def __init__():
        return
    
    # Connect the database to the program
    def connect():
        global conn
        conn = None
        try:
            # IMPORTANT MUST PUT LOCATION OF DATABASE HERE example /user/desktop/read.bd
            conn = sqlite3.connect('LOCATION OF DATABASE',check_same_thread=False)
        except:
                print("The is an error with connecting")
    
    # Disconnect the database
    def disconnect():
        conn.close()
    
    # Returns true if user is in database otherwise false
    def checkForUser(reader):
        cur = conn.cursor()
        cur.execute('Select count(*) FROM Reader WHERE Reader.Password =:pass AND Reader.Username =:user', {"pass": reader.getPassword(), "user": reader.getUsername()})
        check = cur.fetchall()
        for c in check:
            valid = c[0]
        if valid == 1:
            return True
        else:
            return False
    
    # Returns true if name is taken otherwise false
    def checkIfNameTaken(name):
        cur = conn.cursor()
        cur.execute('Select count(*) FROM Reader WHERE Reader.Username =:user', {"user": name})
        check = cur.fetchall()
        for c in check:
            valid = c[0]
        if valid == 1:
            return True
        else:
            return False
    
    # Adds a user to the database    
    def addUser(reader):
        cur = conn.cursor()
        details = [reader.getUsername(), reader.getPassword()]
        cur.execute('INSERT INTO Reader (username, password) values (?,?)', details)
        conn.commit()
    
    # Sets the userId for the reader
    def userId(reader):
        cur = conn.cursor()
        cur.execute('SELECT UserId FROM Reader WHERE Username =:user', {"user": reader.getUsername()})
        data = cur.fetchall()
        for d in data:
            reader.setUserId(d[0])
    
    # Adds a book to the database
    def addBook(book):
        cur = conn.cursor()
        details = [book.getISBN(), book.getTitle(), book.getYear()]
        cur.execute('INSERT INTO Book (ISBN, Title, YearPublished) values (?,?,?)', details)
        conn.commit()
    
    # Adds an author to the database
    def addAuthor(author):
        cur = conn.cursor()
        details = [author.getFirst(), author.getLast(), author.getCountry()]
        cur.execute('INSERT INTO Author (FirstName, LastName, Country) values (?,?,?)', details)
        conn.commit()
    
    # Sets the authorId for an author
    def authorId(author):
        cur = conn.cursor()
        cur.execute('SELECT AuthorId FROM Author WHERE FirstName =:first AND LastName =:last', {"first": author.getFirst(), "last": author.getLast()})
        data = cur.fetchall()
        for d in data:
            author.setId(d[0])
    
    # Returns true if the book exist and false if it does not       
    def bookExist(book):
        cur = conn.cursor()
        cur.execute('Select count(*) FROM Book WHERE ISBN =:num', {"num": book.getISBN()})
        check = cur.fetchall()
        for c in check:
            valid = c[0]
        if valid == 1:
            return True
        else:
            return False
        
    # Returns true if the author exists and false if it does not
    def authorExist(author):
        cur = conn.cursor()
        cur.execute('Select count(*) FROM Author WHERE FirstName=:first AND LastName =:last', {"first": author.getFirst(), "last": author.getLast()})
        check = cur.fetchall()
        for c in check:
            valid = c[0]
        if valid == 1:
            return True
        else:
            return False 
    
    # Will add the book to the users list with the rating
    def addReads(reader, book, rate):
        cur = conn.cursor()
        details = [rate ,book.getISBN(), reader.getUserId()]
        cur.execute('INSERT INTO Reads (Rating ,ISBN, UserId) values (?,?,?)', details)
        conn.commit()
    
    # Checks if the book is already on the readers list    
    def readsExist(reader, book):
        cur = conn.cursor()
        cur.execute('Select count(*) FROM Reads WHERE ISBN=:first AND UserId =:read', {"first": book.getISBN(), "read": reader.getUserId()})
        check = cur.fetchall()
        for c in check:
            valid = c[0]
        if valid == 1:
            return True
        else:
            return False 
    
    # Checks if the book is already in the database for an author
    def writesExist(author, book):
        cur = conn.cursor()
        cur.execute('Select count(*) FROM Writes WHERE ISBN=:first AND AuthorId =:read', {"first": book.getISBN(), "read": author.getId()})
        check = cur.fetchall()
        for c in check:
            valid = c[0]
        if valid == 1:
            return True
        else:
            return False 
    
    # Adds the book for the author writting it    
    def addWrites(book, author):
        cur = conn.cursor()
        details = [book.getISBN(), author.getId()]
        cur.execute('INSERT INTO Writes (ISBN, AuthorId) values (?,?)', details)
        conn.commit()
    
    # Will update book information
    def updateBook(isbn, choice, newVal, person):
        cur = conn.cursor()
        if choice == '1':
            cur.execute('UPDATE Book SET Title = :val WHERE ISBN = :is', {"val": newVal, "is": isbn})
            conn.commit()
        elif choice == '2':
            cur.execute('UPDATE Book SET YearPublished = :val WHERE ISBN = :is', {"val": newVal, "is": isbn})
            conn.commit()
        elif choice == '3':
            cur.execute('UPDATE Reads SET Rating = :val WHERE ISBN = :is AND UserId = :id', {"val": newVal, "is": isbn, "id": person.getUserId()})
            conn.commit()
    
    # Will update author information        
    def updateAuthor(oldFirst, oldLast, oldCountry, newFirst, newLast, newCountry):
        cur = conn.cursor()
        cur.execute('UPDATE Author SET FirstName =:nf, LastName =:nl, Country =:nc WHERE FirstName =:cf AND LastName =:cl AND Country =:cc', {"nf": newFirst, "nl": newLast, "nc": newCountry, "cf": oldFirst, "cl": oldLast, "cc": oldCountry})
        conn.commit()
    
    # Deletes a book off an authors list    
    def delReads(isbn, person):
        cur = conn.cursor()
        cur.execute('DELETE FROM Reads WHERE ISBN =:is AND UserId =:id', {"is": isbn, "id": person.getUserId()})
        conn.commit()
    
    # Deletes a book off the list of books an author has written    
    def delWrites(isbn):
        cur = conn.cursor()
        cur.execute('DELETE FROM Writes WHERE ISBN =:is', {"is": isbn})
        conn.commit()
    
    # Deletes a book from the database
    def delBook(isbn):
        cur = conn.cursor()
        cur.execute('DELETE FROM Book WHERE ISBN =:is', {"is": isbn})
        conn.commit()
    
    # Deletes an author off a database     
    def delAuthor(idNum):
        cur = conn.cursor()
        cur.execute('DELETE FROM Author WHERE AuthorId =:is', {"is": idNum})
        conn.commit()
    
    # Returns true if still in reads and false if not 
    def readsStillActive(isbn):
        cur = conn.cursor()
        cur.execute('Select count(*) FROM Reads WHERE ISBN =:first', {"first": isbn})
        check = cur.fetchall()
        for c in check:
            valid = c[0]
        if valid > 0:
            return True
        else:
            return False 
    
    # Will get the author Id from the database
    def getAId(isbn):
        cur = conn.cursor()
        cur.execute('SELECT AuthorId FROM Writes WHERE ISBN =:is ', {"is": isbn})
        data = cur.fetchall()
        num = -1
        for d in data:
            num = d[0]
        return num
    
    # Will return true if author has written books in database otherwise false
    def getAuthorWrites(idNum):
        cur = conn.cursor()
        cur.execute('Select count(*) FROM Writes WHERE AuthorId =:first', {"first": idNum})
        check = cur.fetchall()
        for c in check:
            valid = c[0]
        if valid > 0:
            return True
        else:
            return False 
        
    # Will return the books a reader has read
    def showBooks(num):
        cur = conn.cursor()
        cur.execute('SELECT Book.ISBN, Title, YearPublished, Rating, FirstName, LastName, Country FROM Reads JOIN Book JOIN Writes JOIN Author ON Book.ISBN = Reads.ISBN AND Writes.ISBN = Book.ISBN AND Writes.AuthorId = Author.AuthorId WHERE UserId =:id ORDER BY Title ASC', {"id": num})
        data = cur.fetchall()
        return data
    
    # Will return the number of books a reader has read
    def getNumBooks(Uid):
        cur = conn.cursor()
        cur.execute('SELECT count(*) FROM READS WHERE UserId =:id', {"id": Uid})
        data = cur.fetchall()
        for d in data:
            num = d[0]
        return num
    
    # Will get the average rating for an author based off the user
    def getAuthorAvg(num, person):
        cur = conn.cursor()
        cur.execute('SELECT round(avg(Reads.Rating),2) FROM Writes JOIN Book JOIN Reads ON Writes.ISBN = Book.ISBN AND Book.ISBN = Reads.ISBN WHERE Writes.AuthorId =:aid AND Reads.UserId =:uid', {"aid": num, "uid": person.getUserId()})
        data = cur.fetchall()
        for d in data:
            avg = d[0]
        return avg
    
    # Will get the author Id
    def getAuthId(first, last, country):
        cur = conn.cursor()
        cur.execute('SELECT AuthorId FROM Author WHERE FirstName =:f AND LastName =:l AND Country =:c', {"f": first, "l": last, "c": country})
        data = cur.fetchall()
        for d in data:
            num = d[0]
        return num
    
    # Will get the books written by an author that a reader has read
    def getBooksByAuthor(num, person):
        cur = conn.cursor()
        cur.execute('SELECT Book.ISBN, Title, YearPublished, Rating FROM Writes JOIN Book JOIN Reads ON Writes.ISBN = Book.ISBN AND Book.ISBN = Reads.ISBN WHERE Writes.AuthorId =:aid AND Reads.UserId =:uid ORDER BY Title ASC', {"aid": num, "uid": person.getUserId()})
        data = cur.fetchall()
        return data
    
    # Will get all the books that are above the average rating for a user
    def aboveAvg(userId):
        cur = conn.cursor()
        cur.execute("""SELECT Book.ISBN, Title, YearPublished, Rating, FirstName, LastName, Country
                        FROM Reads JOIN Book JOIN Writes JOIN Author
                        ON Book.ISBN = Reads.ISBN
                        AND Writes.ISBN = Book.ISBN
                        AND Writes.AuthorId = Author.AuthorId
                        WHERE UserId =:uid
                        AND Rating > (SELECT round(avg(Rating),2)
                                        FROM Reads
                                        WHERE UserId =:uid)
                        ORDER BY Rating DESC, Title ASC""", {"uid": userId})
        data = cur.fetchall()
        return data
    
    # Will get the average rating
    def avgRate(userId):
        cur = conn.cursor()
        cur.execute("SELECT round(avg(Rating),2) FROM Reads WHERE UserId =:uid", {"uid": userId})
        data = cur.fetchall()
        for d in data:
            num = d[0]
        return num
    
    # Will get the books based off of the keyword
    def keywords(userId, keyword):
        keyword = '%' + keyword + '%'
        cur = conn.cursor()
        cur.execute("""SELECT Book.ISBN, Title, YearPublished, Rating, FirstName, LastName, Country
                        FROM Reads JOIN Book JOIN Writes JOIN Author
                        ON Book.ISBN = Reads.ISBN
                        AND Writes.ISBN = Book.ISBN
                        AND Writes.AuthorId = Author.AuthorId
                        WHERE UserId =:uid
                        AND Book.Title Like :kw
                        ORDER BY Title ASC""", {"uid": userId, "kw": keyword})
        data = cur.fetchall()
        return data
    
    # Will get all the authors rated higher than the author entered
    def higherRatedAuthors(userId, authId):
        cur = conn.cursor()
        cur.execute("""SELECT Author.FirstName, Author.LastName, Author.Country, round(avg(Reads.Rating),2) AS Rate
                        FROM Author JOIN Writes JOIN Book JOIN Reads
                        ON Author.AuthorId = Writes.AuthorId
                        AND Writes.ISBN = Book.ISBN
                        AND Book.ISBN = Reads.ISBN
                        WHERE Reads.UserId =:uid
                        GROUP BY Writes.AuthorId
                        HAVING Rate > ( SELECT round(avg(Reads.Rating),2)
                                            FROM Writes JOIN Book JOIN Reads
                                            ON Writes.ISBN = Book.ISBN
                                            AND Book.ISBN = Reads.ISBN
                                            WHERE Writes.AuthorId =:aid
                                            AND Reads.UserId =:uid)
                        ORDER BY Author.LastName ASC""", {"uid": userId, "aid": authId})
        data = cur.fetchall()
        return data
    
    # Will get all the books that two users have antered that are the same
    def friendSameReads(userId, friend):
        cur = conn.cursor()
        cur.execute("""SELECT MyRating, Book.Title, FriendsRating
                           FROM Book JOIN (SELECT MyBooks.ISBN as SharedISBN, MyBooks.Rating AS MyRating, FriendsBooks.Rating AS FriendsRating
                                               FROM (SELECT Reads.ISBN, Reads.Rating
                                                         FROM Reads
                                                         WHERE Reads.UserId =:uid) AS MyBooks 
                                               JOIN (SELECT Reads.ISBN, Reads.Rating
                                                         FROM Reads
                                                         WHERE Reads.UserId = (SELECT Reader.UserId
                                                                                   FROM Reader
                                                                                   WHERE Reader.Username =:fri)) AS FriendsBooks
                                               ON MyBooks.ISBN = FriendsBooks.ISBN) AS SharedBooks
                           ON Book.ISBN = SharedISBN""", {"uid": userId, "fri": friend})
        data = cur.fetchall()
        return data