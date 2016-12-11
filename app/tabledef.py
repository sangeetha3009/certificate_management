from sqlalchemy import *
from sqlalchemy import create_engine, ForeignKey
from sqlalchemy import Column, Date, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref
from database import Base 
from werkzeug.security import generate_password_hash, \
     check_password_hash

engine = create_engine('postgresql://postgres:password@localhost/postgres', echo=True)
	 
########################################################################
class customers(Base):
	""""""
	__tablename__ = "customers"
	 
	id = Column(Integer, primary_key=True)
	customer_name = Column(String)
        customer_email = Column(String)
	password = Column(String)
	 
	#----------------------------------------------------------------------
	def __init__(self, customer_name, password,customer_email):
	    """"""
	    self.customer_email = customer_email
	    self.customer_name=customer_name
	    self.password=generate_password_hash(password)
	
	def set_password(self,password):
	    self.pw_hash=generate_password_hash(password)
	    return self.pw_hash
	
	def check_password(self,password):
	    return check_password_hash(self.password,password)
	
# create tables
Base.metadata.create_all(engine)
