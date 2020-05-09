curl -u admin:avalon -X POST -d @shell/new_vendor.json localhost:5000/vendor/new
curl -uadmin:avalon -X GET localhost:5000/vendor/get/id/1
curl -uadmin:avalon -X POST -d @shell/update_vendor.json localhost:5000/vendor/update/id/1
curl -u admin:avalon -X POST -d @shell/get_vendor.json localhost:5000/vendor/get
curl -u admin:avalon -X GET localhost:5000/vendor/update/1/add/address/1
curl -u admin:avalon -X GET localhost:5000/vendor/update/1/remove/address/1
