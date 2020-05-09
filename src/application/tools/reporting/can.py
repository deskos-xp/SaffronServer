from reportlab.pdfgen import canvas
from reportlab.platypus import SimpleDocTemplate
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter
class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        canvas.Canvas.__init__(self, *args, **kwargs)
        self._codes = []
    def showPage(self):
        self._codes.append({'code': self._code, 'stack': self._codeStack})
        self._startPage()
    def save(self):
        """add page info to each page (page x of y)"""
        # reset page counter 
        self._pageNumber = 0
        width,height = letter 
        for code in self._codes:
            # recall saved page
            self._code = code['code']
            self._codeStack = code['stack']
            self.setFont("Helvetica", 7)
            self.drawRightString(width/2, height/30,
                "page %(this)i of %(total)i" % {
                   'this': self._pageNumber+1,
                   'total': len(self._codes),
                }
            )
            canvas.Canvas.showPage(self)
        self._doc.SaveToFile(self._filename, self)

