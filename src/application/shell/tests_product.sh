
curl -uadmin:avalon localhost:5000/product/new -X POST -d@shell/new_product.json

curl -uadmin:avalon -F 'file=@/home/carl/Pictures/tattoo.png' localhost:5000/product/update/1/upload/upc_image
curl -uadmin:avalon -F 'file=@/home/carl/Pictures/tattoo.png' localhost:5000/product/update/1/upload/product_image
curl -uadmin:avalon -X get localhost:5000/product/get/1/upc_image > product_image.png
curl -uadmin:avalon -X get localhost:5000/product/get/1/product_image > product_image.png



curl -uadmin:avalon localhost:5000/product/update/2/add/manufacturer/1
#curl -uadmin:avalon localhost:5000/product/update/2/remove/manufacturer/1

curl -uadmin:avalon localhost:5000/product/update/2/add/brand/1
#curl -uadmin:avalon localhost:5000/product/update/2/remove/brand/1

curl -uadmin:avalon localhost:5000/product/update/2/add/department/1
#curl -uadmin:avalon localhost:5000/product/update/2/remove/department/1

curl -uadmin:avalon localhost:5000/product/update/2/add/vendor/1
#curl -uadmin:avalon localhost:5000/product/update/2/remove/vendor/1


curl -uadmin:avalon localhost:5000/product/get -X POST -d {}
curl -uadmin:avalon localhost:5000/product/get -X POST -d @shell/get_products.json

curl -uadmin:avalon localhost:5000/product/get/2
curl -uadmin:avalon localhost:5000/product/delete/2
