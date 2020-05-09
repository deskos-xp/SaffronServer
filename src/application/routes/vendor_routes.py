from flask import make_response,request
from flask import current_app as app
from ..models.vendor import db,auth,ma,Vendor,VendorSchema
from ..models.address import Address,AddressSchema

import json as Json
import os
from sqlalchemy.orm.attributes import flag_modified
from . import verify
from .. import delete,status,ccj,status_codes

@app.route("/vendor/delete/<vendor_id>",methods=["delete"])
@auth.login_required
def delete_vendor(vendor_id): 
    return delete(vendor_id,Vendor)


@auth.verify_password
def v(username,password):
    a=verify.verify_password(username,password)
    return a['authorized']

@app.route("/vendor/get/<ID>",methods=["get"])
@auth.login_required
def get_vendor_id(ID):
    if ID == None:
        return status(Vendor(),status=status_codes.NO_ID_PROVIDED,msg="no vendor id provided!")
    vendor=db.session.query(Vendor).filter_by(id=ID).first()
    if vendor == None:
        return status(Vendor(),status=status_codes.INVALID_ID,msg="invalid vendor!")
    vendorSchema=VendorSchema()
    return status(Vendor(),status=status_codes.OBJECT,object=vendorSchema.dump(vendor))


@app.route("/vendor/get",methods=["post"])
@auth.login_required
def get_vendor():
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
    
    vendores=db.session.query(Vendor).filter_by(**json).limit(limit).offset(page*limit).all()
    vendorSchema=VendorSchema()
    vendores=[vendorSchema.dump(i) for i in vendores]
    return status(Vendor(),status=status_codes.OBJECTS,objects=Json.dumps(vendores))

@app.route("/vendor/new",methods=["post"])
@auth.login_required
def add_vendor():
    json=request.get_json(force=True)
    assert json != None
    json=ccj(json)
    if len(json.keys()) > 0:
        qb=db.session.query(Vendor).filter_by(**json).first()
        if qb != None:
            return status(qb,"old") 
    vendor=Vendor(**json)
    db.session.add(vendor)
    db.session.commit()
    db.session.flush()
    return status(vendor,status=status_codes.NEW)

@app.route("/vendor/update/<ID>",methods=["post"])
@auth.login_required
def update_vendor(ID):
    assert ID != None
    vendor_old=db.session.query(Vendor).filter_by(id=ID).first()
    assert vendor_old != None
    json=request.get_json(force=True)
    json=ccj(json)
    assert json != None
    for key in vendor_old.defaultdict().keys():
        if key not in ["id"]:
            assert key in vendor_old.__dict__.keys()
            assert key in json.keys()
            vendor_old.__dict__[key]=json[key]
            flag_modified(vendor_old,key)
    db.session.merge(vendor_old)
    db.session.flush()
    db.session.commit()
    return status(vendor,msg=status_codes.NEW) 

@app.route("/vendor/update/<ID>/add/address/<ADDRESS_ID>",methods=["get"])
@auth.login_required
def update_vendor_with_address_add(ID,ADDRESS_ID):
    assert ID != None
    assert ADDRESS_ID != None
    vendor=db.session.query(Vendor).filter_by(id=ID).first()
    assert vendor != None
    address=db.session.query(Address).filter_by(id=ADDRESS_ID).first()
    assert address != None
    if address not in vendor.address:
        vendor.address.append(address)
        db.session.commit()
        return status(vendor,status=status_codes.UPDATED)
    else:
        return status(vendor,status=status_codes.NOT_UPDATED)

@app.route("/vendor/update/<ID>/remove/address/<ADDRESS_ID>",methods=["get"])
@auth.login_required
def update_vendor_with_address_rm(ID,ADDRESS_ID):
    assert ID != None
    assert ADDRESS_ID != None
    vendor=db.session.query(Vendor).filter_by(id=ID).first()
    assert vendor != None
    address=db.session.query(Address).filter_by(id=ADDRESS_ID).first()
    assert address != None
    if address in vendor.address:
        vendor.address.remove(address)
        db.session.commit()
        return status(vendor,status=status_codes.UPDATED)
    else:
        return status(vendor,status=status_codes.NOT_UPDATED)


