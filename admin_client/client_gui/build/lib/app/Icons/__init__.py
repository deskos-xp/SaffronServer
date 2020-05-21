from io import BytesIO
import os
x=__import__(__name__.split(".")[0])

def getProgram_image(name) -> BytesIO:
    path=x.getLocalizedPath()[1]
    buff=BytesIO()
    with open(os.path.join(path,name),"rb") as fd:
        while True:
            d=fd.read(1024)
            if not d:
                break
            buff.write(d)
    buff.seek(0)
    return buff
