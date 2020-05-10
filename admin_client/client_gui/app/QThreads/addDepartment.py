from PyQt5.QtCore import QThread,QCoreApplication
import requests,time

class AddExistingDepartment(QThread):
    auth=None
    parent=None
    w=None
    address=None
    product_id=None

    def run(self):
        app=QCoreApplication.instance()
        self.addDepartment()
    
    def addDepartment(self):
        departments=self.parent.depThread.departments
        while departments == None:
            time.sleep(0.5)
            departments=self.parent.depThread.departments
            print("getting departments : {}".format(departments))
        selected=self.w.department_cb.currentText()
        departmentId=[i['id'] for i in departments if i['name'] == selected]
        if not ((departmentId == []) or (departmentId == None)):
            departmentId=departmentId[0]
            response=requests.get("{}/product/update/{}/add/department/{}".format(self.address,self.product_id,departmentId),auth=self.auth)
