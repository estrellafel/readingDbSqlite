#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This class will contain the information needed for the reader (aka user).

@author: felixestrella
"""

class reader:
    
    # A constructor for the reader by taking in a username and password. Will set userId to None.
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.userId = None
    
    # Will get the password of the reader
    def getPassword(self):
        return self.password
    
    # Will get the username of the reader
    def getUsername(self):
        return self.username
    
    # Will set the userId for the reader by  taking in a number
    def setUserId(self, number):
        self.userId = number
    
    # Will get the userId for a reader.
    def getUserId(self):
        return self.userId