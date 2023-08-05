#!/usr/bin/env python
import os
import json
from terminaltables import AsciiTable

VERSION="0.2.6"

class I:

    def __init__(self, file = None):
        if not file:
            self.file = os.path.expanduser("~") + "/.i"
        else:
            self.file = file

        self._create_file()

        self.servers = self.get_server_list()

    def _create_file(self):
        if not os.path.isfile(self.file):
            open(self.file, "w+")
            return True
        return False

    def get_server_list(self):
        try:
            with open(self.file, "r") as file:
                data = json.load(file)
            return data
        except ValueError:
            return []

    def store_server_list(self):
        with open(self.file, "w") as file:
            json.dump(self.servers, file, indent = 2)
        return True

    def server_table(self):
        table_data = [
            ["Name", "Address", "Location"]
        ]
        for server in self.servers:
            row = [
                server['name'],
                server['username'] + "@" + server['ip'],
            ]
            if server['location']:
                row.append(server['location'])
            else:
                row.append("")
            table_data.append(row)
        return AsciiTable(table_data)

    def find(self, find):
        for server in self.servers:
            if find in server['name']:
                table_data = [["Name", "Address", "Location"]]
                row = [
                    server["name"],
                    server["username"] + "@" + server['ip']
                ]
                if server['location']:
                    row.append(server['location'])
                table_data.append(row)
                return AsciiTable(table_data)
        return AsciiTable([["Name", "Address", "Location"]])


    def connect(self, server_name): # pragma: no cover
        for server in self.servers:
            if server['name'] == server_name:
                # os.system('cls' if os.name == 'nt' else 'clear')
                os.system("ssh %s" % server['username'] + "@" + server['ip'])


    def validate(self, server):
        for key, value in server.iteritems():
            if not value and not key == "location":
                return False
        return True

    def ask_for_server_info(self): # pragma: no cover
        server = {}
        server['name'] = raw_input("Name: ")
        server['username'] = raw_input("Login username: ")
        server['ip'] = raw_input("IP: ")
        server['location'] = raw_input("Location (optional): ")

        # Validate server info
        if self.validate(server):
            return server
        else:
            return False


    def add(self, server):
        if not self.validate(server):
            return False
        self.servers.append(server)
        self.store_server_list()
        return True

    def remove(self, server_name):
        for server in self.servers:
            if server['name'] == server_name:
                self.servers.remove(server)
        self.store_server_list()
        return True
