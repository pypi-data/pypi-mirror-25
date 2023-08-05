# This file sits next to compiled redis
import subprocess

import os
from time import sleep

import psutil

# Not exactly needed but really helps with testing...
try:
    import pkg_resources

    pkg = pkg_resources.get_distribution('open-redis')
    _path = pkg.location + '/' + 'open_redis'
except:
    _path = os.path.realpath(__file__).rsplit("/", 1)[0]
VERSION = '4.0.1'
REDIS_PATH = os.path.realpath(_path + '/redis-' + VERSION + '/src/redis-server')
REDIS_SENTINEL_PATH = os.path.realpath(_path + '/redis-' + VERSION + '/src/redis-sentinel')
_REDIS_BASE_CONFIG_PATH = os.path.realpath(_path + '/redis-base-config')
_SENTINEL_BASE_CONFIG_PATH = os.path.realpath(_path + '/sentinel-base-config')
EXEC_NAME = 'redis-server'
SENTINEL_EXEC_NAME = 'redis-sentinel'

import socket
from contextlib import closing


def find_free_port():
    with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as s:
        s.bind(('', 0))
        return s.getsockname()[1]


class RedisDeployment(object):
    @staticmethod
    def _running_on_port(find_port):
        """
        Check if any processes are bound to a particular port.
        Returns bound processes
        """
        # Iterate over all system processes (ps)
        for proc in psutil.process_iter():
            # Iterate over all ports this process is listening to
            try:
                data = proc.connections()

                for con in data:
                    # Tuple ip, port
                    port = con.laddr[1]
                    if port == find_port and con.status == 'LISTEN':
                        return proc
            except psutil.AccessDenied:
                pass

        # Did we find all ports we wanted to
        return None

    @staticmethod
    def list_running_instances():
        """
        Returns list of running redis instances running on the server
        :return: list of  RedisDeployment
        :rtype: List[RedisDeployment]
        """
        results = []
        for proc in psutil.process_iter():
            try:
                # print(proc.exe())
                n = proc.exe()

                if EXEC_NAME == proc.name():
                    port = -1
                    for connection in proc.connections():
                        if connection.status == 'LISTEN':
                            port = connection.laddr[1]
                    results.append(RedisDeployment(proc.cwd(), port))
                    # TODO: get working directory...

                    # for con in proc.get_connections():
                    #     # Tuple ip, port
                    #     port = con.local_address[1]
                    #     if port is find_port:
                    #         return proc

                    # results.append(RedisDeployment(proc.))

            except psutil.NoSuchProcess:
                pass
            except psutil.AccessDenied:
                pass

        return results

    def __init__(self, deployment_directory_location, port=None, conf=None):
        if port is None:
            port = find_free_port()

        self.deployment_directory_location = os.path.abspath(os.path.expanduser(deployment_directory_location))
        self.port = port
        self.conf = conf

    # TODO: start() should block until server is actually up
    def start(self, as_process=False, log=None,
              master_ip=None, master_port=None):
        """
        Blocks until server closes if as_process is true. Otherwise it's started as a child process.

        :param as_process: if true will replace current process with the redis process (useful if calling from cmd line)
        :return:
        :rtype: None
        """
        # Runs the start command (if not already running on the port)
        proc = RedisDeployment._running_on_port(self.port)
        if None is proc:
            # Create Deployment Folder (if not exists)
            if not os.path.exists(self.deployment_directory_location):
                os.makedirs(self.deployment_directory_location)

            # Generate Config File
            file_object = open(_REDIS_BASE_CONFIG_PATH, 'r')
            base_config = file_object.read()
            file_object.close()

            if log:
                base_config = base_config.replace('{DEPLOY_LOCATION}/logs/redis.log', str(log))

            base_config = base_config.replace('{DEPLOY_PORT}', str(self.port))
            base_config = base_config.replace('{DEPLOY_LOCATION}', str(self.deployment_directory_location))

            if master_ip is not None and master_port is not None:
                base_config += '\n slaveof ' + str(master_ip) + ' ' + str(master_port)+"\n"

            if self.conf is not None:
                base_config += "\nInclude " + self.conf + "\n"

            # Write Generated File:
            generated_config = open(self.deployment_directory_location + "/redis.config", "w")
            generated_config.write(base_config)
            generated_config.close()

            # Create directory for default log location
            if not os.path.exists(self.deployment_directory_location + "/logs/"):
                os.makedirs(self.deployment_directory_location + "/logs/")

            # Start Server with given config file & port parameter
            if as_process:
                os.execl(REDIS_PATH, REDIS_PATH, *[self.deployment_directory_location + "/redis.config"])
            else:
                # Wrap in process
                process = subprocess.Popen([REDIS_PATH, self.deployment_directory_location + "/redis.config"],
                                           stdout=subprocess.PIPE,
                                           cwd=self.deployment_directory_location)

                # Default behavior is to kill the child on exit
                # This is also not the most efficient way to write this.
                import atexit
                def kill_child():
                    process.kill()

                atexit.register(kill_child)
            sleep(.5)

        else:
            if proc.exe() == EXEC_NAME:
                raise Exception("A Redis Server Is Already Running On Specified Port: " + str(proc.as_dict()))
            else:
                raise Exception("Process Already Running On Specified Port: " + str(proc.as_dict()))

    def clean(self):
        """
        Removes All Logs & Stored Data On The Deployment
        :return:
        """
        raise Exception("Not implemented....")

    def stop(self):
        """
        Stops the process on the running port if its a redis instance...
        :return:
        """
        # Kill launched process (if present) and daemon
        proc = RedisDeployment._running_on_port(self.port)
        if proc and proc.name() == EXEC_NAME:
            if not 'SYSTEM' in proc.username():
                proc.kill()

    def is_running(self):
        # Is redis running on specified port
        proc = RedisDeployment._running_on_port(self.port)
        if None is proc:
            return False
        else:
            if REDIS_PATH == proc.exe():
                return True
            else:
                return False



