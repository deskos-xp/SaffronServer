from .. import db,auth,ma
from .product import Product,ProductSchema
from .as_dict import AsDict

productCount_products=db.Table("productCount_product",
            db.Column("product_id",db.Integer,db.ForeignKey("products.id")),
            db.Column("productCount_id",db.Integer,db.ForeignKey("productCount.id"))
                    )

class ProductCount(db.Model,AsDict):
    __tablename__="productCount"
    id=db.Column(db.Integer,primary_key=True)
    products=db.relationship('Product',secondary=productCount_products,backref=db.backref("productCount"))
    units=db.Column(db.Integer)
    cases=db.Column(db.Integer)

    def __repr__(self):
        return '''
        ProductCount(
            id={},
            products={},
            units={},
            cases={}
            )
            '''.format(self.id,self.products,self.units,self.cases)

class ProductCountSchema(ma.SQLAlchemySchema):
    class Meta:
        model=ProductCount
    id=ma.auto_field()
    products=ma.List(ma.Nested(ProductSchema))
    cases=ma.auto_field()
    units=ma.auto_field()
