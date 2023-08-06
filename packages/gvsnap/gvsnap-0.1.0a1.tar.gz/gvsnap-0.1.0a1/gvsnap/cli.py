# -*-coding:utf-8 -*
""" Main CLI module."""

import click
import vagrant
import git
import os
import time
from halo import Halo
import maya


@click.group()
@click.option('--debug/--no-debug', default=False)
def main(debug):
    # click.echo('Debug mode is %s' % ('on' if debug else 'off'))
    pass


@main.command()
def list():
    """ Saves a Vagrant snapshot tagged for this Repo's branch and commit."""
    click_echo_snapshot_list()


def click_echo_snapshot_list():
    """ Print the snapshot list."""
    vagrant_obj = vagrant.Vagrant()
    spinner = Halo(text='Loading snapshot list ...', spinner='dots')
    spinner.start()
    try:
        snapshot_list = vagrant_obj.snapshot_list()
        spinner.succeed('It worked!')
    except:
        click.echo("Error while running Vagrant command (vagrant snapshot list).")
        return
    # click.echo(snapshot_list)
    for idx, snap in enumerate(parse_snapshot_list(snapshot_list)):
        click.echo("[{}] {} {} {} ({})".format(idx, snap["name"], snap["sha"], snap["slang_time"], snap["exact_time"]))
    return snapshot_list


@main.command()
def save():
    """ Saves a Vagrant snapshot tagged for this Repo's branch and commit."""
    spinner = Halo(text='Saving ...', spinner='dots')
    spinner.start()
    repo = git.Repo(os.getcwd(), search_parent_directories=True)
    sha = repo.head.object.hexsha
    sha_short = repo.git.rev_parse(sha, short=7)
    branch_name = repo.active_branch.name
    epoch_time = int(time.time())
    snapshot_name = "{}-{}-{}".format(branch_name, sha_short, epoch_time)
    vagrant_obj = vagrant.Vagrant()
    vagrant_obj.snapshot_save(snapshot_name)
    spinner.succeed('It worked!')
    click.echo("'{}' saved.".format(snapshot_name))

@main.command()
@click.argument('branch', required=False)
def restore(branch=None):
    """ Restores a Vagrant snapshot tagged for this Repo's branch and commit."""
    if branch:
        click.echo('Restoring most recent from branch {}'.format(branch))
        restore_snapshot_name = branch
    else:
        snapshot_list = click_echo_snapshot_list()
        restore_snapshot = input('Restore with snapshot #:')
        click.echo("I'm supposed to restore to {}".format(restore_snapshot))
        click.echo(snapshot_list[restore_snapshot])
        restore_snapshot_name = snapshot_list[restore_snapshot]
    spinner = Halo(text='Restoring ... this may take a minute.', spinner='dots')
    spinner.start()
    vagrant_obj = vagrant.Vagrant()
    vagrant_obj.snapshot_restore(restore_snapshot_name)
    spinner.succeed('It worked!')

def parse_snapshot_list(snap_list):
    """ Parse the snapshot list."""
    return_list = []
    for snap in snap_list:
        try:
            timestamp = snap.split("-")[-1]
            time_maya = maya.MayaDT(int(timestamp))
            slang_time = time_maya.slang_time()
            exact_time = time_maya.rfc2822()
            sha = snap.split("-")[-2]
            name = snap.split("-" + sha)[0]
        except ValueError:
            timestamp=None
            sha=None
            name=snap
            slang_time=None
            exact_time=None
        except IndexError:
            timestamp=None
            sha=None
            name=snap
            slang_time=None
            exact_time=None
        return_list.append(dict(timestamp=timestamp, name=name, sha=sha, slang_time=slang_time, exact_time=exact_time))
    return return_list
