import click
import logging

from maisie import Projects
from maisie.cli.display import Display

from textwrap import wrap

import os


DEFAULT_DISPLAY_ATTRIBUTES = [
    "id",
    # "workspace_id",
    "name",
    "description",
    "git_url",
    "created",
]


@click.group()
def projects():
    pass


@click.command()
@click.option(
    "-n", "--name", prompt="Project's name", help="Name of the project to add"
)
@click.option(
    "-d",
    "--description",
    prompt="Project's description",
    help="Description of the project to add",
)
@click.option(
    "-git", "--git_url", prompt="Git Repository (URL)", help="Url of git repository"
)
@click.pass_context
def add(context, name, description, git_url):
    project = Projects()
    project = project.create(name, description, git_url)
    title = "Project"
    include = DEFAULT_DISPLAY_ATTRIBUTES
    display = Display(
        context=context, response=project, attributes=include, title=title
    )
    display.display_response()


@click.command()
def rm():
    pass


@click.command()
@click.option(
    "-id", "--id", default=None, type=int, help="Returns project with a specified id"
)
@click.pass_context
def ls(context, id):
    if id:
        projects = Projects().get(id)
    else:
        projects = Projects().get_all()
    if projects:
        title = "List of projects"
        include = DEFAULT_DISPLAY_ATTRIBUTES
        display = Display(
            context=context, response=projects, attributes=include, title=title
        )
        display.display_response()


projects.add_command(add)
projects.add_command(rm)
projects.add_command(ls)
