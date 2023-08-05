# This file sits next to compiled redis
import subprocess

import os
import psutil

# Not exactly needed but really helps with testing...
try:
    import pkg_resources
    pkg = pkg_resources.get_distribution('open-redis')
    _path = pkg.location+ '/' + 'open_redis'
except:
    _path = os.path.realpath(__file__).rsplit("/", 1)[0]
VERSION = '3.2.10'
REDIS_PATH = os.path.realpath(_path + '/redis-' + VERSION + '/src/redis-server')
_REDIS_BASE_CONFIG_PATH = os.path.realpath(_path + '/redis-base-config')
EXEC_NAME ='redis-server'

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

    def __init__(self, deployment_directory_location, port=6379, conf=None):
        self.deployment_directory_location = os.path.abspath(os.path.expanduser(deployment_directory_location))
        self._port = port
        self.conf = conf

    # TODO: start() should block until server is actually up
    def start(self, as_process=False, log=None):
        """
        Blocks until server closes if as_process is true. Otherwise it's started as a child process.

        :param as_process: if true will replace current process with the current process (useful if calling from cmd line)
        :return:
        :rtype: None
        """
        # Runs the start command (if not already running on the port)
        proc = RedisDeployment._running_on_port(self._port)
        if None is proc:
            # Create Deployment Folder (if not exists)
            if not os.path.exists(self.deployment_directory_location):
                os.makedirs(self.deployment_directory_location)

            # Generate Config File
            file_object = open(_REDIS_BASE_CONFIG_PATH, 'r')
            base_config = file_object.read()
            file_object.close()

            if self.conf is not None:
                base_config += "\nInclude " + self.conf+"\n"

            if log:
                base_config = base_config.replace('{DEPLOY_LOCATION}/logs/redis.log', str(log))

            base_config = base_config.replace('{DEPLOY_PORT}', str(self._port))
            base_config = base_config.replace('{DEPLOY_LOCATION}', str(self.deployment_directory_location))


            # Write Generated File:
            generated_config = open(self.deployment_directory_location+"/redis.config", "w")
            generated_config.write(base_config)
            generated_config.close()

            # Create directory for default log location
            if not os.path.exists(self.deployment_directory_location+"/logs/"):
                os.makedirs(self.deployment_directory_location+"/logs/")

            # Start Server with given config file & port parameter
            if as_process:
                os.execl(REDIS_PATH, REDIS_PATH, *[self.deployment_directory_location+"/redis.config"])
            else:
                # Wrap in process
                process = subprocess.Popen([REDIS_PATH, self.deployment_directory_location+"/redis.config"],
                                           stdout=subprocess.PIPE,
                                           cwd=self.deployment_directory_location)

                # Default behavior is to kill the child on exit
                # This is also not the most efficient way to write this.
                import atexit
                def kill_child():
                    process.kill()
                atexit.register(kill_child)

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
        proc = RedisDeployment._running_on_port(self._port)
        if proc and proc.name() == EXEC_NAME:
            if not 'SYSTEM' in proc.username():
                proc.kill()

    def is_running(self):
        # Is redis running on specified port
        proc = RedisDeployment._running_on_port(self._port)
        if None is proc:
            return False
        else:
            if REDIS_PATH == proc.exe():
                return True
            else:
                return False

    @property
    def port(self):
        return self._port
