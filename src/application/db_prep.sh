
curl localhost:5000/admin/new
curl -u admin:avalon localhost:5000/department/new -X POST -d@shell/new_department.json
curl -uadmin:avalon localhost:5000/address/new -X POST -d @shell/new_address.json
curl -u admin:avalon localhost:5000/user/new -d @shell/new_user.json -X POST
curl -u admin:avalon localhost:5000/user/update/1/add/department/1 -X GET
curl -uadmin:avalon localhost:5000/user/update/1/add/address/1 -X get



curl -u admin:avalon -X POST -d @shell/new_vendor.json localhost:5000/vendor/new
curl -u admin:avalon -X POST -d @shell/new_manufacturer.json localhost:5000/manufacturer/new
curl -u admin:avalon -X POST -d @shell/new_brand.json localhost:5000/brand/new

curl -uadmin:avalon -X GET localhost:5000/vendor/update/1/add/address/1
curl -uadmin:avalon -X GET localhost:5000/manufacturer/update/1/add/address/1
curl -uadmin:avalon -X GET localhost:5000/brand/update/1/add/address/1

curl -uadmin:avalon localhost:5000/product/new -X POST -d@shell/new_product.json

#create units
#curl -uadmin:avalon -X POST -d @shell/new_weightUnit.json localhost:5000/weightUnit/new
#curl -uadmin:avalon -X POST -d @shell/new_priceUnit.json localhost:5000/priceUnit/new
#create prices/weights values
#curl -uadmin:avalon -X POST -d '{"id":3,"value":1.00}' localhost:5000/price/new
#curl -uadmin:avalon -X POST -d '{"id":3,"value":1.00}' localhost:5000/weight/new

#use get method to get unit by value for its id
#add units to values tables
#curl -uadmin:avalon -X GET localhost:5000/price/update/3/add/1
#curl -uadmin:avalon -X GET localhost:5000/weight/update/3/add/1

#add prices/weights to product
#curl -uadmin:avalon -X GET localhost:5000/product/update/1/add/weight/3
#curl -uadmin:avalon -X GET localhost:5000/product/update/1/add/price/3

#new weight
#update weight/update/<weight_id>/add/<weightUnit_id>

curl -uadmin:avalon localhost:5000/product/update/1/add/manufacturer/1
#curl -uadmin:avalon localhost:5000/product/update/2/remove/manufacturer/1

curl -uadmin:avalon localhost:5000/product/update/1/add/brand/1
#curl -uadmin:avalon localhost:5000/product/update/2/remove/brand/1

curl -uadmin:avalon localhost:5000/product/update/1/add/department/1
#curl -uadmin:avalon localhost:5000/product/update/2/remove/department/1

curl -uadmin:avalon localhost:5000/product/update/1/add/vendor/1
#curl -uadmin:avalon localhost:5000/product/update/2/remove/vendor/1

curl -X POST -d {} -uadmin:avalon localhost:5000/productCount/new
curl -X GET -uadmin:avalon localhost:5000/productCount/update/1/add/product/1
curl -X POST -d '{"units":12,"cases":1}' -uadmin:avalon localhost:5000/productCount/update/1
curl -X POST -d {} -uadmin:avalon localhost:5000/productCount/get

curl -uadmin:avalon -X POST -d {} localhost:5000/ledger/new
curl -uadmin:avalon -X get localhost:5000/ledger/update/1/add/user/1
curl -uadmin:avalon -X get localhost:5000/ledger/update/1/add/productCount/1

