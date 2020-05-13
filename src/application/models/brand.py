from .. import db,auth,ma
from .address import Address,AddressSchema
from .as_dict import AsDict

brand_address=db.Table("brand_addresses",
        db.Column("brand_id",db.Integer,db.ForeignKey("brands.id"),unique=True),
        db.Column("address_id",db.Integer,db.ForeignKey("address.id"))
        )


class Brand(db.Model,AsDict):
    __tablename__="brands"
    name=db.Column(db.String(length=128))
    comment=db.Column(db.String(length=255))
    id=db.Column(db.Integer,primary_key=True)
    address=db.relationship('Address',secondary=brand_address,backref=db.backref("brands"))

    email=db.Column(db.String(length=64))
    phone=db.Column(db.String(length=11))
   
    def __repr__(self):
        return '''
        Brand(
name="{}",
comment="{}",
id={},
address={},
email="{}",
phone="{}"
)       '''.format(
                self.name,
                self.comment,
                self.id,
                self.address,
                self.email,
                self.phone
            )
    def defaultdict(self):
        return dict(
                name=str(),
                comment=str(),
                id=int(),
                address=str(),
                email=str(),
                phone=str()
        )

class BrandSchema(ma.SQLAlchemySchema):
    class Meta:
        model=Brand
    name=ma.auto_field()
    comment=ma.auto_field()
    id=ma.auto_field()
    address=ma.List(ma.Nested(AddressSchema))
    email=ma.auto_field()
    phone=ma.auto_field()

