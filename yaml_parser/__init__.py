import yaml
from yaml import CLoader
import os
import subprocess
import re
import pandas as pd

class Yaml_Parser:

    def __init__(self, docker_compose_base_path:str, docker_compose_environ_path:None):
        try:
          self.base_path = docker_compose_base_path
          self.environ_path = docker_compose_environ_path
         
          with open(self.base_path,"r") as docker_compose_base_config:
            self.base_config = yaml.load(docker_compose_base_config, Loader=CLoader)["services"]
          
          if(self.environ_path is not None):

            with open(self.environ_path,"r") as docker_compose_environ_config:
              self.environ_config = yaml.load(docker_compose_environ_config, Loader=CLoader)["services"]

          else:
            self.environ_config = None

          self.consolidated_config = self.base_config
          
          self.splitting_fields = {"volumes":":","environment":"=","ports":":"}

          self.split_all_fields()
          
          self.consolidate()


        except Exception as e:
          print(f)
     

    def split_all_fields(self):
        
        for parameter_value,token in self.splitting_fields.items():
            self.tokenize(self.base_config, token, parameter_value)

            if(self.environ_config is not None):
               self.tokenize(self.environ_config, token, parameter_value)


    def tokenize(self,config, token, key_name):
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

    def consolidate(self):

        if(self.environ_config is None):
             pass

        else:
             for service, service_config in self.environ_config.items():
                  for key, value in service_config.items():
                      if(type(value) == dict):
                        for key2, values2 in value.items():
                            try:
                                self.consolidated_config[service][key][key2]=values2
                            except Exception as e:
                                self.consolidated_config[service][key] = value
                                break

                      elif(type(value)==list):
                        try:
                           self.consolidated_config[service][key].extend(value)
                        except:
                           self.consolidated_config[service][key] = value
                      else:
                          self.consolidated_config[service][key]=value
                      
			
