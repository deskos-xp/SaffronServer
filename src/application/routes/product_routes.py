from flask import make_response,request
from flask import current_app as app
from ..models.product import db,auth,ma,Product,ProductSchema
from ..models.vendor import Vendor,VendorSchema
from ..models.brand import Brand,BrandSchema
from ..models.manufacturer import Manufacturer,ManufacturerSchema
from ..models.departments import Department,DepartmentSchema
from ..models.weight import Weight,WeightSchema
from ..models.price import Price,PriceSchema
from werkzeug.utils import secure_filename
from werkzeug.wsgi import FileWrapper
from flask import send_file,send_from_directory
import json as Json
import os
from sqlalchemy.orm.attributes import flag_modified
from . import verify
from .. import delete,status,ccj,status_codes
from ..tools.barcode.barcodes import barcode_gen
from io import BytesIO
utypes=["upc_image","product_image"]
ALLOWED_EXTENSIONS=["png","jpg","jpeg"]

from .. import logging

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@auth.verify_password
def v(username,password):
    a=verify.verify_password(username,password)
    return a['authorized']

@app.route("/product/update/<ID>",methods=["post"])
@auth.login_required
def update_product(ID):
    assert ID != None
    json=request.get_json(force=True)
    json=ccj(json)
    assert json != None
    product=db.session.query(Product).filter_by(id=ID).first()
    for k in json.keys():
        if k in product.__dict__.keys():
            product.__dict__[k]=json[k]
            flag_modified(product,k)
    db.session.merge(product)
    db.session.flush()
    db.session.commit()
    return status(product,status=status_codes.UPDATED,msg="updated primary product key id:{}'s with keys for {}".format(product.id,",".join(json.keys())))

@app.route("/product/barcode/<ID>/<TYPE>",methods=["get"])
@auth.login_required
def get_barcode(ID:int,TYPE:str):
    assert ID != None
    assert TYPE != None
    product=db.session.query(Product).filter_by(id=ID).first()
    assert product != None
    assert len(product.upc)
    bard=barcode_gen(upc=product.upc,Type=TYPE)
    bard.buff.seek(0)
    img=bytes()
    while True:
        d=bard.buff.read(128)
        if not d:
            break
        img+=d
    bard=None
    del(bard)
    imgio=BytesIO()
    imgio.write(img)
    imgio.seek(0)
    logging.info("user is uploading {TYPE} for product ID'd by {ID}".format(**dict(TYPE=TYPE,ID=ID)))
    return send_file(imgio,mimetype="image/jpeg",as_attachment=True,attachment_filename="upc_image.jpeg")

@app.route("/product/update/<ID>/upload/<WHICH>",methods=["post"])
@auth.login_required
def upload_upc_image(ID,WHICH):
    assert WHICH != None
    assert ID != None
    product=db.session.query(Product).filter_by(id=ID).first()
    assert product != None
    if WHICH not in utypes:
        return status(product,status=status_codes.NOT_UPLOADED,msg="valid uploads are {}".format(','.join(utypes)))

    if 'file' not in request.files:
        return status(product,status=status_codes.NOT_UPLOADED,msg="no file provided")
    file=request.files['file']

    if file.filename == '':
        return status(product,status=status_codes.NOT_UPLOADED,msg="no file provided for uploading")
    if file and allowed_file(file.filename):
        fname=secure_filename(file.filename)
        fname="{}:{}:{}".format(WHICH,str(ID),fname)
        fullpath=os.path.join(app.root_path,os.path.join(app.config['UPLOAD_FOLDER'],fname))
        logging.debug(fullpath)
        product.__dict__[WHICH]=fname
        flag_modified(product,WHICH)
        db.session.merge(product)
        db.session.flush()
        db.session.commit()

        file.save(fullpath)
        return status(product,status=status_codes.UPLOADED,msg="file saved as {}!".format(fullpath))
    else:
        return status(product,status=status_codes.NOT_UPLOADED,msg="allowed filetypes are {}".format(','.join(ALLOWED_EXTENSIONS)))

@app.route("/product/get/<ID>/<WHICH>",methods=["get"])
@auth.login_required
def get_images(ID,WHICH):
    assert ID != None
    assert WHICH != None
    if WHICH not in utypes:
        return status(Product(),status=status_codes.NOT_UPLOADED,msg="valid images are {}".format(', '.join(utypes)))

    product=db.session.query(Product).filter_by(id=ID).first()
    assert product != None
    fname=product.__dict__[WHICH]
    p=os.path.join(app.root_path,app.config['UPLOAD_FOLDER'])
    logging.debug(p)
    return send_from_directory(p,fname)

