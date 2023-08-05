# coding=utf8

import shutil
import click
import sys
from result2 import Result



def command(func):
    cli.add_command(func)
    return func


@click.group()
def cli():
    pass

@command
@click.command()
@click.argument('ak')
@click.argument('sk')
@click.argument('bk')
def nr(ak, sk, bk):
    """
    新建rep
    :param ak:
    :type ak:
    :param sk:
    :type sk:
    :param bk:
    :type bk:
    :return:
    :rtype:
    """
    from sync import ReponsitoryConfig
    rs = ReponsitoryConfig().new_reponsitory(ak, sk, bk)
    if rs == Result.Ok:
        click.echo('saved!')
    click.echo(rs())


@command
@click.command()
@click.argument('ak')
@click.argument('sk')
@click.argument('bk')
def ur(ak, sk, bk):
    """
    更新rep
    :param ak:
    :type ak:
    :param sk:
    :type sk:
    :param bk:
    :type bk:
    :return:
    :rtype:
    """
    from sync import ReponsitoryConfig
    rs = ReponsitoryConfig().update_reponsitory(ak, sk, bk)
    if rs == Result.Ok:
        click.echo('saved!')
    click.echo(rs())


@command
@click.command()
def syn():
    """
    开始上传
    :return:
    :rtype:
    """
    from sync import ReponsitoryConfig, SyncProcessor
    syncProcessor = SyncProcessor(ReponsitoryConfig())
    rs = syncProcessor.auth()
    if rs == Result.Err:
        click.echo(rs())
        sys.exit(1)
    click.echo('Authenticated...')

    for fk, fp in syncProcessor.iterFiles():
        r = syncProcessor.upfile(fk, fp)
        if r == Result.Ok:
            click.echo('file: %s upload success!' % fk)
        else:
            click.echo(r())


def main():
    cli()

if __name__ == "__main__":
    main()