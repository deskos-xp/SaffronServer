
sudo pacman -S nginx

function config_cp(){
	if ! test -e "/etc/nginx/conf.d" ; then
		mkdir -v /etc/nginx/conf.d
	fi
	cp -v etc/nginx/conf.d/saffron_server.conf /etc/nginx/conf.d/
	cp -v etc/nginx/nginx.conf /etc/nginx/
	cp -v etc/systemd/system/saffron_server.service /etc/systemd/system/
	if ! test -e "/etc/uwsgi" ; then
		mkdir -v "/etc/uwsgi"
	fi
	cp -v etc/uwsgi/saffron_server.ini /etc/uwsgi/

}

cp -r src /srv/SaffronServerFlask
config_cp
python -m venv /srv/SaffronServerFlask/venv
source /srv/SaffronServerFlask/venv/bin/activate
pip install -r /srv/SaffronServerFlask/depends.txt

chown -R http:http /srv/SaffronServerFlask
chmod -R 777 /srv/SaffronServerFlask

systemctl start nginx
systemctl start saffron_server
systemctl enable nginx
systemctl enable saffron_server

