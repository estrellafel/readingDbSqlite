#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This class will contain the information needed for the author.

@author: felixestrella
"""

class author:
    
    # A contructor for the author by takinging in the firstname, lastname, and country. Sets id to None.
    def __init__(self, firstName, lastName, country):
        self.firstName = firstName
        self.lastName = lastName
        self.country = country
        self.id = None
    
    # Will get the firstname
    def getFirst(self):
        return self.firstName
    
    # Will get the lastname
    def getLast(self):
        return self.lastName
    
    # Will get the country
    def getCountry(self):
        return self.country
    
    # Will get the id
    def getId(self):
        return self.id
    
    # Will set the id
    def setId(self, id):
        self.id = id