@app.route("/product/new",methods=["post"])
@auth.login_required
def new_product():
        json=request.get_json(force=True)
        json=ccj(json)
        assert json != None
        if len(json.keys()) > 0:
            exists=db.session.query(Product).filter_by(**json).first()
            if exists != None:
                return status(exists,status=status_codes.OLD)
        product=Product(**json)
        db.session.add(product)
        db.session.commit()
        db.session.flush()
        return status(product,status=status_codes.NEW) 
        '''
        return """
product created!
ToDos:
    /product/update/<product_id>/add/weight/<weight_id>
    /product/update/<product_id>/add/price/<price_id>
    /product/update/<product_id>/add/vendor/<vendor_id>
    /product/update/<product_id>/add/brand/<brand_id>
    /product/update/<product_id>/add/manufacturer/<manufacturer_id>
    /product/update/<product_id>/add/department/<department_id>
    """
        '''
@app.route("/product/get/<product_id>",methods=["GET"])
@auth.login_required
def get_product_id(product_id):
    assert product_id != None
    product=db.session.query(Product).filter_by(id=product_id).first()
    if product == None:
        return status(Product(),status=status_codes.INVALID_ID,msg="no such product")
    productSchema = ProductSchema()
    return status(Product(),status=status_codes.OBJECT,object=productSchema.dump(product))

@app.route("/product/get",methods=["post"])
@auth.login_required
def get_products():
    json=request.get_json(force=True)
    json=ccj(json)
    assert json != None
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
    json_tagged={i:"%{}%".format(json[i]) for i in json.keys() }
    print(Product().as_dict())

    q = db.session.query(Product)
    for attr,value in json_tagged.items():
        q = q.filter(getattr(Product,attr).like(value))
    products=q.limit(limit).offset(page*limit).all()

    #products=db.session.query(Product).filter_by(**json).limit(limit).offset(page*limit).all()
    if products == []:
        return status(Product(),status=status_codes.INVALID_ID,msg="no products could be found!")
    productSchema=ProductSchema()
    products=[productSchema.dump(i) for i in products]
    return status(Product(),status=status_codes.OBJECTS,objects=Json.dumps(products))


@app.route("/product/delete/<product_id>",methods=["delete"])
@auth.login_required
def delete_product(product_id): 
    return delete(product_id,Product)

@app.route("/product/update/<product_id>/remove/vendor/<vendor_id>",methods=["get"])
@auth.login_required
def remove_vendor_to_product(product_id,vendor_id):
    assert product_id != None
    assert vendor_id != None
    vendor=db.session.query(Vendor).filter_by(id=vendor_id).first()
    assert vendor != None
    product=db.session.query(Product).filter_by(id=product_id).first()
    #removal=False
    print(product.vendors)
    try:
        product.vendors.remove(vendor)
    except:
        return status(product,status=status_codes.NOT_UPDATED) 
    
    db.session.commit()
    return status(product,status=status_codes.UPDATED)

@app.route("/product/update/<product_id>/add/weight/<weight_id>",methods=["get"])
@auth.login_required
def add_weight_to_product(product_id,weight_id):
    assert product_id != None
    assert weight_id != None
    weight=db.session.query(Weight).filter_by(id=weight_id).first()
    assert weight != None
    product=db.session.query(Product).filter_by(id=product_id).first()
    print(product.weight)
    if weight not in product.weight:
        product.weight.append(weight)
    else:
        return status(product,status=status_codes.NOT_UPDATED) 
    flag_modified(product,"weight")
    db.session.merge(product)
    db.session.flush()
    db.session.commit()
    return status(product,status=status_codes.UPDATED)

@app.route("/product/update/<product_id>/add/price/<price_id>",methods=["get"])
@auth.login_required
def add_price_to_product(product_id,price_id):
    assert product_id != None
    assert price_id != None
    price=db.session.query(Price).filter_by(id=price_id).first()
    assert price != None
    product=db.session.query(Product).filter_by(id=product_id).first()
    print(product.price)
    if price not in product.price:
        product.price.append(price)
    else:
        return status(Product(),status=status_codes.NOT_UPDATED)
    flag_modified(product,"price")
    db.session.merge(product)
    db.session.flush()
    db.session.commit()
    return status(Product(),status=status_codes.UPDATED)


