import click
import webbrowser
from tabulate import tabulate
from time import sleep

import russell
from russell.cli.utils import get_task_url, get_module_task_instance_id
from russell.client.common import get_url_contents
from russell.client.experiment import ExperimentClient
from russell.client.module import ModuleClient
from russell.client.task_instance import TaskInstanceClient
from russell.client.project import ProjectClient
from russell.config import generate_uuid
from russell.manager.experiment_config import ExperimentConfigManager
from russell.manager.russell_ignore import RussellIgnoreManager
from russell.model.experiment_config import ExperimentConfig
from russell.log import logger as russell_logger
import requests,json
from kafka import KafkaConsumer
import sys


@click.command()
@click.argument('project_url_or_id', nargs=1)
def clone(project_url_or_id):
    """
    Initialize new project at the current dir.
    After create run your command. Example:

        russell run "python tensorflow.py > /output/model.1"
    """
    # experiment_config = ExperimentConfig(name=project,
                                         # family_id=generate_uuid())
    # ExperimentConfigManager.set_config(experiment_config)
    # RussellIgnoreManager.init()

    ProjectClient().clone(project_url_or_id,
                          uncompress=True,
                          delete_after_uncompress=True)
