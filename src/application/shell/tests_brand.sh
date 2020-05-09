curl -u admin:avalon -X POST -d @shell/new_brand.json localhost:5000/brand/new
curl -uadmin:avalon -X GET localhost:5000/brand/get/id/1
curl -uadmin:avalon -X POST -d @shell/update_brand.json localhost:5000/brand/update/id/1
curl -u admin:avalon -X POST -d @shell/get_brand.json localhost:5000/brand/get
curl -u admin:avalon -X GET localhost:5000/brand/update/1/add/address/1
curl -u admin:avalon -X GET localhost:5000/brand/update/1/remove/address/1
