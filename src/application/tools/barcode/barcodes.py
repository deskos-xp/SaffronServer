import treepoem,sys,os
from io import BytesIO

class barcode_gen:
    buff:BytesIO=None
    def __init__(self,**kwargs):
        upc=kwargs.get("upc")
        TYPE=kwargs.get("Type")
        img=treepoem.generate_barcode(barcode_type=TYPE,data=upc);
        img=img.convert("RGB")
        
        self.buff=BytesIO()
        with BytesIO() as o:
            img.save(o,format="jpeg")
            self.buff.write(o.getvalue())
        self.buff.seek(0) 
