#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This class will contain the information needed for the author.

@author: felixestrella
"""

class book:
    
    # A constructor for book that takes in the ISBN, title, and year published.
    def __init__(self, ISBN, title, yearPublished):
        self.ISBN = ISBN
        self.title = title
        self.yearPublished = yearPublished
    
    # Will get the ISBN
    def getISBN(self):
        return self.ISBN
    
    # Will get the title
    def getTitle(self):
        return self.title
    
    # Will get the year published
    def getYear(self):
        return self.yearPublished
    
    