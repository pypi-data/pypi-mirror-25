"""Gitlab CLI get_environment Command"""


from json import dumps
from .base import Base

import gitlab

import os
import sys

import requests

import yaml
from datetime import date, time, datetime, timedelta

from pprint import pprint
import logging
import re
from subprocess import Popen, PIPE
import click

from .. import utils


#une classe dois toujours commencer par une majuscule!!!
class Get_environment(Base):

    def run(self):

        
        project = self.utils.get_project_name(self.utils.project_name)
        environments = project.environments.list()

        if self.options["--list"]:        
            for env in environments:
                print "list: name=" + env.name + " id=" + str(env.id) + " url=" + str(env.external_url)

        if self.utils.key:
            for env in environments:
                if env.name == self.utils.key:
                    environment = project.environments.get(env.id)
                    print "You selected environment : name=" + environment.name + " " + str(environment.id) + " " + environment.external_url

