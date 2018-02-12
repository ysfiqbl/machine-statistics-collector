"""
This is the file which is executed to run the application.
"""

import py_compile
import xml.etree.ElementTree as ET
from settings import CLIENT_CONFIG_FILE_PATH, CLIENT_SCRIPT_FILE_PATH

from .tasks import collect_statistics


def create_app(config_file_path=CLIENT_CONFIG_FILE_PATH):
    return App(config_file_path)


class App(object):

    def __init__(self, config_file_path):
        self.config_file = config_file_path
        self.compile_stats_script(CLIENT_SCRIPT_FILE_PATH)


    def clients(self):
        """
        Read XML cofig file and create list of machines along with their
        details

        :param file_path: path to the configuratin file
        :return: list of client machines and their details
        """
        tree = ET.parse(self.config_file)
        root = tree.getroot()
        clients = []

        for client in root.findall('client'):
            client.attrib['alerts'] = []
            for node in client.iter():
                if node.tag == 'alert':
                    client.attrib['alerts'].append(node.attrib)

            clients.append(client.attrib)

        return clients


    def compile_stats_script(self, file_path=CLIENT_SCRIPT_FILE_PATH):
        """
        Compile Python file to .py_compile

        :param file_path: path to file that needs to be compiled
        """
        py_compile.compile(file_path)
        return None


if __name__ == '__main__':
    app = create_app()

    for client in app.clients():
        collect_statistics.delay(client)