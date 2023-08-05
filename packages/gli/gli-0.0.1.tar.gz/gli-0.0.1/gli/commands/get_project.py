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
class Get_project(Base):

    def run(self):

        if self.utils.project_name:
            project = self.utils.get_project_name(self.utils.project_name)
            print (project.pretty_print())