@app.route("/product/update/<product_id>/add/vendor/<vendor_id>",methods=["get"])
@auth.login_required
def add_vendor_to_product(product_id,vendor_id):
    assert product_id != None
    assert vendor_id != None
    vendor=db.session.query(Vendor).filter_by(id=vendor_id).first()
    assert vendor != None
    product=db.session.query(Product).filter_by(id=product_id).first()
    print(product.vendors)
    if vendor not in product.vendors:
        product.vendors.append(vendor)
    else:
        return status(Product(),status=status_codes.NOT_UPDATED) 
    flag_modified(product,"vendors")
    db.session.merge(product)
    db.session.flush()
    db.session.commit()
    return status(Product(),status=status_codes.UPDATED)

@app.route("/product/update/<product_id>/remove/brand/<brand_id>",methods=["get"])
@auth.login_required
def remove_brand_to_product(product_id,brand_id):
    assert product_id != None
    assert brand_id != None
    brand=db.session.query(Brand).filter_by(id=brand_id).first()
    assert brand != None
    product=db.session.query(Product).filter_by(id=product_id).first()
    #removal=False
    print(product.brands)
    try:
        product.brands.remove(brand)
    except:
        return status(Product(),status=status_codes.NOT_UPDATED)
    
    db.session.commit()
    return status(Product(),status=status_codes.UPDATED)


@app.route("/product/update/<product_id>/add/brand/<brand_id>",methods=["get"])
@auth.login_required
def add_brand_to_product(product_id,brand_id):
    assert product_id != None
    assert brand_id != None
    brand=db.session.query(Brand).filter_by(id=brand_id).first()
    assert brand != None
    product=db.session.query(Product).filter_by(id=product_id).first()
    print(product.brands)
    if brand not in product.brands:
        product.brands.append(brand)
    else:
        return status(Product(),status=status_codes.NOT_UPDATED)
    flag_modified(product,"brands")
    db.session.merge(product)
    db.session.flush()
    db.session.commit()
    return status(Product(),status=status_codes.UPDATED)

@app.route("/product/update/<product_id>/remove/manufacturer/<manufacturer_id>",methods=["get"])
@auth.login_required
def remove_manufacturer_to_product(product_id,manufacturer_id):
    assert product_id != None
    assert manufacturer_id != None
    manufacturer=db.session.query(Manufacturer).filter_by(id=manufacturer_id).first()
    assert manufacturer != None
    product=db.session.query(Product).filter_by(id=product_id).first()
    #removal=False
    print(product.manufacturers)
    try:
        product.manufacturers.remove(manufacturer)
    except:
        return status(Product(),status=status_codes.NOT_UPDATED)
    
    db.session.commit()
    return status(Product(),status=status_codes.UPDATED)



@app.route("/product/update/<product_id>/add/manufacturer/<manufacturer_id>",methods=["get"])
@auth.login_required
def add_manufacturer_to_product(product_id,manufacturer_id):
    assert product_id != None
    assert manufacturer_id != None
    manufacturer=db.session.query(Manufacturer).filter_by(id=manufacturer_id).first()
    assert manufacturer != None
    product=db.session.query(Product).filter_by(id=product_id).first()
    print(product.manufacturers)
    if manufacturer not in product.manufacturers:
        product.manufacturers.append(manufacturer)
    else:
        return status(Product(),status=status_codes.NOT_UPDATED)
    flag_modified(product,"manufacturers")
    db.session.merge(product)
    db.session.flush()
    db.session.commit()
    return status(Product(),status=status_codes.UPDATED)

@app.route("/product/update/<product_id>/remove/department/<department_id>",methods=["get"])
@auth.login_required
def remove_department_to_product(product_id,department_id):
    assert product_id != None
    assert department_id != None
    department=db.session.query(Department).filter_by(id=department_id).first()
    assert department != None
    product=db.session.query(Product).filter_by(id=product_id).first()
    #removal=False
    print(product.departments)
    try:
        product.departments.remove(department)
    except:
        return status(Product(),status=status_codes.NOT_UPDATED)
    
    db.session.commit()
    return status(Product(),status=status_codes.UPDATED)

@app.route("/product/update/<product_id>/add/department/<department_id>",methods=["get"])
@auth.login_required
def add_department_to_product(product_id,department_id):
    assert product_id != None
    assert department_id != None
    department=db.session.query(Department).filter_by(id=department_id).first()
    assert department != None
    product=db.session.query(Product).filter_by(id=product_id).first()
    print(product.departments)
    if department not in product.departments:
        product.departments.append(department)
    else:
        return status(Product(),status=status_codes.NOT_UPDATED)
    flag_modified(product,"departments")
    db.session.merge(product)
    db.session.flush()
    db.session.commit()
    return status(Product(),status=status_codes.UPDATED)
