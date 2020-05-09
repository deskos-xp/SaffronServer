from flask import make_response,request
from flask import current_app as app
from ..models.manufacturer import db,auth,ma,Manufacturer,ManufacturerSchema
from ..models.address import Address,AddressSchema
import json as Json
import os
from sqlalchemy.orm.attributes import flag_modified
from . import verify
from .. import delete,status,ccj,status_codes

@app.route("/manufacturer/delete/<ID>",methods=["delete"])
@auth.login_required
def delete_manufacturer(ID):
    return delete(ID,Manufacturer)


@auth.verify_password
def v(username,password):
    a=verify.verify_password(username,password)
    return a['authorized']

@app.route("/manufacturer/get/<ID>",methods=["get"])
@auth.login_required
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
def get_manufacturer():
    json=request.get_json(force=True)
    json=ccj(json)
    print(json)
    assert json != None
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
def add_manufacturer():
    json=request.get_json(force=True)
    json=ccj(json)
    assert json != None

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
def update_manufacturer(ID):
    assert ID != None
    manufacturer_old=db.session.query(Manufacturer).filter_by(id=ID).first()
    assert manufacturer_old != None
    json=request.get_json(force=True)
    json=ccj(json)
    assert json != None
    for key in manufacturer_old.defaultdict().keys():
        if key not in ["id"]:
            assert key in manufacturer_old.__dict__.keys()
            assert key in json.keys()
            manufacturer_old.__dict__[key]=json[key]
            flag_modified(manufacturer_old,key)
    db.session.merge(manufacturer_old)
    db.session.flush()
    db.session.commit()
    return status(manufacturer,status=status_codes.UPDATED) 


@app.route("/manufacturer/update/<ID>/add/address/<ADDRESS_ID>",methods=["get"])
@auth.login_required
def update_manufacturer_with_address_add(ID,ADDRESS_ID):
    assert ID != None
    assert ADDRESS_ID != None
    manufacturer=db.session.query(Manufacturer).filter_by(id=ID).first()
    assert manufacturer != None
    address=db.session.query(Address).filter_by(id=ADDRESS_ID).first()
    assert address != None
    if address not in manufacturer.address:
        manufacturer.address.append(address)
        db.session.commit()
        return status(manufacturer,status=status_codes.UPDATED)
    else:
        return status(manufacturer,status=status_codes.NOT_UPDATED)

@app.route("/manufacturer/update/<ID>/remove/address/<ADDRESS_ID>",methods=["get"])
@auth.login_required
def update_manufacturer_with_address_rm(ID,ADDRESS_ID):
    assert ID != None
    assert ADDRESS_ID != None
    manufacturer=db.session.query(Manufacturer).filter_by(id=ID).first()
    assert manufacturer != None
    address=db.session.query(Address).filter_by(id=ADDRESS_ID).first()
    assert address != None
    if address in manufacturer.address:
        manufacturer.address.remove(address)
        db.session.commit()
        return status(manufacturer,status=status_codes.UPDATED)
    else:
        return status(manufacturer,status=status_codes.NOT_UPDATED)


