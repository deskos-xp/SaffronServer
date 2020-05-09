curl -i -H "Content-Type: application/json" -uadmin:avalon localhost:5000/address/get -X POST -d @shell/get_address.json
curl -uadmin:avalon localhost:5000/address/update/id/1 -X POST -d @shell/update_address.json
curl -uadmin:avalon localhost:5000/address/get/id/1 -X GET
curl -uadmin:avalon localhost:5000/address/new -X POST -d @shell/new_address.json
