# DevOps Automation Scripts

This repository contains a collection of Bash and Python scripts that automate and simplify various DevOps operations, making them easier and more efficient.

## Scripts

1. **clickhouse-backup**

   - Description: This script creates backups of a ClickHouse database as TSV (Tab-Separated Values) files. It also provides the capability to restore the backups to another ClickHouse instance, effectively creating a slave node.
   - Usage: Detailed instructions and usage examples can be found within the script file.

2. **mysql_backup.sh** and **mysql_restore.sh**

   - Description: These Bash scripts provide a comprehensive solution for backing up MySQL databases. They support both table-by-table and full database backups. The backup files are encrypted using the RSA algorithm for added security. The scripts also include functionality for decrypting and restoring the backups.
   - Usage: Refer to the script files for detailed instructions and usage examples.

3. **alert_commands.py**

   - Description: This Python script monitors specific keywords on a Linux system and sends alerts to a Telegram group when the keywords are detected. It can be customized to suit your specific monitoring needs.
   - Usage: Instructions on configuring and running the script can be found within the script file.

4. **check_ssl_expiry.py**

   - Description: This Python script checks the number of days remaining until a website certificate expires. If the expiration is imminent, it sends an alert to a Telegram group. This helps ensure timely certificate renewal and avoids service disruptions.
   - Usage: Refer to the script file for instructions on running and configuring the script.

5. **check_status.py**

   - Description: This Python script checks the HTTP status code of a specific web page. It can be useful for monitoring the availability and responsiveness of critical web services.
   - Usage: Instructions on running the script and specifying the target web page are provided in the script file.

6. **elk_traffic_check**

   - Description: This script analyzes the total traffic stored in an Elasticsearch database (ELK stack) and sends an alert to a Telegram group if the traffic falls below 50 percent of the expected threshold. This helps identify potential issues or anomalies in the data collection process.
   - Usage: Detailed instructions on configuring and running the script can be found within the script file.

7. **keep_ssh_tunnel_up.py**

   - Description: This script ensures that an SSH tunnel remains active and sends data through the tunnel. It helps maintain secure and reliable communication between systems.
   - Usage: Refer to the script file for instructions on running and customizing the script to suit your specific SSH tunnel setup.

8. **syncthing.py**

   - Description: This Python script facilitates the synchronization of two directories on different servers using the Syncthing protocol. It simplifies the process of keeping files and directories up to date across multiple systems.
   - Usage: Instructions on configuring and running the script are provided within the script file.

## Prerequisites

- Bash
- Python 3.x
- ClickHouse (for `clickhouse-backup`)
- MySQL (for `mysql_backup.sh` and `mysql_restore.sh`)
- Elasticsearch (for `elk_traffic_check`)

Please ensure that the necessary dependencies are installed on your system before using the scripts.

## License

This repository is licensed under the [MIT License](LICENSE). Feel free to modify, distribute, and use the scripts according to the terms of this license.

## Contributions

Contributions to this repository are welcome! If you have any improvements, bug fixes, or new scripts to add, please submit a pull request. Your contributions will be greatly appreciated.

## Disclaimer

These scripts are provided as-is, without any warranty or guarantee of any kind. Use them at your own risk. The authors and contributors of this repository are not responsible for any damages or issues caused by the use of these scripts.