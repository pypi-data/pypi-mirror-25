#!/usr/bin/env python
# -*- coding: utf-8 -*-
import codecs
import os
import random
import re
import sys
import time
from os.path import expanduser
from distutils.version import LooseVersion

import click
import dpath
import functools
import yaml
from configobj import ConfigObj
from prettytable import PrettyTable
from voluptuous import Required, All, Schema, MultipleInvalid, Optional, Any, Match, datetime

__VERSION__ = '0.1.0'
__AUTHOR__ = ''
__WEBSITE__ = ''
__DATE__ = ''

home = expanduser("~")
home = os.path.join(home, '.dyvz')
DYPLOY_FILE = os.path.join(home, 'dyploy.ini')

schema = Schema({})


def error(ctx, _msg):
    click.secho(_msg, fg='red')
    ctx.abort()


def warn(_msg):
    click.secho(_msg, fg='yellow')


def validate(_data):
    try:
        schema(_data)
    except Exception as e:
        error(e.message)


try:
    os.makedirs(home)
except:
    pass

if not os.path.exists(DYPLOY_FILE):
    with codecs.open(DYPLOY_FILE, mode='w+', encoding='utf-8') as config_file:
        pass

schema_hosts = {
    Required(All(str)): Any({
        Required('type'): Any('local', 'remote'),
        Optional('login'): All(str),
        Optional('password'): All(str),
        Optional('pkey_file'): All(str),
        Required('path'): All(str),
    })
}
schema_vars = All([{
    Required(str): All()
}])
schema_operation = Any(
    {
        Required('operation'): 'copy_file',
        Required('from'): str,
        Required('to'): str,
        Required('source'): str,
        Required('destination'): str,
    },
    {
        Required('operation'): 'copy_directory',
        Required('from'): str,
        Required('to'): str,
        Required('source'): str,
        Required('destination'): str,
    },
    {
        Required('operation'): 'copy_content',
        Required('from'): str,
        Required('to'): str,
        Required('source'): str,
        Required('destination'): str,
    }
)
schema_tasks = [schema_operation]
schema_gloabl = Schema({
    Required('version'): All(Match('^\d+\.\d+\.\d+$')),
    Required('reference'): All(Match('^\w+$'), ),
    Optional('vars'): schema_vars,
    Required('hosts'): schema_hosts,
    Optional(All()): schema_tasks,
})


def yaml_eval(value, context):
    if not isinstance(value, basestring):
        return value
    pattern1 = re.compile("(\$\{[^}]+})")
    values1 = pattern1.findall(value)
    pattern2 = re.compile("(\$[^$]+\$)")
    values2 = pattern2.findall(value)
    pattern3 = re.compile("rand_([\s\*\$=+\.\d\w]+)_(\d+)")
    values3 = pattern3.findall(value)
    if values1 or values2 or values3:
        for v_value in values1:
            main_v = v_value
            v_value = v_value[2:-1]
            try:
                v_value = unicode(eval(v_value, context))
            except:
                click.secho('Can not process %s in the context %s' % (v_value, context), fg='red')
                sys.exit(-1)
            value = value.replace(main_v, v_value)
        for v_value in values2:
            main_v = v_value
            v_value = v_value[1:-1]
            try:
                v_value = unicode(eval(v_value, context))
            except:
                click.secho('Can not process %s in the context %s' % (v_value, context), fg='red')
                sys.exit(-1)
            value = value.replace(main_v, v_value)
        for v_value in values3:
            main_v = 'rand_%s_%s' % v_value
            v_value = ''.join([random.choice(v_value[0]) for x in range(int(v_value[1]))])
            if not v_value:
                click.secho('Can not process %s' % main_v, fg='red')
                sys.exit(-1)
            value = value.replace(main_v, v_value)
    if value:
        if not (re.match('\d{4}-\d{2}-\d{2}', value)):
            try:
                value = eval(value, context)
            except:
                pass
    return value


