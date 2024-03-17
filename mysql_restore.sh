#!/bin/bash

#set date
date=$(date +%Y-%m-%d)

# Set the MySQL connection details
DB_HOST="$1"
DB_PORT="$2"
DB_USER="$3"
DB_PASS="$4"
DB_NAME="$5"
BASE_PATH="/home/moba"

backup_name="mysql-$date".tar.gz.enc
download_ip="$6"
download_user="$7"
download_pass="$8"
download_path="$9"

# install sshpass
if [ -f /etc/redhat-release ]; then
  if command -v yum &> /dev/null; then
    yum install -y sshpass
  else
    echo "Yum package manager not found."
  fi
elif [ -f /etc/debian_version ]; then
  if command -v apt &> /dev/null; then
    apt install -y sshpass
  else
    echo "Apt package manager not found."
  fi
else
  echo "Unsupported distribution."
fi

#download backup file
sshpass -p "$download_pass"  scp "$download_user@$download_ip:$download_path/$backup_name" . 

openssl enc -d -aes-256-cbc -in "mysql-$date.tar.gz.enc" -out "mysql-$date.tar.gz" -kfile /data/mysqldump-key.priv.pem

tar -xzvf "mysql-$date".tar.gz

# Loop through the files in the directory
for file in $BASE_PATH/pishvaz/*; do
  if [[ $file =~ ^.*-([0-9]{4}-[0-9]{2}-[0-9]{2})\.sql$ ]]; then
    table_name=$(basename $file | awk -F'-' '{print $1}')
    date=${BASH_REMATCH[1]}
#    echo "$table_name"
    mysql -u$DB_USER -p$DB_PASS $DB_NAME  < $file
#    echo "mysql -u$DB_USER -p$DB_PASS $DB_NAME --table $table_name < $file"
    echo "Restored $file to $table_name table"
  else
    echo "Skipping file $file, invalid format"
  fi
done

#./restore.sh hostaddress_of_mysql mysql_port mysql_user mysql_password project_name download_ip download_user download_pass download_path