class RedisSentinel(object):
    @staticmethod
    def _running_on_port(find_port):
        """
        Check if any processes are bound to a particular port.
        Returns bound processes
        """
        # Iterate over all system processes (ps)
        for proc in psutil.process_iter():
            # Iterate over all ports this process is listening to
            try:
                data = proc.connections()

                for con in data:
                    # Tuple ip, port
                    port = con.laddr[1]
                    if port == find_port and con.status == 'LISTEN':
                        return proc
            except psutil.AccessDenied:
                pass

        # Did we find all ports we wanted to
        return None

    @staticmethod
    def list_running_instances():
        """
        Returns list of running redis instances running on the server
        :return: list of  RedisDeployment
        :rtype: List[RedisDeployment]
        """
        results = []
        for proc in psutil.process_iter():
            try:
                # print(proc.exe())
                n = proc.exe()

                if SENTINEL_EXEC_NAME == proc.name():
                    port = -1
                    for connection in proc.connections():
                        if connection.status == 'LISTEN':
                            port = connection.laddr[1]
                    results.append(RedisDeployment(proc.cwd(), port))
                    # TODO: get working directory...
            except psutil.NoSuchProcess:
                pass
            except psutil.AccessDenied:
                pass

        return results

    def __init__(self, deployment_directory_location, port=None, conf=None):
        if port is None:
            port = find_free_port()
        self.deployment_directory_location = os.path.abspath(os.path.expanduser(deployment_directory_location))
        self.port = port
        self.conf = conf

    def start(self, as_process=False, master_name='mymaster', master_ip='127.0.0.1', master_port=6379, quorum=1):
        """
        Blocks until server closes if as_process is true. Otherwise it's started as a child process.

        :param quorum: Number of sentinels required for quorum
        :param master_port: Master port
        :param master_ip:  Master ip
        :param master_name: Master Name
        :param as_process: if true will replace current process with the sentinel (useful if calling from cmd line)
        :return:
        :rtype: None
        """
        # Runs the start command (if not already running on the port)
        proc = RedisSentinel._running_on_port(self.port)
        if None is proc:
            # Create Deployment Folder (if not exists)
            if not os.path.exists(self.deployment_directory_location):
                os.makedirs(self.deployment_directory_location)

            # Generate Config File
            file_object = open(_SENTINEL_BASE_CONFIG_PATH, 'r')
            base_config = file_object.read()
            file_object.close()

            base_config = base_config.replace('{DEPLOY_PORT}', str(self.port))
            base_config = base_config.replace('{DEPLOY_LOCATION}', str(self.deployment_directory_location))

            base_config = base_config.replace('{MASTER_NAME}', master_name)
            base_config = base_config.replace('{MASTER_IP}', str(master_ip))
            base_config = base_config.replace('{MASTER_PORT}', str(master_port))
            base_config = base_config.replace('{QUORUM}', str(quorum))

            if self.conf is not None:
                base_config += '\n' + open(self.conf, 'r').read()

            # Write Generated File:
            generated_config = open(self.deployment_directory_location + "/sentinel.config", "w")
            generated_config.write(base_config)
            generated_config.close()

            # Start Server with given config file & port parameter
            if as_process:
                os.execl(REDIS_SENTINEL_PATH, REDIS_SENTINEL_PATH,
                         *[self.deployment_directory_location + "/sentinel.config"])
            else:
                # Wrap in process
                process = subprocess.Popen(
                    [REDIS_SENTINEL_PATH, self.deployment_directory_location + "/sentinel.config"],
                    stdout=subprocess.PIPE,
                    cwd=self.deployment_directory_location)

                # Default behavior is to kill the child on exit
                # This is also not the most efficient way to write this.
                import atexit
                def kill_child():
                    process.kill()

                atexit.register(kill_child)

        else:
            if proc.exe() == SENTINEL_EXEC_NAME:
                raise Exception("A Sentinel Is Already Running On Specified Port: " + str(proc.as_dict()))
            else:
                raise Exception("Process Already Running On Specified Port: " + str(proc.as_dict()))

    def stop(self):
        """
        Stops the process on the running port if its a redis instance...
        :return:
        """
        # Kill launched process (if present) and daemon
        proc = RedisSentinel._running_on_port(self.port)
        if proc and proc.name() == SENTINEL_EXEC_NAME:
            if not 'SYSTEM' in proc.username():
                proc.kill()
