#!/usr/bin/env python
# -*- coding: utf-8 -*-
import codecs
import os
import random
import re
import shutil
import subprocess
import tempfile
import time
from os.path import expanduser
from distutils.version import LooseVersion
from distutils.dir_util import copy_tree
from distutils.file_util import copy_file
import paramiko
from dyools import Logger, Path as P
import click
import dpath
import functools
import yaml
from configobj import ConfigObj
from paramiko import SSHClient
from scp import SCPClient

from prettytable import PrettyTable
from voluptuous import Required, All, Schema, MultipleInvalid, Optional, Any, Match, datetime

log = Logger()

__VERSION__ = '0.3.0'
__AUTHOR__ = ''
__WEBSITE__ = ''
__DATE__ = ''

home = expanduser("~")
home = os.path.join(home, '.dyvz')
DYPLOY_FILE = os.path.join(home, 'dyploy.ini')
COPY_FILE, COPY_DIRECTORY, COPY_CONTENT, SYNC = 'copy_file', 'copy_directory', 'copy_content', 'sync'
COMMAND = 'command'
LOCAL, REMOTE = 'local', 'remote'
schema = Schema({})


def validate(_data):
    try:
        schema(_data)
    except Exception as e:
        log.error(e.message)


try:
    os.makedirs(home)
except:
    pass

if not os.path.exists(DYPLOY_FILE):
    with codecs.open(DYPLOY_FILE, mode='w+', encoding='utf-8') as config_file:
        pass

