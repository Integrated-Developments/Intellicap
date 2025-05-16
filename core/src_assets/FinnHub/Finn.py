Version = 'Scr: 0.0.1'

## SS- Importing Libraries ----- ##
import requests #type:ignore
import json #type:ignore
import datetime #type:ignore
import os, sys #type:ignore
import time #type:ignore
from sqlalchemy import create_engine, Column, Integer, String #type:ignore
from sqlalchemy.ext.declarative import declarative_base #type:ignore
from sqlalchemy.orm import sessionmaker #type:ignore

## SS- Global Variables ----- ##
_dir = None

def Base_Directory () :
    if getattr(sys, 'frozen', False) :
        _dir = os.path.dirname (sys.executable)
    else:
        _dir = os.path.dirname(os.path.abspath(__file__))

def Prints (*args) :
    for txt in args :
        print (txt)
        print ("")

def SetUp_Database () :
    Base = declarative_base()
    engine = create_engine('sqlite:///FinnHub.db', echo=True)
    Session = sessionmaker(bind=engine)
    session = Session()
    
    class Api (Base) :
        __tablename__ = 'Api'
        key = Column(String, primary_key=True, unique=True, index=True) # The API Key
        username = Column(String, nullable=False) # The username
        cntAll = Column(Integer, default=0) # Total Calls Made Ever
        cntMonth = Column(Integer, default=0) # Calls per month against limit
        cntDay = Column(Integer, default=0) # Calls per day against limit
        cntHour = Column(Integer, default=0) # Calls per hour against limit
        last = Column(String, default=None) # Last time called
    
    class Symbols (Base) :
        __tablename__ = 'Symbols'
        symbol = Column(Integer, primary_key=True, unique=True, index=True) # The Symbol
        active = Column(Integer, default=0) # Use it or not

    Base.metadata.create_all(engine)

    def DB_AddApi (api_key=str, username=str) :
        new_key = Api(key=api_key, username=username)
        session.add(new_key)
        session.commit()
