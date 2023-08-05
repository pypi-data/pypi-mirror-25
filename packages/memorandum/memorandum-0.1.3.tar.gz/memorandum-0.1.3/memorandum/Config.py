###
# Author: Vincent Lucas <vincent.lucas@gmail.com>
###

import getpass
import json
import os.path

###
# Config class to load and create the configuratin.
###
class Config:
    ###
    # Load the configuration file or create it if it does not exists.
    ###
    def __init__(
            self,
            conf_dir = os.path.expanduser("~/.config/memorandum"),
            conf_filename = "memorandum.rc"):

        self.conf = None
        self.conf_dir = conf_dir
        self.conf_filename = conf_filename
        self.conf_path = "{0}/{1}".format(conf_dir, conf_filename)

        # Create the configuration file if it does not exists
        self.create_conf_file()

        # Loads the configuration
        self.load_json()

        # Create alias for module
        self.create_alias()

    ###
    # Create configuration file
    ###
    def create_conf_file(
            self):
        if(not os.path.isfile(self.conf_path)):
            print("Configuration file does not exists.\
                    \n\tCreating : {0}\n".format(self.conf_path))

            if(not os.path.isdir(self.conf_dir)):
                os.makedirs(self.conf_dir, mode=0o700, exist_ok=True)

            # url e.g. : "https://<server.example.com>/SOGo/dav/<login>/Calendar/personal"
            json_data = {
                    "user": input('user: '),
                    "password": getpass.getpass(prompt='password: '),
                    "url": input('url: '),
                    "email": input('email: ')
            }

            with open(self.conf_path, mode='a') as fd:
                json_data_str = json.dumps(json_data, sort_keys=True, indent=4)
                fd.write(json_data_str)

    ###
    # Load json data from the given file.
    #
    # @param filename The filename to read the json data from.
    ###
    def load_json(
            self):
        self.conf = None
        with open(self.conf_path) as fd:
            self.conf = json.load(fd)


    ###
    # Creates an alias for the main command.
    #
    # @param alias_file The alias file used for the current shell.
    ###
    def create_alias(
            self,
            alias_file = os.path.expanduser("~/.bash_aliases")):
        alias_line = "alias memorandum='python3 -m memorandum'"
        found = False

        if(os.path.isfile(alias_file)):
            with open(alias_file, mode='r') as fd:
                for line in fd:
                    if(line == alias_line):
                        found = True

        if(not found):
            user_check = input("Alias memorandum does not exists.\
                    \n\tAdd alias to : {0} ? [y/N]: ".format(alias_file))
            if(user_check == "y"):
                with open(alias_file, mode='a') as fd:
                    fd.write(alias_line)
