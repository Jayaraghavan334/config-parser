import yaml
from yaml import CLoader
import os
import subprocess
import re
import pandas as pd
import random
from Exception import FileNotFoundException

class Yaml_Parser(self,docker_compose_base_path,docker_compose_environ_path:None):

    def __init__(self):
        try:
          self.base_path = docker_compose_base_path
          self.environ_path = docker_compose_environ_path
           
          with open(base_path,"r") as docker_compose_base_config:
            self.base_config = yaml.load(self.base_path, Loader=CLoader)["services"]
          
          if(environ_path is not None):

            with open(environ_path,"r") as docker_compose_environ_config:
            self.environ_config = yaml.load(self.environ_path, Loader=CLoader)["services"]

          else:
            self.environ_config = None
        
          self.splitting_fields = {"volumes":":","environment":"=","ports":":"}

        except:
          print("File not found. Please enter valid file path")
     

    def split_all_fields():
        
        for parameter_value,token in self.spliiting_fields.items():
            self.tokenize(self.base_config, token, parameter_value)

            if(self.environ_config is not None):
               self.tokenize(self.environ_config, token, parameter_value)


    def tokenize(config, token, key_name):
        new_service_config = {}

         for service, service_config in config.items():
            new_service_config={}

            for keys in service_config.keys():
                if(keys == key_name):

                    if(type(service_config[key_name])==list):

                    for val in service_config[key_name]:
                        if(type(val)==str):

                            val_key = val.split(token)[0]

                            val_mapping = val.split(token)[1]

                            new_service_config[val_key] = val_mapping

                    config[service][key_name] = new_service_config
    

