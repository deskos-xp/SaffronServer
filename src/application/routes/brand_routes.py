from flask import make_response,request
from flask import current_app as app
from ..models.brand import db,auth,ma,Brand,BrandSchema
from ..models.address import Address,AddressSchema
from ..models.product import Product

import json as Json
import os
from sqlalchemy.orm.attributes import flag_modified
from . import verify
from .. import delete,status,ccj,status_codes
from ..decor import roles_required
from ..messages import messages
@auth.verify_password
def v(username,password):
    a=verify.verify_password(username,password)
    return a['authorized']

@app.route("/brand/get/<ID>",methods=["get"])
@auth.login_required
@roles_required(roles=['admin','user'])
def get_brand_id(ID):
    if ID == None:
        return status(Brand(),status=status_codes.NO_ID_PROVIDED,msg="no brand id provided!")
    brand=db.session.query(Brand).filter_by(id=ID).first()
    if brand == None:
        return status(Brand(),status=status_codes.INVALID_ID,msg="invalid brand!")
    brandSchema=BrandSchema()
    return status(brand,status=status_codes.OBJECT,object=brandSchema.dump(brand))


@app.route("/brand/get",methods=["post"])
@auth.login_required
@roles_required(roles=['admin','user'])
def get_brand():
    json=request.get_json(force=True)
    json=ccj(json)
    print(json)
    #assert json != None
    if json == None:
        return messages.NO_JSON.values
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
    
    brandes=db.session.query(Brand).filter_by(**json).limit(limit).offset(page*limit).all()
    brandSchema=BrandSchema()
    brandes=[brandSchema.dump(i) for i in brandes]
    return status(Brand(),status=status_codes.OBJECTS,objects=Json.dumps(brandes))

@app.route("/brand/new",methods=["post"])
@auth.login_required
@roles_required(roles=['admin'])
def add_brand():
    json=request.get_json(force=True)
    json=ccj(json)
    #assert json != None
    if json == None:
        return messages.NO_JSON.value
    if len(json.keys()) > 0:
        qb=db.session.query(Brand).filter_by(**json).first()
        if qb != None:
            return status(qb,status=status_codes.OLD)

    brand=Brand(**json)
    db.session.add(brand)
    db.session.commit()
    db.session.flush()
    return status(brand,status=status_codes.NEW)

@app.route("/brand/delete/<ID>",methods=["delete"])
@auth.login_required
@roles_required(roles=['admin'])
def delete_band(ID):
    if ID == None:
        return messages.NO_ID.value
    return delete(ID,Brand)


@app.route("/brand/update/<ID>/add/address/<ADDRESS_ID>",methods=["get"])
@auth.login_required
@roles_required(roles=['admin'])
def update_brand_with_address_add(ID,ADDRESS_ID):
    #assert ID != None
    if not ID:
        return messages.NO_ID.value
    #assert ADDRESS_ID != None
    if not ADDRESS_ID:
        return messages.NO_ADDRESS_ID.value
    brand=db.session.query(Brand).filter_by(id=ID).first()
    #assert brand != None
    if not brand:
        return messages.ENTITY_DOES_NOT_EXIST_BRAND.value
    address=db.session.query(Address).filter_by(id=ADDRESS_ID).first()
    #assert address != None
    if not address:
        return messages.ENTITY_DOES_NOT_EXIST_ADDRESS.value

    if address not in brand.address:
        brand.address.append(address)
        db.session.commit()
        return status(brand,status=status_codes.UPDATED)
    else:
        return status(brand,status=status_codes.NOT_UPDATED)

@app.route("/brand/update/<ID>/remove/address/<ADDRESS_ID>",methods=["get"])
@auth.login_required
@roles_required(roles=['admin'])
def update_brand_with_address_rm(ID,ADDRESS_ID):
    if not ID:
        return messages.NO_ID.value
    #assert ID != None
    if not ADDRESS_ID:
        return messages.NO_ADDRESS_ID.value

    #assert ADDRESS_ID != None
    brand=db.session.query(Brand).filter_by(id=ID).first()
    #assert brand != None
    if not brand:
        return messages.ENTITY_DOES_NOT_EXIST_BRAND.value
    address=db.session.query(Address).filter_by(id=ADDRESS_ID).first()
    #assert address != None
    if not address:
        return messages.ENTITY_DOES_NOT_EXIST_ADDRESS.value

    if address in brand.address:
        brand.address.remove(address)
        db.session.commit()
        return status(brand,status=status_codes.UPDATED)
    else:
        return status(brand,status=status_codes.NOT_UPDATED)

@app.route("/brand/update/<ID>",methods=["post"])
@auth.login_required
@roles_required(roles=['admin'])
def update_brand(ID):
    #assert ID != None
    if not ID:
        return messages.NO_ID.value
    brand_old=db.session.query(Brand).filter_by(id=ID).first()
    #assert brand_old != None
    if not brand_old:
        return messages.ENTITY_DOES_NOT_EXIST_BRAND.value
    json=request.get_json(force=True)
    json=ccj(json)
    #assert json != None
    if not json:
        return messages.NO_JSON.value
    for key in brand_old.defaultdict().keys():
        if key not in ["id","address"]:
            #assert key in brand_old.__dict__.keys()
            if key not in brand_old.__dict__.keys():
                return messages.INVALID_KEY_BRAND.value
            #assert key in json.keys()
            if key not in json.keys():
                return messages.INVALID_KEY_BRAND.value

            brand_old.__dict__[key]=json[key]
            flag_modified(brand_old,key)
    db.session.merge(brand_old)
    db.session.flush()
    db.session.commit()
    return status(brand_old,status=status_codes.UPDATED)
