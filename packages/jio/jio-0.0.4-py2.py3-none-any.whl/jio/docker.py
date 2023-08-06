from docker import Client
from jio.exec import syscall
from jio.io import jio_log


DOCKER = Client(base_url='unix://var/run/docker.sock')


def dockcall(dock_id, command):
    '''calls a command inside of a dock'''
    dock_command = command.replace("\n", '')
    dock_command = "bash -c \"{}\"".format(dock_command)
    jio_log('dockcmd: {}'.format(dock_command))
    ret_command = DOCKER.exec_create(container=dock_id, cmd=dock_command, tty=True)
    exec_id = ret_command['Id']
    ret = DOCKER.exec_start(exec_id=exec_id, tty=True)
    jio_log(ret)
    return ret


def dockcall_detach(dock_id, command):
    '''calls a command inside of a dock'''
    dock_command = command.replace('\n', '')
    dock_command = 'bash -c "{}" &'.format(dock_command)
    jio_log('detach: {}'.format(dock_command))
    ret_command = DOCKER.exec_create(
        container=dock_id,
        cmd=dock_command,
        tty=True,
        stdout=False,
        stderr=False
    )
    exec_id = ret_command['Id']
    ret = DOCKER.exec_start(exec_id=exec_id, tty=True, detach=True)
    jio_log(ret)
    return ret


def copy_to_dock(dock_id, src, dest, skybox='.'):
    '''copies a file from src to dest in dock_id, with skybox being the directory the file is in'''
    try:
        src_filename = src.split('/')[-1]
    except Exception as exception_text:
        jio_log('copy_to_dock split failed: {}'.format(exception_text))
        src_filename = src
    if dest[-1] is not '/':
        dest += '/'
    syscall(
        'docker exec -i {} mkdir {}; cd {} && tar -c {} | docker exec -i {} /bin/tar -C {}'
        ' -x'.format(
            dock_id,
            dest,
            skybox,
            src,
            dock_id,
            dest
        )
    )
    syscall('docker exec -i {} unzip {}/{} -d {} >/dev/null 2>/dev/null'.format(
        dock_id,
        dest,
        src_filename,
        dest
    ))
    return True
