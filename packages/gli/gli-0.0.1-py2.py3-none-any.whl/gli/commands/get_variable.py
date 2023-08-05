"""Gitlab CLI get_project Command"""


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
class Get_variable(Base):

    def run(self):

        project = self.utils.get_project_name(self.utils.project_name)

        if self.options["--list"]:
            variables = self.utils.gl.project_variables.list(project_id=project.id)
            for variable in variables:
                #don't print value of var ==> use --key for that
                #print(variable.key+"="+variable.value)
                print(variable.key)


        if self.utils.key:
            variables = self.utils.gl.project_variables.get(self.utils.key, project_id=project.id)
            print(variables.value)

