#!/usr/bin/env python3
from argparse import ArgumentParser, FileType
import sys
import subprocess


OPTION_EXIT = 0
CSV_DELIMITER = ";"
SSH_CMD = "/usr/bin/ssh"

hosts = {}


class Host:
    def __init__(self, row_split):
        self.name = row_split[0]
        self.ip = row_split[1]
        self.port = row_split[2]
        self.user = row_split[3]
        self.key_path = row_split[4] if len(row_split) > 4 else None
        self.args = row_split[5] if len(row_split) > 5 else None

    def __str__(self):
        return f"{self.name} ({self.user} on {self.ip})"

    def is_key_set(self):
        return self.key_path is not None

    def is_args_set(self):
        return self.args is not None


def parse_arguments():
    parser = ArgumentParser()
    parser.add_argument("-l", "--list", dest="list", type=FileType("r"), required=True)

    return parser.parse_args()


def read_hosts(file):
    lines = file.readlines()
    host_lines = lines[1:]
    host_count = 0
    for host_line in host_lines:
        host_count += 1
        host_line_split = host_line.split(CSV_DELIMITER)
        host_line_split = [h.strip() for h in host_line_split]
        hosts[host_count] = Host(host_line_split)

    return hosts


def print_hosts():
    for key, host in hosts.items():
        print(f"{key}. {host}")


def clear_screen():
    subprocess.call("clear", shell=True)


def print_host_selection():
    print("############### SSH HOSTS ###############")
    print("")
    print_hosts()
    print("")
    print("0. exit")


def input_is_valid(user_input):
    return user_input in hosts or user_input == OPTION_EXIT


def get_input():
    user_input = int(input("Connect to: "))
    return user_input


def create_command_str(host):
    cmd = SSH_CMD
    cmd += f" -p {host.port}"
    cmd += f" {host.args}" if host.is_args_set() else ""
    cmd += f" -i {host.key_path}" if host.is_key_set() else ""
    cmd += f" {host.user}@{host.ip}"

    return cmd


def connect_to_host(host):
    cmd = create_command_str(host)
    exit_code = subprocess.call(cmd, shell=True)

    return exit_code


def main():
    arguments = parse_arguments()
    read_hosts(arguments.list)

    host_key = -1
    try:
        while host_key != OPTION_EXIT:
            try:
                print_host_selection()
                host_key = get_input()

                if host_key == OPTION_EXIT:
                    continue

                exit_code = connect_to_host(hosts[host_key])
                if exit_code == "0":
                    clear_screen()
            except KeyError:
                print("Invalid choice!")
                continue
    except Exception as e:
        print(f"Something went wrong: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
