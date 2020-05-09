curl -u carl:avalon localhost:5000/department/get -X POST -d@shell/get_department.json
curl -u carl:avalon localhost:5000/department/new -X POST -d@shell/new_department.json
curl -u carl:avalon localhost:5000/department/get/id/1
curl -u carl:avalon localhost:5000/department/update/id/1 -X POST -d@shell/update_department.json
