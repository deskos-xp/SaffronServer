from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.enums import TA_JUSTIFY
from reportlab.platypus import SimpleDocTemplate,Paragraph,Spacer,Image
from reportlab.lib.styles import getSampleStyleSheet,ParagraphStyle
from reportlab.lib.units import inch
from datetime import datetime

from .can import NumberedCanvas

class gen:
    fname="default.pdf"
    doctime:datetime=datetime.now()
    width,height=letter
    styles=getSampleStyleSheet()
    story=[]
    doc=None

    def __init__(self,entry:tuple,name:str,fname:str):
        self.doc=SimpleDocTemplate(fname,pagesize=letter,
            rightMargin=72,leftMargin=72,
            topMargin=72,bottomMargin=32)
        self.fname=fname
        #self.styles.add(ParagraphStyle(name="Justify",alignment=TA_JUSTIFY))

        new=ParagraphStyle(**self.styles['Title'].__dict__)
        new.fontSize=13
        new.name="TitleSub"
        new.fontName="Helvetica-Oblique"
        self.styles.add(new)
        #self.styles.add(
        
        self.story.append(Paragraph(name,self.styles['Title']))
        self.story.append(Paragraph(datetime.ctime(self.doctime),self.styles['TitleSub']))
        #print(self.styles.list())
        for line in entry:
            x=Paragraph(line,self.styles['Normal'])
            self.story.append(x)
            self.story.append(Spacer(1,12))
        self.doc.title=name
        self.doc.build(self.story,canvasmaker=NumberedCanvas)
        





if __name__ == "__main__":
    docTest=("this is a test","this is a test2",)*2000
    gen(docTest,"testDoc",fname="xmas.pdf")
