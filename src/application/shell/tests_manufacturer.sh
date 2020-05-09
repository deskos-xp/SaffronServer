curl -u admin:avalon -X POST -d @shell/new_manufacturer.json localhost:5000/manufacturer/new
curl -uadmin:avalon -X GET localhost:5000/manufacturer/get/id/1
curl -uadmin:avalon -X POST -d @shell/update_manufacturer.json localhost:5000/manufacturer/update/id/1
curl -u admin:avalon -X POST -d @shell/get_manufacturer.json localhost:5000/manufacturer/get
curl -u admin:avalon -X GET localhost:5000/manufacturer/update/1/add/address/1
curl -u admin:avalon -X GET localhost:5000/manufacturer/update/1/remove/address/1
