from .. import db,ma,auth
from .vendor import Vendor,VendorSchema
from .brand import Brand,BrandSchema
from .manufacturer import Manufacturer,ManufacturerSchema
from .departments import Department,DepartmentSchema
#from .weight import Weight,WeightSchema
#from .price import Price,PriceSchema
from .as_dict import AsDict

product_vendors = db.Table('product_vendors',db.metadata,
        db.Column("product_id",db.Integer,db.ForeignKey("products.id"),unique=True),
        db.Column("vendors_id",db.Integer,db.ForeignKey("vendors.id"))
        )
 
product_brands = db.Table('product_brands',db.metadata,
        db.Column("product_id",db.Integer,db.ForeignKey("products.id"),unique=True),
        db.Column("brands_id",db.Integer,db.ForeignKey("brands.id"))
        )               

product_manufacturers = db.Table('product_manufacturers',db.metadata,
        db.Column("product_id",db.Integer,db.ForeignKey("products.id"),unique=True),
        db.Column("manufacturers_id",db.Integer,db.ForeignKey("manufacturers.id"))
        )

product_departments = db.Table('product_departments',db.metadata,
        db.Column("product_id",db.Integer,db.ForeignKey("products.id"),unique=True),
        db.Column("departments_id",db.Integer,db.ForeignKey("departments.id"))
        )
'''
product_weight = db.Table('product_weight',db.metadata,
        db.Column("product_id",db.Integer,db.ForeignKey("products.id"),unique=True),
        db.Column("weight_id",db.Integer,db.ForeignKey("weight.id"))
        )
product_price = db.Table('product_price',db.metadata,
        db.Column("product_id",db.Integer,db.ForeignKey("products.id"),unique=True),
        db.Column("price_id",db.Integer,db.ForeignKey("price.id"))
        )
'''
class Product(db.Model,AsDict):
    __tablename__="products"
    #vendor_id=db.Column(db.Integer,db.ForeignKey('vendors.id'))
    vendors=db.relationship("Vendor",secondary=product_vendors,backref=db.backref("products"))

    #manufacturer_id=db.Column(db.Integer,db.ForeignKey("manufacturers.id"))
    manufacturers=db.relationship("Manufacturer",secondary=product_manufacturers,backref=db.backref("products"))

    #brand_id=db.Column(db.Integer,db.ForeignKey("brands.id"))
    brands=db.relationship("Brand",secondary=product_brands,backref=db.backref("products"))

    #department_id=db.Column(db.Integer,db.ForeignKey("departments.id"))
    departments=db.relationship("Department",secondary=product_departments,backref=db.backref("products"))

    id = db.Column(db.Integer,primary_key=True)


    name=db.Column(db.String(length=64))
     
    #weight=db.Column(db.Float)
    #need a weight unit class for valid weight units stored in db
    #weight_unit_id=db.Column(db.Integer,db.ForeignKey("weight_units.id"))
    #weight=db.relationship("Weight",secondary=product_weight,backref=db.backref("products"))
    
    #price=db.Column(db.Float)
    #need a price unit class for valid price units stored in db
    #price_unit_id=db.Column(db.Integer,db.ForeignKey("price_units.id"))
    #price=db.relationship("Price",secondary=product_price,backref=db.backref("products"))


    price=db.Column(db.Float)
    weight=db.Column(db.Float)
    priceUnit=db.Column(db.String(length=32))
    weightUnit=db.Column(db.String(length=32))

    case_count=db.Column(db.Integer)
    #if i want date times i can code that later

    comment=db.Column(db.String(length=255))

    upc=db.Column(db.String(length=32))
    home_code=db.Column(db.String(length=15))	   
    #these will be paths to the image on the filesystem
    #stored under products_images
    
    upc_image=db.Column(db.String(length=255))
    product_image=db.Column(db.String(length=255))
    def __repr__(self):
        return """Product(
            name="{}",
            vendor_id=#unused,
            vendors={},
            manufacturer_id=#unused,
            manufacturers={},
            brand_id=#unused,
            brands={},
            department_id=#unused,
            departments={},
            id={},
            price={},
            weight={},
            case_count={},
            comment="{}",
            upc="{}",
            home_code="{}",
            upc_image="{}",
            product_image="{}"            
            )
        """.format(
                self.name,
                #self.vendor_id,
                self.vendors,
                #self.manufacturer_id,
                self.manufacturers,
                #self.brand_id,
                self.brands,
                #self.department_id,
                self.departments,
                self.id,
                self.price,
                self.weight,
                self.case_count,
                self.comment,
                self.upc,
                self.home_code,
                self.upc_image,
                self.product_image
                )
    def defaultdict():
        return dict(
                name=self.name,
                #vendor_id=self.vendor_id,
                vendors=self.vendors,
                #manufacturer_id=self.manufacturer_id,
                manufacturers=self.manufacturers,
                #brand_id=self.brand_id,
                brands=self.brands,
                #department_id=self.department_id,
                departments=self.departments,
                id=self.id,
                price=self.price,
                weight=self.weight,
                comment=self.comment,
                upc=self.upc,
                home_code=self.home_code,
                upc_image=self.upc_image,
                product_image=self.product_image
                )

class ProductSchema(ma.SQLAlchemySchema):
    class Meta:
        model=Product
    #vendor_id=ma.auto_field()
    vendors=ma.List(ma.Nested(VendorSchema))
    id=ma.auto_field()
    #manufacturer_id=ma.auto_field()
    manufacturers=ma.List(ma.Nested(ManufacturerSchema))
    #brand_id=ma.auto_field()
    brands=ma.List(ma.Nested(BrandSchema))
    #department_id=ma.auto_field()
    departments=ma.List(ma.Nested(DepartmentSchema))
    price=ma.auto_field()
    weight=ma.auto_field()
    comment=ma.auto_field()
    name=ma.auto_field()
    upc=ma.auto_field()
    home_code=ma.auto_field()
    upc_image=ma.auto_field()
    product_image=ma.auto_field()
