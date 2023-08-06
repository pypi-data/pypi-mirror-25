
# Gli (GitLab Client)

Gli is a Gitlab Client based on the [python-gitlab](http://python-gitlab.readthedocs.io/) project.

## Purpose

This Cli allows you to manage some objects of your Gitlab projects:

- Your Gitlab Pipelines Variables (Create, Update, Delete)
- Get details on your projects
- Activate/Deactivate the Gitlab Registry for a project

The python-gitlab comes also with a GitLab Cli : [gitlab](http://python-gitlab.readthedocs.io/en/stable/cli.html) but that don't fullfill the features I was looking for.


Gli uses the same configuration file as for the python-gitlab client : `~/.python-gitlab.cfg`

## Installation

The easiest way is to install from Pypi library

```
pip install gli
```

## Gli Configuration

The configuration uses the `INI` format, and contain new section for each GitLab server you want to interract with:

```ini
[global]
default=gitlab.pic
ssl_verify = False
timeout = 5
api_version = 3

[gitlab.pic]
url = https://<gitlab-pic-url>
private_token = XXXXXX
api_version = 3

[gitlab.forge]
url = https://<gitlab-forge-url>
private_token = YYYYY
api_version = 4

```

you can find more detailed on the [python-gitlab docs](http://python-gitlab.readthedocs.io/en/stable/cli.html#configuration)


## Gli usage

Gli uses a cli based on the  [skele-cli](https://github.com/rdegges/skele-cli) python project.

```
"""
gli - Gitlab Client

Usage:
  gli get_project  --project-name=<project_name> [-d]
  gli get_variable --project-name=<project_name> --key=<variable_name> [--list] [-d]
  gli get_variable --project-name=<project_name> --list [-d]
  gli set_variable --project-name=<project_name> --key=<variable_name> --value=<variable_value> [-d]
  gli delete_variable --project-name=<project_name> --key=<variable_name>
  gli delete_environment --project-name=<project_name> --key=<environment_name>
  gli toggle_registry --project-name=<project_name> [-d]
  gli -h | --help
  gli -v | --version

Options:
  -d                            Debug mode.
  -h --help                     Show this screen.
  --key=key                     Key for object
  --value=value                 Value for object
  -v --version                  Show version.

Commands:
  get_project : get details on a gitlab project
  get_variable: Retrieve list or value for Gitlab variables
  set_variable: Create or Update value for a Gitlab Pipeline variable
  dfelete_variable: Delete a Gitlab Pipeline variable
  toggle_registry: allow to activate or deactivete the GitLab Container Registry
```


Exemple Managing variables : 

```
#Get project details
gli get_project --project=sallamand/gli

#list project variables
gli get_variable --project=sallamand/gli --list

#get value for a specific variable
gli get_variable --project=sallamand/gli --key mavariable

#Create (or update)variable
gli set_variable --project=sallamand/gli --key mavariable --value mavalue
```

Enable/Disable Gitlab Registry for a project:

```
gli toggle_registry --project=sallamand/gli 
```


## Contribution

If you've cloned this project, and want to install the library (*and all
development dependencies*), the command you'll want to run is::

```
make install
```

If you'd like to run all tests for this project (*assuming you've written
some*), you would run the following command::

```
make test
```

This will trigger [py.test](http://pytest.org/latest/), along with its popular
[coverage](https://pypi.python.org/pypi/pytest-cov) plugin.


If you'd like to cut a new release of the CLI tool, and publish it to the Python PAckage Index [Pypi](https://pypi.python.org/pypi) :

```
make release
```

This will build both a source tarball of the CLI as well as a newer whell build


