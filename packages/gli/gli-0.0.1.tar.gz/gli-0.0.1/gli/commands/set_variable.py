"""Gitlab CLI set_variable Command"""


from json import dumps
from .base import Base

import gitlab

from .. import utils


#une classe dois toujours commencer par une majuscule!!!
class Set_variable(Base):

    def run(self):

        project = self.utils.get_project_name(self.utils.project_name)


        try:
            variable = self.utils.gl.project_variables.get(self.utils.key, project_id=project.id)

            self.utils.debug("blue", "<--variable "+self.utils.key+" = "+variable.value)
            variable.value = self.utils.value
            variable.save()
            self.utils.debug("blue", "-->variable "+self.utils.key+" = "+variable.value)
            
        except gitlab.exceptions.GitlabGetError,e:

            #import ipdb; ipdb.set_trace()
            if e.message == "404 Variable Not Found":
                self.utils.debug("blue", "Create new variable "+self.utils.key+" = "+self.utils.value)
                variable = self.utils.gl.project_variables.create({'key': self.utils.key,
                                                                   'value': self.utils.value},
                                                                  project_id=project.id)
            
            #Check the save works correctly
            variable = self.utils.gl.project_variables.get(self.utils.key, project_id=project.id)
            if variable.value == self.utils.value:
                print("gitlab project("+self.utils.project_name+") variable "+self.utils.key+"="+self.utils.value+" has been successfully updated")
                
