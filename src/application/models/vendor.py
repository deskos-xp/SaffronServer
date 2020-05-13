from .. import db,auth,ma
from .address import Address,AddressSchema
from .as_dict import AsDict

vendor_address=db.Table("vendor_addresses",
        db.Column("vendor_id",db.Integer,db.ForeignKey("vendors.id"),unique=True),
        db.Column("address_id",db.Integer,db.ForeignKey("address.id"))
        )

class Vendor(db.Model,AsDict):
    __tablename__="vendors"
    name=db.Column(db.String(length=128))
    comment=db.Column(db.String(length=255))
    id=db.Column(db.Integer,primary_key=True)
    address=db.relationship('Address',secondary=vendor_address,backref=db.backref("vendors"))

    email=db.Column(db.String(length=64))
    phone=db.Column(db.String(length=11))
   
    def __repr__(self):
        return '''
        Vendor(
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

class VendorSchema(ma.SQLAlchemySchema):
    class Meta:
        model=Vendor
    name=ma.auto_field()
    comment=ma.auto_field()
    id=ma.auto_field()
    address=ma.List(ma.Nested(AddressSchema))
    email=ma.auto_field()
    phone=ma.auto_field()

