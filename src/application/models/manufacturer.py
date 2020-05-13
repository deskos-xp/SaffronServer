from .. import db,auth,ma
from .address import Address,AddressSchema
from .as_dict import AsDict

manufacturer_address=db.Table("manufacturer_addresses",
        db.Column("manufacturer_id",db.Integer,db.ForeignKey("manufacturers.id"),unique=True),
        db.Column("address_id",db.Integer,db.ForeignKey("address.id"))
        )

class Manufacturer(db.Model,AsDict):
    name=db.Column(db.String(length=128))
    id=db.Column(db.Integer,primary_key=True)
    comment=db.Column(db.String(length=255))
    phone=db.Column(db.String(length=11))
    address=db.relationship("Address",secondary=manufacturer_address,backref=db.backref("manufacturers"))
    email=db.Column(db.String(length=128))

    __tablename__="manufacturers"

    def __repr__(self):
        return 'Manufacturer(name="{0}",id={1},comment="{2}",phone={3},email="{4}",address={5})'.format(self.name,self.id,self.comment,self.phone,self.email,self.address)

    def defaultdict(self):
        return dict(
                name=str(),
                id=int(),
                comment=str(),
                phone=int(),
                address=int(),
                email=str()
                )

class ManufacturerSchema(ma.SQLAlchemySchema):
    class Meta:
        model=Manufacturer
    name=ma.auto_field()
    id=ma.auto_field()
    comment=ma.auto_field()
    phone=ma.auto_field()
    address=ma.List(ma.Nested(AddressSchema))
    email=ma.auto_field()
