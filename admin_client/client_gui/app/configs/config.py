import enum
import os
from .. import getLocalizedPath
class config(enum.Enum):
    package=os.path.join(getLocalizedPath()[1],"configs")
    states=os.path.join(package,"states.json")
    priceUnit=os.path.join(package,"priceUnit.json")
    weightUnit=os.path.join(package,"weightUnit.json")
