curl -u admin:avalon localhost:5000/user/update/id/2 -X POST -d @shell/update_user.json
curl -u admin:avalon localhost:5000/user/get -X POST -d '{"active":true,"page":1,"limit":1}'
curl -u admin:avalon localhost:5000/user/get/id/2
curl -u admin:avalon localhost:5000/user/new -d @shell/new_user.json -X POST
curl localhost:5000/admin/new
