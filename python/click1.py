#!/usr/bin/env python
# -*- coding: utf-8 -*-


import click

@click.command()
@click.option('--userlist', '-u', default='kothand', help='Comma-separated list of users')
@click.option('--fslist', '-f', default='/', help='Filesystems to report on')

def sayhello(fslist, userlist):
    click.echo('Hello, we will report on filesystems %s for users %s!' % (fslist,userlist))

if __name__ == '__main__':
    sayhello()