# Copyright 2023 Elijah Gordon (NitrixXero) <nitrixxero@gmail.com>

# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.

from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter
from paramiko import SSHClient, AutoAddPolicy, AuthenticationException, SSHException


def execute_ssh_command(hostname, port, username, password, command):
    ssh_client = SSHClient()

    ssh_client.set_missing_host_key_policy(AutoAddPolicy())

    try:
        ssh_client.connect(hostname, port=port, username=username, password=password)
        stdin, stdout, stderr = ssh_client.exec_command(command)
        output = stdout.read().decode('utf-8')

        print("[*] Connecting to: '({})'".format(hostname))
        print("[*] On Port: '({})'".format(port))
        print("[*] Username: '({})' Password: '({})'".format(username, password))
        print("--------------------------------------------------------------------")

        print("[*] Output of command '({})' on ({}): \n\n{}".format(command, hostname, output))

    except AuthenticationException:
        print("[!] Authentication failed. Please check your username and password.")
    except SSHException as e:
        print("[!] Unable to establish SSH connection:", str(e))
    finally:
        ssh_client.close()

        print("--------------------------------------------------------------------")
        print("[*] Connection to: '({})' closed".format(hostname))
        print("--------------------------------------------------------------------")

if __name__ == "__main__":
    parser = ArgumentParser(description="SSH client script with Paramiko", formatter_class=ArgumentDefaultsHelpFormatter)
    parser.add_argument("hostname", help="SSH server hostname")
    parser.add_argument("-u", "--username", required=True, help="SSH username")
    parser.add_argument("-p", "--password", required=True, help="SSH password")
    parser.add_argument("-P", "--port", type=int, default=22, help="SSH server port")
    parser.add_argument("command", help="Command to execute on the SSH server")
    parser.add_argument("-V", "--version", action="version", version="%(prog)s 1.0")

    args = parser.parse_args()

    execute_ssh_command(args.hostname, args.port, args.username, args.password, args.command)
