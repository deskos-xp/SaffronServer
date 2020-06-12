from flask import make_response,request
from flask import current_app as app
from ..models.manufacturer import db,auth,ma,Manufacturer,ManufacturerSchema
from ..models.address import Address,AddressSchema
import json as Json
import os
from sqlalchemy.orm.attributes import flag_modified
from . import verify
from .. import delete,status,ccj,status_codes
from ..decor import roles_required
from ..messages import messages

@app.route("/manufacturer/delete/<ID>",methods=["delete"])
@auth.login_required
@roles_required(roles=['admin'])
def delete_manufacturer(ID):
    if not ID:
        return messages.NO_ID.value
    return delete(ID,Manufacturer)


@auth.verify_password
def v(username,password):
    a=verify.verify_password(username,password)
    return a['authorized']

@app.route("/manufacturer/get/<ID>",methods=["get"])
@auth.login_required
@roles_required(roles=['admin','user'])
def get_manufacturer_id(ID):
    if ID == None:
        return status(Manufacturer(),status=status_codes.NO_ID_PROVIDED,msg="no manufacturer id provided!")
    manufacturer=db.session.query(Manufacturer).filter_by(id=ID).first()
    if manufacturer == None:
        return status(Manufacturer(),status=status_codes.INVALID_ID,msg="invalid manufacturer!")
    manufacturerSchema=ManufacturerSchema()
    return status(Manufacturer(),status=status_codes.OBJECT,object=manufacturerSchema.dump(manufacturer))


@app.route("/manufacturer/get",methods=["post"])
@auth.login_required
@roles_required(roles=['admin','user'])
def get_manufacturer():
    json=request.get_json(force=True)
    json=ccj(json)
    print(json)
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
    
    manufactureres=db.session.query(Manufacturer).filter_by(**json).limit(limit).offset(page*limit).all()
    manufacturerSchema=ManufacturerSchema()
    manufactureres=[manufacturerSchema.dump(i) for i in manufactureres]
    return status(Manufacturer(),status=status_codes.OBJECTS,objects=Json.dumps(manufactureres))

@app.route("/manufacturer/new",methods=["post"])
@auth.login_required
@roles_required(roles=['admin'])
def add_manufacturer():
    json=request.get_json(force=True)
    json=ccj(json)
    #assert json != None
    if not json:
        return messages.NO_JSON.value
    if len(json.keys()) > 0:
        qb=db.session.query(Manufacturer).filter_by(**json).first()
        if qb != None:
            return status(qb,"old")

    manufacturer=Manufacturer(**json)
    db.session.add(manufacturer)
    db.session.commit()
    db.session.flush()
    return status(manufacturer,status=status_codes.NEW) 

@app.route("/manufacturer/update/<ID>",methods=["post"])
@auth.login_required
@roles_required(roles=['admin'])
def update_manufacturer(ID):
    #assert ID != None
    if not ID:
        return messages.NO_ID.value
    manufacturer_old=db.session.query(Manufacturer).filter_by(id=ID).first()

    #assert manufacturer_old != None
    if not manufacturer_old:
        return messages.ENTITY_DOES_NOT_EXIST_MANUFACTURER.value
    json=request.get_json(force=True)
    json=ccj(json)
    #assert json != None
    if not json:
        return messages.NO_JSON.value

    for key in manufacturer_old.defaultdict().keys():
        if key not in ["id","address"]:
            #assert key in manufacturer_old.__dict__.keys()
            if key not in manufacturer_old.__dict__.keys():
                return messages.INVALID_KEY_MANUFACTURER.value
            #assert key in json.keys()
            if key not in json.keys():
                return messages.INVALID_KEY_MANUFACTURER.value
            manufacturer_old.__dict__[key]=json[key]
            flag_modified(manufacturer_old,key)
    db.session.merge(manufacturer_old)
    db.session.flush()
    db.session.commit()
    return status(manufacturer_old,status=status_codes.UPDATED) 


@app.route("/manufacturer/update/<ID>/add/address/<ADDRESS_ID>",methods=["get"])
@auth.login_required
@roles_required(roles=['admin'])
def update_manufacturer_with_address_add(ID,ADDRESS_ID):
    #assert ID != None
    if not ID:
        return messages.NO_ID.value
    #assert ADDRESS_ID != None
    if not ADDRESS_ID:
        return messages.NO_ADDRESS_ID.value

    manufacturer=db.session.query(Manufacturer).filter_by(id=ID).first()
    #assert manufacturer != None
    if not manufacturer:
        return messages.ENTITY_DOES_NOT_EXIST_MANUFACTURER.value

    address=db.session.query(Address).filter_by(id=ADDRESS_ID).first()
    #assert address != None
    if not address:
        return messages.ENTITY_DOES_NOT_EXIST_ADDRESS.value

    if address not in manufacturer.address:
        manufacturer.address.append(address)
        db.session.commit()
        return status(manufacturer,status=status_codes.UPDATED)
    else:
        return status(manufacturer,status=status_codes.NOT_UPDATED)

@app.route("/manufacturer/update/<ID>/remove/address/<ADDRESS_ID>",methods=["get"])
@auth.login_required
@roles_required(roles=['admin'])
def update_manufacturer_with_address_rm(ID,ADDRESS_ID):
    #assert ID != None
    if not ID:
        return messages.NO_ID.value
    #assert ADDRESS_ID != None
    if not ADDRESS_ID:
        return messages.NO_ADDRESS_ID.value

    manufacturer=db.session.query(Manufacturer).filter_by(id=ID).first()
    #assert manufacturer != None
    if not manufacturer:
        return messages.ENTITY_DOES_NOT_EXIST_MANUFACTURER

    address=db.session.query(Address).filter_by(id=ADDRESS_ID).first()
    #assert address != None
    if not address:
        return messages.ENTITY_DOES_NOT_EXIST_ADDRESS

    if address in manufacturer.address:
        manufacturer.address.remove(address)
        db.session.commit()
        return status(manufacturer,status=status_codes.UPDATED)
    else:
        return status(manufacturer,status=status_codes.NOT_UPDATED)


