# Install a kick ass bughouse ELO server

Install on base Ubuntu 14.04

apt-get install packages from ./install_me/apt-get.install

pip install packages from ./install_me/pip.install

npm install packages from ./install_me/npm.install

cp ./etc_nginx_sites_available/bugsport to /etc/nginx/sites_available/bugsport

ln -s /etc/nginx/sites_available/bugsport /etc/nginx/sites_enabled/bugsport

cp ./etc_uwsgi_apps_available/bughouse.ini to /etc/uwsgi/apps_available/bughouse.ini

ln -s /etc/uwsgi/apps_available/bughouse.ini /etc/uwsgi/apps_enabled/bughouse.ini

# not including this in the repo, since it contains passwords n stuff
# place uwsgi_environment.env in roots home dir
place deploy_bugsport.sh in roots home dir and chmod +x on it

