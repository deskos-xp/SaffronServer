from flask import make_response,request
from flask import current_app as app
from ..models.address import db,auth,ma,Address,AddressSchema
from ..models.brand import Brand
from ..models.vendor import Vendor
from ..models.manufacturer import Manufacturer
import json as Json
import os
from sqlalchemy.orm.attributes import flag_modified
from . import verify
from .. import delete,status,ccj,status_codes
from ..decor import roles_required
from ..messages import messages

@app.route("/address/delete/<ID>",methods=["delete"])
@auth.login_required
@roles_required(roles=['admin'])
def delete_address(ID):
    ##assert ID != None
    if not ID:
        return messages.NO_ID.value
    return delete(ID,Address)

@auth.verify_password
def v(username,password):
    a=verify.verify_password(username,password)
    return a['authorized']

@app.route("/address/get/<ID>",methods=["get"])
@auth.login_required
@roles_required(roles=['admin','user'])
def get_address_id(ID):
    if ID == None:
        return status(Address(),status=status_codes.NO_ID_PROVIDED,msg="no address id provided!")
    address=db.session.query(Address).filter_by(id=ID).first()
    if Address == None:
        return status(Address(),status=status_codes.INVALID_ID,msg="invalid address!")
    addressSchema=AddressSchema()
    return status(Address(),status=status_codes.OBJECT,object=addressSchema.dump(address))

@app.route("/address/get",methods=["post"])
@auth.login_required
@roles_required(roles=['admin','user'])
def get_address():
    json=request.get_json(force=True)
    json=ccj(json)
    #print(json)
    #assert json != None
    if not json:
        return messages.NO_JSON.value
    page=json.get('page')
    limit=json.get('limit')
    if page == None:
        page=0
    if limit == None:
        limit=10
    
    if json.get('limit') != None:
        json.__delitem__('limit')
    if json.get('page') != None:
        json.__delitem__('page')
    
    addresses=db.session.query(Address).filter_by(**json).limit(limit).offset(page*limit).all()
    addressSchema=AddressSchema()
    addresses=[addressSchema.dump(i) for i in addresses]
    return status(Address(),status=status_codes.OBJECTS,objects=Json.dumps(addresses))

@app.route("/address/new",methods=["post"])
@auth.login_required
@roles_required(roles=['admin'])
def add_address():
    json=request.get_json(force=True)
    json=ccj(json)
    if not json:
        return messages.NO_JSON.value
    if len(json.keys()) > 0:
        address=db.session.query(Address).filter_by(**json).first()
        if address != None:
            return  status(address,status=status_codes.OLD)
    address=Address(**json)
    db.session.add(address)
    db.session.commit()
    db.session.flush()
    return status(address,status=status_codes.NEW)
    
@app.route("/address/update/<ID>",methods=["post"])
@auth.login_required
@roles_required(roles=['admin'])
def update_address(ID):
    #assert ID != None
    if not ID:
        return messages.NO_ID.value
    address_old=db.session.query(Address).filter_by(id=ID).first()
    #assert address_old != None
    if not address_old:
        return messages.ENTITY_DOES_NOT_EXIST.value
    json=request.get_json(force=True)
    json=ccj(json)
    #assert json != None
    if not json:
        return messages.NO_JSON.value
    for key in address_old.defaultdict().keys():
        if key not in ["id"]:
            #assert key in address_old.__dict__.keys()
            if key not in address_old.__dict__.keys():
                return messages.INVALID_KEY_ADDRESS.value

            #assert key in json.keys()
            if key not in json.keys():
                return messages.INVALID_KEY_ADDRESS.values

            address_old.__dict__[key]=json[key]
            flag_modified(address_old,key)
    db.session.merge(address_old)
    db.session.flush()
    db.session.commit()
    return status(address_old,status=status_codes.UPDATED) 
