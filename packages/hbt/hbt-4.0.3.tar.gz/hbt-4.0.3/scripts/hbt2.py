#!/usr/bin/env python
# -*- coding: utf-8 -*-
import click
import os

from sourcefile import SourceFile
from config import HBTConfig
import pipeline

RBT_COMMAND_NAME = 'rbt'
CONTEXT_SETTINGS = dict(token_normalize_func=lambda x: RBT_COMMAND_NAME)

config = HBTConfig()


class AliasedGroup(click.Group):
    def get_command(self, ctx, cmd_name):
        return click.Group.get_command(self, ctx, cmd_name) or click.Group.get_command(self, ctx, RBT_COMMAND_NAME)


@click.command(cls=AliasedGroup)
def cli():
    pass


@click.command()
@click.argument('source_dir')
def copyright(source_dir):
    to_parse = list()
    for root, dirs, files in os.walk(source_dir):
        for file in files:
            source_file = SourceFile.create(root, file)
            if source_file:
                to_parse.append(source_file)
    [(click.echo(f.name), f.add_copyright()) for f in to_parse]


@click.command()
@click.argument('branch')
@click.pass_context
def land(ctx, branch):
    import pipeline
    pipeline.Pipeline.create_pipeline(config, ctx, pipeline.profile_land).run()


@click.command(context_settings=dict(ignore_unknown_options=True,))
@click.argument('rbt_args', nargs=-1, type=click.UNPROCESSED)
@click.pass_context
def rbt(ctx, rbt_args):
    pipeline.Pipeline.create_pipeline(config, ctx, pipeline.profile_rbt).run()


def main():
    cli.add_command(copyright)
    cli.add_command(land)
    cli.add_command(rbt)
    cli()


if __name__ == '__main__':
    main()