schema_hosts = {
    Required(All(str)): Any(
        {
            Required('type'): LOCAL,
            Required('path'): All(str),
        },
        {
            Required('type'): REMOTE,
            Required('host'): All(str),
            Optional('port'): int,
            Required('login'): All(str),
            Required('password'): All(str),
            Required('path'): All(str),
        },
        {
            Required('type'): REMOTE,
            Required('host'): All(str),
            Optional('port'): int,
            Required('login'): All(str),
            Required('pkey'): All(str),
            Required('path'): All(str),
        }
    )
}
schema_vars = All([{
    Required(str): All()
}])
schema_operation = Any(
    {
        Optional('name'): str,
        Required('operation'): COMMAND,
        Required('in'): str,
        Required('command'): str,
    },
    {
        Optional('name'): str,
        Required('operation'): COPY_FILE,
        Required('from'): str,
        Required('to'): str,
        Required('source'): str,
        Required('destination'): str,
    },
    {
        Optional('name'): str,
        Required('operation'): COPY_DIRECTORY,
        Required('from'): str,
        Required('to'): str,
        Required('source'): str,
        Required('destination'): str,
    },
    {
        Optional('name'): str,
        Required('operation'): COPY_CONTENT,
        Required('from'): str,
        Required('to'): str,
        Required('source'): str,
        Required('destination'): str,
    },
    {
        Optional('name'): str,
        Required('operation'): SYNC,
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
                log.error('Can not process %s in the context %s' % (v_value, context))
            value = value.replace(main_v, v_value)
        for v_value in values2:
            main_v = v_value
            v_value = v_value[1:-1]
            try:
                v_value = unicode(eval(v_value, context))
            except:
                log.error('Can not process %s in the context %s' % (v_value, context))
            value = value.replace(main_v, v_value)
        for v_value in values3:
            main_v = 'rand_%s_%s' % v_value
            v_value = ''.join([random.choice(v_value[0]) for x in range(int(v_value[1]))])
            if not v_value:
                log.title('Can not process %s' % main_v)
            value = value.replace(main_v, v_value)
    if value:
        if not (re.match('^\d{4}-\d{2}-\d{2}$', value)):
            try:
                value = eval(value, context)
            except:
                pass
    return value


def get_yaml_data(ctx, name, value):
    if not os.path.isfile(value):
        log.error('The file <%s> not found' % value)
    __data = {}
    datas = [data for data in yaml.load_all(codecs.open(value, encoding='utf8', mode='r').read()) if data]
    if not datas:
        log.error('No data in the configuration file')
    for data in datas:
        try:
            data = schema_gloabl(data)
        except Exception as e:
            if hasattr(e, 'errors') and hasattr(e.errors, '__iter__'):
                err_msg = '\n'.join([str(x) for x in e.errors])
            else:
                err_msg = e.message
            log.error(err_msg)
        except MultipleInvalid as e:
            log.error(e.message)
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
        tasks = conf.copy()
        if 'version' in tasks:
            del tasks['version']
        if 'reference' in tasks:
            del tasks['reference']
        if 'hosts' in tasks:
            del tasks['hosts']
        if 'vars' in tasks:
            del tasks['vars']
        tasks = yaml_eval(str(tasks), context)
        conf.update(tasks)
    except Exception as e:
        log.error(e.message)
    try:
        hosts = yaml_eval(str(conf.get('hosts', {})), context)
        conf['hosts'] = hosts
    except Exception as e:
        log.error(e.message)
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
    for task in tasks:
        for i, task_data in enumerate(data.get(task)):
            operation = task_data.get('operation')
            values = functools.partial(dpath.util.values, obj=task_data)
            i += 1
            task_name = "{} - {}".format(i, task_data.get('name', '') or operation.title())
            log.title('*' * 80)
            log.title(('   Task : %s   ' % task_name).center(80, '*'))
            log.title('*' * 80)
            hosts_in_tasks = list(set(values(glob='/from') + values(glob='/to') + values(glob='/in')))
            hosts = {}
            for host_in_tasks in hosts_in_tasks:
                host_data = data.get('hosts').get(host_in_tasks, {})
                hosts[host_in_tasks] = host_data
                hosts[host_in_tasks]['name'] = host_in_tasks
                ttype = host_data.get('type')
                if ttype == REMOTE:
                    client = SSHClient()
                    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                    connect_kwargs = {}
                    if host_data.get('host', False):
                        connect_kwargs.update({'hostname': host_data.get('host')})
                    if host_data.get('port', False):
                        connect_kwargs.update({'port': host_data.get('port')})
                    if host_data.get('login', False):
                        connect_kwargs.update({'username': host_data.get('login')})
                    if host_data.get('password', False):
                        connect_kwargs.update({'password': host_data.get('password')})
                    if host_data.get('pkey', False):
                        connect_kwargs.update({'key_filename': host_data.get('pkey')})
                    client.connect(**connect_kwargs)
                    scp = SCPClient(client.get_transport())
                    sftp = paramiko.SFTPClient.from_transport(client.get_transport())
                    hosts[host_in_tasks]['client'] = client
                    hosts[host_in_tasks]['scp'] = scp
                    hosts[host_in_tasks]['sftp'] = sftp
                else:
                    hosts[host_in_tasks]['client'] = None
                    hosts[host_in_tasks]['scp'] = None
                    hosts[host_in_tasks]['sftp'] = None
            if operation in [COPY_FILE, COPY_DIRECTORY, COPY_CONTENT, SYNC]:
                _run_copy(ctx, operation, task_data, hosts)
            elif operation == COMMAND:
                _run_command(ctx, task_data, hosts)
            else:
                raise Exception('operation %s not implemented' % operation)


def _run_copy_file(ctx, operation_data, hosts):
    pass


def _run_copy(ctx, operation, operation_data, hosts):
    def _copy_directory_local_to_local(host_src, host_dest, dir_src, dir_dest):
        file_src = os.path.join(os.path.normpath(host_src.get('path')), os.path.normpath(dir_src))
        dir_dest = os.path.join(os.path.normpath(host_dest.get('path')), os.path.normpath(dir_dest))
        log.debug('From : %s' % file_src)
        log.debug('To : %s' % dir_dest)
        for path_item in P.subpaths(dir_dest, isfile=operation == COPY_CONTENT):
            try:
                os.makedirs(path_item)
            except:
                pass
        if operation == COPY_CONTENT:
            try:
                os.system('touch %s' % dir_dest)
            except:
                pass
            copy_file(file_src, dir_dest)
        elif operation == COPY_FILE:
            shutil.copy(file_src, dir_dest)
        elif operation == COPY_DIRECTORY:
            basename = os.path.basename(file_src)
            dir_dest = os.path.join(dir_dest, basename)
            copy_tree(file_src, dir_dest)
        else:
            copy_tree(file_src, dir_dest)

    def _copy_directory_remote_to_remote(host_src, host_dest, dir_src, dir_dest):
        tmp_dir = tempfile.mkdtemp(suffix='_tmpdir', prefix='dyploy_')
        _copy_directory_remote_to_local(host_src, {'path': tmp_dir}, dir_src, tmp_dir)
        file = os.path.join(tmp_dir, os.listdir(tmp_dir)[0])
        _copy_directory_local_to_remote({'path': file}, host_dest, file, dir_dest)
        shutil.rmtree(tmp_dir)

    def _copy_directory_local_to_remote(host_src, host_dest, dir_src, dir_dest):
        file_src = os.path.join(os.path.normpath(host_src.get('path')), os.path.normpath(dir_src))
        dir_dest = os.path.join(os.path.normpath(host_dest.get('path')), os.path.normpath(dir_dest))
        log.debug('From : %s' % file_src)
        log.debug('To : %s' % dir_dest)
        sftp = host_dest.get('sftp')
        for path_item in P.subpaths(dir_dest, isfile=operation == COPY_CONTENT):
            try:
                sftp.mkdir(path_item)
            except:
                pass
        scp = host_dest.get('scp')
        if operation == COPY_CONTENT:
            try:
                sftp.exec_command('touch %s' % dir_dest)
            except:
                pass
            scp.put(file_src, dir_dest)
        elif operation == COPY_FILE:
            scp.put(file_src, dir_dest)
        elif operation == COPY_DIRECTORY:
            scp.put(file_src, dir_dest, recursive=True)
        else:
            for item in os.listdir(file_src):
                scp.put(os.path.join(file_src, item), dir_dest, recursive=True)

    def _copy_directory_remote_to_local(host_src, host_dest, dir_src, dir_dest):
        file_src = os.path.join(os.path.normpath(host_dest.get('path')), os.path.normpath(dir_dest))
        dir_dest = os.path.join(os.path.normpath(host_src.get('path')), os.path.normpath(dir_src))
        log.debug('From : %s' % dir_dest)
        log.debug('To : %s' % file_src)
        for path_item in P.subpaths(file_src, isfile=operation == COPY_CONTENT):
            try:
                os.makedirs(path_item)
            except:
                pass
        scp = host_src.get('scp')
        sftp = host_src.get('sftp')
        if operation == COPY_CONTENT:
            try:
                os.system('touch %s' % file_src)
            except:
                pass
            scp.get(dir_dest, file_src, recursive=True)

        elif operation == COPY_FILE:
            scp.get(dir_dest, file_src)

        elif operation == COPY_DIRECTORY:
            scp.get(dir_dest, file_src, recursive=True)
        else:
            for item in sftp.listdir(dir_dest):
                scp.get(dir_dest, os.path.join(file_src, item), recursive=True)

    host_src = hosts.get(operation_data.get('from'))
    host_dest = hosts.get(operation_data.get('to'))
    ttype_src = host_src.get('type')
    ttype_dest = host_dest.get('type')
    log.info('copy directory from <%s> to <%s>' % (ttype_src, ttype_dest))
    dir_src = operation_data.get('source')
    dir_dest = operation_data.get('destination')
    if ttype_src == ttype_dest == LOCAL:
        _copy_directory_local_to_local(host_src, host_dest, dir_src, dir_dest)
    elif ttype_src == ttype_dest == REMOTE:
        _copy_directory_remote_to_remote(host_src, host_dest, dir_src, dir_dest)
    elif ttype_src == LOCAL and ttype_dest == REMOTE:
        _copy_directory_local_to_remote(host_src, host_dest, dir_src, dir_dest)
    elif ttype_src == REMOTE and ttype_dest == LOCAL:
        _copy_directory_remote_to_local(host_src, host_dest, dir_src, dir_dest)


def _run_copy_directory(ctx, operation_data, hosts):
    def _copy_directory_local_to_local():
        pass

    host_src = hosts.get(operation_data.get('from'))
    host_dest = hosts.get(operation_data.get('to'))
    ttype_src = host_src.get('type')
    ttype_dest = host_dest.get('type')
    log.info('copy directory from <%s> to <%s>' % (ttype_src, ttype_dest))
    dir_src = host_src.get('source')
    dir_dest = host_dest.get('destination')
    if host_src == host_dest == LOCAL:
        _copy_directory_local_to_local()


def _run_copy_content(ctx, operation_data, hosts):
    pass


def _run_command(ctx, operation_data, hosts):
    host = hosts.get(operation_data.get('in'))
    ttype = host.get('type')
    command = operation_data.get('command')
    log.info('execute the command : %s' % command)
    if ttype == LOCAL:
        orig_path = os.getcwd()
        os.chdir(host.get('path'))
        __execute_commands(ctx, command, ttype, host)
        os.chdir(orig_path)
    else:
        __execute_commands(ctx, command, ttype, host)


def __execute_commands(ctx, command, ttype, host):
    if ttype == LOCAL:
        if host.get('path', False):
            os.chdir(host.get('path'))
        log.code('Command : %s on th host <%s>' % (command, host.get('name', 'unknown')))
        p = subprocess.Popen(command.split(), stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
        out, err = p.communicate()
        if err:
            log.error(err)
        if out:
            log.success(out)
    else:
        stdin, stdout, stderr = host.get('client').exec_command(command)
        for line in stdout:
            log.success(line)
        for line in stderr:
            log.success(line)


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
        log.error('Some tasks are not found : %s' % diff_tasks)
    hosts_in_tasks = list(set(values(glob='/*/*/from') + values(glob='/*/*/to') + values(glob='/*/*/in')))
    hosts_in_hosts = values(glob='/hosts')[0].keys()
    diff_hosts = ', '.join([str(x) for x in set(hosts_in_tasks) - set(hosts_in_hosts)])
    if diff_hosts:
        log.error('Some hosts are not found : %s' % diff_hosts)
    log.warn('Running tasks ...')
    _run(ctx, tasks, conf)
    log.info('All tasks are executed, save the history and exit')
    save_history(ctx, conf)
    log.success('Finished without problems')


@cli.command()
@click.pass_context
def references(ctx):
    """Show references"""
    data = ctx.obj['history']
    log.title('References :')
    log.info(' - %s' % '\n - '.join(data.keys()))


@cli.command()
@click.option('-n', '--number', 'number', type=click.INT, default='10', help='Number of line by reference')
@click.option('-r', '--reference', 'reference', type=click.STRING, help='Number of line by reference')
@click.pass_context
def history(ctx, reference, number):
    """Show history"""
    data = ctx.obj['history']
    for ref, section_data in data.iteritems():
        if reference and reference != ref:
            continue
        log.title('Reference : %s' % ref)
        lines = [(k, v) for k, v in data.get(ref, {}).items()]
        lines = sorted(lines, key=lambda r: LooseVersion(r[0]), reverse=True)
        x = PrettyTable()
        x.field_names = ["Version", "Date"]
        x.align["Version"] = "l"
        x.align["Date"] = "c"
        n = 0
        for version, stamp in lines:
            if number > 0 and n == number:
                break
            x.add_row([version, stamp])
            n += 1
        log.info(x)


if __name__ == '__main__':
    cli(obj={})


def main():
    return cli(obj={})
