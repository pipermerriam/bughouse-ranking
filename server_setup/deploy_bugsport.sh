#!/bin/bash

# go to git dir
cd /var/git

# remove old repo
/bin/rm -rf /var/git/bughouse-ranking && echo "#----------> removed old repo dir"

# clone with depth 1
/usr/bin/git clone https://github.com/simpleenergy/bughouse-ranking.git --depth=1 && echo "#----------> cloned repo into /var/git"

# rsync into place
/usr/bin/rsync -avq /var/git/bughouse-ranking/bughouse /var/www/bughouse && echo "rsynced into /var/www"
/usr/bin/rsync -avq /var/git/bughouse-ranking/manage.py /var/www/bughouse && echo "rsynced manage.py"

# re-link env file
#/bin/ln -sfn /root/uwsgi_environment.env /var/www/bughouse/uwsgi_environment.env && echo "#----------> relinked env file"
/bin/cp /root/uwsgi_environment.env /var/www/bughouse/.env && echo "#----------> replaced .env file"

# ensure dirs exist
/bin/mkdir -p /var/www/bughouse/public/static && echo "#----------> ensured static dir"
/bin/mkdir -p /var/www/bughouse/public/media && echo "#----------> ensured media dir"

# go back where you were
cd -

# Collect me some static stuff
cd /var/www/bughouse
/var/www/bughouse/env/bin/python manage.py collectstatic --noinput && echo "Collected some static stuff"

# Chown all the things
/bin/chown -R root:www-data /var/www && echo "#----------> chowining stuff root:www-data"
#/bin/chown -R www-data:www-data /var/www && echo "#----------> chowining stuff root:www-data"

# restart stuff
/usr/sbin/service nginx restart && echo "#----------> restarted nginx"
/usr/sbin/service uwsgi restart && echo "#----------> restarted uwsgi"

# show all is good
/usr/sbin/service nginx status

echo "#----------> Grabbing top of HTML to make sure it's up"
/usr/bin/wget -O - http://bgsprt.com | head

cd -
