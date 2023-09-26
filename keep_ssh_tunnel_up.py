import sys
import psutil
import socket
import subprocess
from datetime import datetime


def establish_tunnel(dest_port, ssh_ip, ssh_user, ssh_port):
    subprocess.Popen(
        f'ssh -D {dest_port} -N -f -p {ssh_port} {ssh_user}@{ssh_ip}', shell=True
    )


def get_tcp_connections():
    local_connections = psutil.net_connections('inet')
    tcp_connections = []
    for connection in local_connections:
        ip, port = connection.laddr
        if ip in ('0.0.0.0', '127.0.0.1', '::'):
            if connection.type == socket.SOCK_STREAM and connection.status == psutil.CONN_LISTEN:
                protocol = 'tcp'
            else:
                continue

            tcp_connections.append(f'{port}/{protocol}')

    return tcp_connections


def main(dest_port, ssh_ip, ssh_user, ssh_port):
    tcp_connections = get_tcp_connections()
    tunnel_exists = f'{dest_port}/tcp' in tcp_connections
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    if not tunnel_exists:
        establish_tunnel(dest_port, ssh_ip, ssh_user, ssh_port)
        print(f'{current_time} - {dest_port} - {ssh_ip} - {ssh_user} - {ssh_port} - new tunnel established')


if __name__ == '__main__':
    args = sys.argv[1:]
    if len(args) < 4:
        raise Exception('Incomplete arguments - must pass: dest_port, ssh_ip, ssh_user, ssh_port')

    main(*args)


# usage: /var/www/keep_tunnel_up/venv/bin/python /var/www/keep_tunnel_up/ssh_tunnel_watcher.py <socks5_port> <ip_ssh> <ssh_user> <sshport> >> /var/log/ssh_tunnel_watcher.log