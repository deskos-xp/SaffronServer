from flask import make_response,request
from flask import current_app as app

from ..models.user import User,UserSchema
from ..models.productCount import ProductCount,ProductCountSchema,db,auth,ma
from ..models.product import Product,ProductSchema
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


@app.route("/productCount/new",methods=["post"])
@auth.login_required
@roles_required(roles=['admin'])
def new_productCount():
        json=request.get_json(force=True)
        #assert json != None
        if not json:
            return messages.NO_JSON.value
        json=ccj(json)
        if len(json.keys()) > 0:
            exists=db.session.query(ProductCount).filter_by(**json).first()
            if exists != None:
                return status(exists,status=status_codes.OLD) 
        productCount=ProductCount(**json)
        db.session.add(productCount)
        db.session.commit()
        db.session.flush()
        return status(productCount,status=status_codes.NEW)

@app.route("/productCount/get/<productCount_id>",methods=["GET"])
@auth.login_required
@roles_required(roles=['admin','user'])
def get_productCount_id(productCount_id):
    if not productCount_id:
        return messages.NO_PRODUCT_COUNT_ID.value
    #assert productCount_id != None
    productCount=db.session.query(ProductCount).filter_by(id=productCount_id).first()
    if productCount == None:
        return status(ProductCount(),status=status_codes.INVALID_ID,msg="no such productCount")
    productCountSchema = ProductCountSchema()
    return status(ProductCount(),status=status_codes.OBJECT,object=productCountSchema.dump(productCount))

@app.route("/productCount/get",methods=["post"])
@auth.login_required
@roles_required(roles=['admin','user'])
def get_productCount():
    json=request.get_json(force=True)
    json=ccj(json)
    #assert json != None
    if not json:
        return messages.NO_JSON.value
    page=json.get("page")
    limit=json.get("limit")
    if page == None:
        page=0
    else:
        json.__delitem__("page")

    if limit == None:
        limit = 10
    else:
        json.__delitem__("limit")
    productCount=db.session.query(ProductCount).filter_by(**json).limit(limit).offset(page*limit).all()
    if productCount == []:
        return status(ProductCount(),status=status_codes.INVALID_ID,msg="no such productCount")
    productCountSchema=ProductCountSchema()
    productCounts=[productCountSchema.dump(i) for i in productCount]
    return status(ProductCount(),status=status_codes.OBJECTS,objects=Json.dumps(productCounts))


@app.route("/productCount/delete/<productCount_id>",methods=["delete"])
@auth.login_required
@roles_required(roles=['admin'])
def delete_productCount(productCount_id): 
    if not productCount_id:
        return messages.NO_PRODUCT_COUNT_ID.value

    return delete(productCount_id,ProductCount)

@app.route("/productCount/update/<productCount_id>",methods=["post"])
@auth.login_required
@roles_required(roles=['admin'])
def update_productCount(productCount_id):
    #assert productCount_id != None
    if not productCount_id:
        return messages.NO_PRODUCT_COUNT_ID.value

    json=request.get_json(force=True)
    json=ccj(json)
    #assert json != None
    if not json:
        return messages.NO_JSON.value
    productCount=db.session.query(ProductCount).filter_by(id=productCount_id).first()
    #assert productCount != None
    if not productCount:
        return messages.ENTITY_DOES_NOT_EXIST_PRODUCT_COUNT.value

    productCount.__dict__.update(json)
    for key in json.keys():
        flag_modified(productCount,key)
    
    db.session.merge(productCount)
    db.session.flush()
    db.session.commit()
    return status(productCount,status=status_codes.UPDATED) 

@app.route("/productCount/update/<productCount_id>/remove/product/<product_id>",methods=["get"])
@auth.login_required
@roles_required(roles=['admin'])
def remove_product_from_productCount(productCount_id,product_id):
    #assert productCount_id != None
    if not productCount_id:
        return messages.NO_PRODUCT_COUNT_ID.value
    #assert product_id != None
    if not product_id:
        return messages.NO_PRODUCT_ID.value

    product=db.session.query(Product).filter_by(id=product_id).first()
    #assert product != None
    if not product:
        return messages.ENTITY_DOES_NOT_EXIST_PRODUCT.value
    productCount=db.session.query(ProductCount).filter_by(id=productCount_id).first()
    #removal=False
    print(productCount.products)
    try:
        productCount.products.remove(product)
    except:
        return status(productCount,status=status_codes.NOT_UPDATED)
    
    db.session.commit()
    return status(productCount,status=status_codes.UPDATED)

@app.route("/productCount/update/<productCount_id>/add/product/<product_id>",methods=["get"])
@auth.login_required
@roles_required(roles=['admin'])
def add_product_to_productCount(productCount_id,product_id):
    #assert productCount_id != None
    if not productCount_id:
        return messages.NO_PRODUCT_COUNT_ID.value
    #assert product_id != None
    if not product_id:
        return messages.NO_PRODUCT_ID.value

    product=db.session.query(Product).filter_by(id=product_id).first()
    #assert product != None
    if not product:
        return messages.ENTITY_DOES_NOT_EXIST_PRODUCT.value
    productCount=db.session.query(ProductCount).filter_by(id=productCount_id).first()
    #assert productCount != None
    if not productCount:
        return messages.ENTITY_DOES_NOT_EXIST_PRODUCT_COUNT.value

    print(productCount.products)
    if product not in productCount.products:
        productCount.products.append(product)
    else:
        return status(productCount,status=status_codes.NOT_UPDATED)
    flag_modified(productCount,"products")
    db.session.merge(productCount)
    db.session.flush()
    db.session.commit()
    return status(productCount,status=status_codes.UPDATED)


