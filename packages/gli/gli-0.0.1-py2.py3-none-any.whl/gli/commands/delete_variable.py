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
class Delete_variable(Base):

    def run(self):

        
        project = self.utils.get_project_name(self.utils.project_name)



        if self.utils.key:
            variable = self.utils.gl.project_variables.get(self.utils.key, project_id=project.id)

            print "Confirm that you want to delete variable "+variable.key+" from project "+self.utils.project_name+" ? y/(n)"
            res = raw_input()
            if res.lower() == "y" or res.lower() == "yes":
                variable.delete()
                print "deleted"

