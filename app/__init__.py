import os
import json
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import *
from tabledef import *
from flask import Flask,Response,request,current_app,session,abort,jsonify
from database import *
import requests
from flask_pymongo import PyMongo
from createCert import *

app=Flask(__name__)
app.config.from_object('config')
db=SQLAlchemy(app)
app.config['MONGO_DBNAME']='customers_certs'
app.config['MONGO_URI']='mongodb://mongodb:password@localhost:27017/customers_certs'
mongo=PyMongo(app)

@app.route('/signup-customer',methods=['POST'])
def admin_signup():
    POST_USERNAME=str(request.json.get('customer_name'))
    POST_PASSWORD=str(request.json.get('password'))
    POST_EMAIL=str(request.json.get('customer_email'))
    u=customers(POST_USERNAME,POST_PASSWORD,POST_EMAIL)
    try:
        db.session.add(u)
        db.session.commit()
	mongo_cust=mongo.db.customers_certs
        mongo_cust.insert({"id":u.id,"customer_name":POST_USERNAME})
        return jsonify({"status":"Signup Success"}),200
    except Exception as e:
	print "Exception was ",e
	return jsonify({"status":"Signup Failure"}),202

@app.route('/delete-customer',methods=['POST'])
def admin_delete():
    POST_EMAIL=str(request.json.get('customer_email'))
    POST_PASSWORD=str(request.json.get('password'))
    Session=sessionmaker(bind=engine)
    s=Session()
    try:
        query=s.query(customers).filter(customers.customer_email.in_([POST_EMAIL]))
        result=query.first()
    except Exception as e:
        return jsonfiy({"error":"User not found in table"}),202
    try:
        is_authen=result.check_password(POST_PASSWORD)
        if is_authen:
            t=s.query(customers).filter(customers.id.in_([str(result.id)]))
            t.delete(synchronize_session=False)
	    s.commit()
            mongo_cust=mongo.db.customers_certs
            mongo_cust.remove({"id":result.id})
	    return "Deletion performed ",200	    
        else:
            return ({"error":"Authentication failed!"}),202
    except Exception as e:
        return jsonify({"error":"Deletion Failure"}),202
    
@app.route('/create-certificate',methods=['POST'])
def createCert():
    POST_EMAIL=str(request.json.get('customer_email'))
    POST_PASSWORD=str(request.json.get('password'))
    Session=sessionmaker(bind=engine)
    s=Session()
    query=s.query(customers).filter(customers.customer_email.in_([POST_EMAIL]))
    result=query.first()
    try:
        if result:
            is_authen=result.check_password(POST_PASSWORD)
            if is_authen:
                session['logged_in']=True
                t=generate_ssl(request.json.get('domain'),POST_EMAIL,request.json.get('country'),result.id)
	        mongo_cust=mongo.db.customers_certs
                mongo_cust.insert({"id":result.id,"certificate_name":t,"status":"active"})
		return jsonify({"certificate_name":t}),200
            else:
                return jsonify({"error":"Authentication failed for user to create certificate"}),202
	else:
		return jsonify({"error":"User not found"}),202
    except Exception as e:
	return jsonify({"error":"Error in certificate creation"}),202    
	    
@app.route('/customer-signin',methods=['POST'])
def admin_signin():
    POST_EMAIL=str(request.json.get('customer_email'))
    POST_PASSWORD=str(request.json.get('password'))
    Session=sessionmaker(bind=engine)
    s=Session()
    query=s.query(customers).filter(customers.customer_email.in_([POST_EMAIL]))
    result=query.first()
    try:
        if result:
            is_authen=result.check_password(POST_PASSWORD)
            if is_authen:
	        session['logged_in']=True
	        return jsonify({"status":"Signin Success"}),200
            else:
		return jsonify({"error":"Authentication failed"}),202
	else:
	    return jsonify({"error":"User not found"}),202
    except Exception as e:
	return jsonify({"error":"Signin Failure"}),202


@app.route('/show-all-Certificates',methods=['POST'])
def showCerts():
    POST_EMAIL=str(request.json.get('customer_email'))
    POST_PASSWORD=str(request.json.get('password'))
    Session=sessionmaker(bind=engine)
    s=Session()
    query=s.query(customers).filter(customers.customer_email.in_([POST_EMAIL]))
    result=query.first()
    certificates=[]
    try:
        if result:
            is_authen=result.check_password(POST_PASSWORD)
            if is_authen:
                session['logged_in']=True
                mongo_cust=mongo.db.customers_certs
                for c in mongo_cust.find({"id":result.id,"status":"active"},{"certificate_name":1,"_id":0}):
  		    certificates.append(c)
                return jsonify({"certificates":certificates}),200
            else:
                return jsonify({"error":"Authentication failed"}),202
	else:
		return jsonify({"error":"User not found"}),202
    except Exception as e:
        return jsonify({"error":"Unable to retrieve active certificates for the user"}),202

@app.route('/deactivate-certificate',methods=['POST'])
def deactivateCert():
    POST_EMAIL=str(request.json.get('customer_email'))
    POST_PASSWORD=str(request.json.get('password'))
    Session=sessionmaker(bind=engine)
    s=Session()
    query=s.query(customers).filter(customers.customer_email.in_([POST_EMAIL]))
    result=query.first()
    try:
        if result:
            is_authen=result.check_password(POST_PASSWORD)
            if is_authen:
                mongo_cust=mongo.db.customers_certs
                mongo_cust.update_one({"id":result.id,"certificate_name":request.json.get('certificate_name'),"status":"active"},{"$set":{"status":"deactivated"}})
                return jsonify({"status":"certificate deactivated"}),200
            else:
                return jsonify({"error":"Authentication failed"}),202
	else:
	    return jsonify({"error":"User not found"}),202
    except Exception as e:
        return jsonify({"error":"Either certificate name is incorrect or it is already inactive"}),202



@app.route('/show-certificate',methods=['POST'])
def showCert():
    POST_EMAIL=str(request.json.get('customer_email'))
    POST_PASSWORD=str(request.json.get('password'))
    Session=sessionmaker(bind=engine)
    s=Session()
    query=s.query(customers).filter(customers.customer_email.in_([POST_EMAIL]))
    result=query.first()
    try:
        if result:
	    path=os.path.dirname(os.path.abspath(__file__))+"/"
            is_authen=result.check_password(POST_PASSWORD)
            if is_authen:
		file=path+request.json.get('certificate_name')
                f=open(str(file),'r')
		read=f.read()
		return jsonify({"certificate-content":read}),200
            else:
                return jsonify({"error":"Authentication failed"}),202
        else:
            return jsonify({"error":"User not found"}),202
    except Exception as e:
        return jsonify({"error":"Error in displaying content of certificate!"}),202

