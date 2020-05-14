import enum,json,os
import os
from colored import fg,bg,attr

class drmEnum(enum.Enum):
    LOCKED=enum.auto()
    UNLOCKED=enum.auto()
    
class drmMeta:
    config='eula.json'
    path = os.path.abspath(__file__)
    dir_path = os.path.dirname(path)
    email="k.j.hirner.wisdom@gmail.com"
    name="SaffronExplorer"

class drm(drmMeta):
    eula:dict=None
    def __init__(self):
        super(drm,self).__init__()
        self.loadEULA()
        self.state=self.checkEULA()
        if self.state == drmEnum.LOCKED:
            self.printEULA()

    def printEULA(self):
        string=""
        with open(os.path.join(self.dir_path,self.eula.get('eula-file')),'r') as fd:
            while True:
                line=fd.readline()
                if not line:
                    break
                string+='{fg}{line}{fg}'.format(**dict(line=line,fg=fg(2)))
                
        string=string.replace(self.email,"{attr}{bg}{fg}{email}{fg}{bg}{reset}{bg1}".format(**dict(fg=fg(0),email=self.email,bg=bg(1),bg1=bg(0),attr=attr(5),reset=attr(25))))
        string=string.replace(self.name,"{attr}{bg}{fg}{name}{fg}{bg}{reset}{bg1}".format(**dict(reset=attr(25),attr=attr(5),fg=fg(0),name=self.name,bg=bg(1),bg1=bg(0))))
        print(string)
        print("{blink}{fg}You{fg1}{blink_reset} need to Sign the {bold}EULA{bold_reset} in {underline}{config}{underline_reset}".format(
            **dict(
                fg=fg(1),
                fg1=fg(2),
                blink=attr(5),
                blink_reset=attr(25),
                config=self.config,
                underline=attr(4),
                underline_reset=attr(24),
                bold=attr(1),
                bold_reset=attr(21),
            )))

    def loadEULA(self):
        with open(os.path.join(self.dir_path,self.config),'r') as fd:
            self.eula=json.load(fd)
    

    def checkEULA(self):
        if self.eula != None:
            if 'agrees' in self.eula.keys() and 'eula-file' in self.eula.keys():
                if os.path.exists(os.path.join(self.dir_path,self.eula.get('eula-file'))) and os.stat(os.path.join(self.dir_path,self.eula.get('eula-file'))).st_size > 0:
                    if self.eula.get('agrees') != None:
                        if self.eula.get('agrees') == True:
                            return drmEnum.UNLOCKED
        return drmEnum.LOCKED

    


