from .. import db,auth,ma
from .as_dict import AsDict

class Address(db.Model,AsDict):
    __tablename__="address"
    id=db.Column(db.Integer,primary_key=True)
    street_name=db.Column(db.String(length=128))
    street_number=db.Column(db.String(length=128))
    apartment_suite=db.Column(db.String(length=64))
    city=db.Column(db.String(length=64))
    state=db.Column(db.String(length=2))
    ZIP=db.Column(db.String(length=20))
    
    def __repr__(self):
        return '''Address(
            id={},
            street_name="{}",
            street_number="{}",
            apartment_suite="{}",
            city="{}",
            state="{}",
            ZIP="{}"
        )'''.format(
                self.id,
                self.street_name,
                self.street_number,
                self.apartment_suite,
                self.city,
                self.state,
                self.ZIP
                )

    def defaultdict(self):
        return dict(
                id=int(),
                street_name=str(),
                street_number=str(),
                apartment_suite=str(),
                city=str(),
                state=str(),
                ZIP=str()
                )

        serial=AddressSchema()

class AddressSchema(ma.SQLAlchemySchema):
    class Meta:
        model=Address
    id=ma.auto_field()
    street_name=ma.auto_field()
    street_number=ma.auto_field()
    apartment_suite=ma.auto_field()
    city=ma.auto_field()
    state=ma.auto_field()
    ZIP=ma.auto_field()

