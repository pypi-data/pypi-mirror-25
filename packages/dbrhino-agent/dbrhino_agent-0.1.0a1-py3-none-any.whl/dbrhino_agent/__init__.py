#!/usr/bin/env python3
import click
from .click_utils import CONFIG, CONFIG_OPTS
from .remote import Remote
from .grants import Grant
import logging
from requests.exceptions import ConnectionError
import time

logging.basicConfig()
root_logger = logging.getLogger("")
root_logger.level = logging.DEBUG
logger = logging.getLogger(__name__)


@click.command("upsert-databases")
@click.option(*CONFIG, **CONFIG_OPTS)
def upsert_databases(config):
    Remote(config).upsert_databases()


def _fetch_and_apply_grants(remote):
    for grant_def in remote.fetch_grants():
        try:
            grant = Grant(**grant_def)
            db = remote.config.find_database(grant.database)
            db.implement_grant(grant)
        except:
            logger.exception("Unknown error implementing grant")


def _run_once(remote):
    try:
        remote.upsert_databases()
        _fetch_and_apply_grants(remote)
    except:
        logger.exception("Unknown error")


@click.command()
@click.option(*CONFIG, **CONFIG_OPTS)
def run(config):
    _run_once(Remote(config))


@click.command()
@click.option(*CONFIG, **CONFIG_OPTS)
@click.option("--interval-secs", type=click.INT, default=30)
def server(config, interval_secs):
    remote = Remote(config)
    while True:
        _run_once(remote)
        time.sleep(interval_secs)


@click.group()
def cli():
    pass

cli.add_command(upsert_databases)
cli.add_command(run)
cli.add_command(server)


def main():
    cli()
