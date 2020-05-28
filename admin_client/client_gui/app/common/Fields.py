import re,enum

def regexThisShit2(text):
    try:
        p=re.search("(?P<ID>\d*):(?P<TYPE>\w*)",text)
        return dict(ID=p.group("ID"),TYPE=p.group("TYPE"))
    except Exception as e:
        print(e)

def regexThisShit(text):
    try:
        p=re.compile('^\d*:\w*')
        result=p.match(text)
        s2=result.group()

        p=re.compile('^\d*:')
        ID=p.match(s2)
        ID=int(ID.group()[:-1])

        p=re.compile(':[\w]*')
        TYPE=p.search(s2).group()
        TYPE=TYPE[1:]
        return dict(ID=ID,TYPE=TYPE)
    except Exception as e:
        print(e)

def stripStructures(data):
    tmp={}
    for i in data.keys():
        if type(data[i]) in [type(int()),type(bool()),type(float()),type(str())]:
            tmp[i]=data[i]
    return tmp


def preRegex(text):
    ID=text.split(" - ")[0]
    TYPE=ID.split(":")[1]
    ID=ID.split(":")[0]
    return dict(ID=ID,TYPE=TYPE)


def toAddressString(data:dict):
    #"{'ZIP': '', 'apartment_suite': '', 'city': '', 'id': 6, 'state': '', 'street_name': '', 'street_number': '', 'name': ' , ,  '"
    return "{id}:address - {street_number} {street_name}, {city}, {state} {ZIP} ({apartment_suite})".format(**data)


def fields(name):
    def addressFields():
        return dict(
                city="",
                state="",
                street_number="",
                street_name="",
                ZIP="",
                apartment_suite=""
                )
    def genericFields():
        return dict(
            comment="",
            name="",
            email="",
            phone=""
                )
    def departmentFields():
        return dict(
            comment="",
            name="",
            store_department_number=0
                )
    def productFields():
        return dict(
                comment="",
                upc="",
                homecode="",
                priceUnit="",
                weightUnit=""
                )


    if name == 'address':
        return addressFields()
    elif name in ['vendor','manufacturer','brand']:
        return genericFields()
    elif name == 'department':
        return departmentFields()
    elif name == 'product':
        return productFields()
    else:
        return dict()

class Mode(enum.Enum):
    POST=enum.auto()
    GET=enum.auto()
