#!/bin/bash

# Get the current date
date=$(date +%Y-%m-%d)

# MySQL connection details
host=$1
port=$2
user=$3
password=$4
project=$5

mkdir -p db_backups/$project
cd db_backups/$project

# Get list of databases
databases=$(mysql -h "$host" -P "$port" -u "$user" -p"$password" -e "SHOW DATABASES;" | grep -Ev "(Database|information_schema|performance_schema|mysql)")

# Loop through each database
for db in $databases; do
    # Create a directory for the database if it doesn't exist
    echo "directory of $db was created"
    if [[ "$db" == "pishvaz" ]]
    then
        mkdir -p "$db"
        # Get list of tables in the database
        tables=$(mysql -h "$host" -P "$port" -u "$user" -p"$password" -e "USE $db; SHOW TABLES;" | grep -v "Tables_in_")
        echo "this is tables of $db database: $tables"
        # Loop through each table
        for table in $tables; do
                echo "echo start dumping of $db database/$tables"
                # Dump the table data to a separate SQL file
                mysqldump -h "$host" -P "$port" -u "$user" -p"$password" "$db" "$table" > "$db/$table-$date.sql"
                echo "echo finish dumping of $db database/$tables"
        done 
    else
        mysqldump -h "$host" -P "$port" -u "$user" -p"$password" "$db" > "$db-$date.sql"
        echo "echo finish dumping of $db database/$tables"
    fi
done
tar -cvzf "mysql-$date".tar.gz *.sql pishvaz 
openssl enc -aes-256-cbc -salt -in "mysql-$date".tar.gz -out "mysql-$date.tar.gz.enc" -kfile /data/mysqldump-key.priv.pem
for i in *.tar.gz.enc; do sshpass -p 'BACKUPSERVER_PASSWORD' scp  $i  BACKUPSERVER_USER@BACKUPSERVER_IP:PATH ;done

# delete directory of backups in server
rm -rf /root/db_backups/
echo "Good Luck :)"
# ./myscript.sh hostaddress_of_mysql mysql_port mysql_user mysql_password project_name