def get_yaml_data(ctx, name, value):
    if not os.path.isfile(value):
        error(ctx, 'The file <%s> not found' % value)
    __data = {}
    datas = [data for data in yaml.load_all(codecs.open(value, encoding='utf8', mode='r').read()) if data]
    if not datas:
        error(ctx, 'No data in the configuration file')
    for data in datas:
        try:
            data = schema_gloabl(data)
        except Exception as e:
            if hasattr(e, 'errors') and hasattr(e.errors, '__iter__'):
                err_msg = '\n'.join([str(x) for x in e.errors])
            else:
                err_msg = e.message
            error(ctx, err_msg)
        except MultipleInvalid as e:
            error(ctx, e.message)
        __data.update(data)
    return integrate_vars(ctx, __data)


@click.group()
@click.version_option(__VERSION__, is_flag=True, expose_value=False, is_eager=True, help="Show the version")
@click.pass_context
def cli(ctx):
    """CLI for Dyploy"""
    config_dyploy_obj = ConfigObj(DYPLOY_FILE, encoding='utf-8')
    ctx.obj['config_dyploy_obj'] = config_dyploy_obj
    history = {}
    for section in config_dyploy_obj.sections:
        history[section] = config_dyploy_obj.get(section, {})
    ctx.obj['history'] = history


def integrate_vars(ctx, conf):
    context = os.environ.copy()
    context['now'] = time.strftime('%Y%m%d_%H%M%S')
    context['today'] = time.strftime('%Y%m%d')
    for item in conf.get('vars', {}):
        for key, value in item.items():
            context[key] = yaml_eval(value, context)
    try:
        tasks = yaml_eval(str(conf.get('tasks', {})), context)
        conf['tasks'] = tasks
    except Exception as e:
        error(ctx, e.message)
    try:
        hosts = yaml_eval(str(conf.get('hosts', {})), context)
        conf['hosts'] = hosts
    except Exception as e:
        error(ctx, e.message)
    try:
        conf.pop('vars')
    except Exception as e:
        pass
    return conf


def save_history(ctx, data):
    config = ctx.obj['config_dyploy_obj']
    reference = data.get('reference')
    version = data.get('version')
    stamp = datetime.datetime.now().isoformat()
    if reference in config.keys():
        config[reference].update({
            version: stamp
        })
    else:
        config[reference] = {
            version: stamp
        }
    config.write()

def _run(ctx, tasks, data):
    pass

@cli.command()
@click.argument('tasks', nargs=-1, )
@click.option('--conf', 'conf', default='.dyploy.yml', help='Yaml file used for the configuration',
              callback=get_yaml_data)
@click.pass_context
def run(ctx, tasks, conf):
    """Run tasks"""
    conf = integrate_vars(ctx, conf)
    values = functools.partial(dpath.util.values, obj=conf)
    diff_tasks = ', '.join([str(x) for x in set(tasks) - set(conf.keys())])
    if diff_tasks:
        error(ctx, 'Some tasks are not found : %s' % diff_tasks)
    hosts_in_tasks = list(set(values(glob='/*/*/from') + values(glob='/*/*/to')))
    hosts_in_hosts = values(glob='/hosts')[0].keys()
    diff_hosts = ', '.join([str(x) for x in set(hosts_in_tasks) - set(hosts_in_hosts)])
    if diff_hosts:
        error(ctx, 'Some hosts are not found : %s' % diff_hosts)
    click.secho('Running tasks ...', fg='yellow')
    _run(ctx, tasks, conf)
    click.secho('All tasks are executed, save the history and exit', fg='green')
    save_history(ctx, conf)
    click.secho('Finished without problems', fg='green')


@cli.command()
@click.pass_context
def history(ctx):
    """Show history"""
    data = ctx.obj['history']
    for ref, section_data in data.iteritems():
        click.secho('Reference : %s' % ref, fg='blue')
        lines = [(k, v) for k, v in data.get(ref, {}).items()]
        lines = sorted(lines, key=lambda r: LooseVersion(r[0]), reverse=True)
        x = PrettyTable()
        x.field_names = ["Version", "Date"]
        x.align["Version"] = "l"
        x.align["Date"] = "c"
        for version, stamp in lines:
            x.add_row([version, stamp])
        click.echo(x)


if __name__ == '__main__':
    cli(obj={})


def main():
    return cli(obj={})
