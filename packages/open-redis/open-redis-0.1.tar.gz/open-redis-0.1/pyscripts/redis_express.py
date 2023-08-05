from open_redis.deployment import REDIS_PATH, VERSION, RedisDeployment
import argparse

parser = argparse.ArgumentParser(
    description='A commandline utility to launch redis. All output (e.g. logs, dumps, etc) will go into the chosen deployment folder (unless overridden)')
parser.add_argument('-d', '--deploy_folder', default=None, type=str, help="Folder to deploy to", required=True)
parser.add_argument('-c', '--config_file', default=None, type=str, help="Path to additional configuration file",
                    nargs='?', required=False)
parser.add_argument('-p', '--port', default=6379, type=int, help="The port to start the server on", nargs='?',
                    required=False)


def main():
    args = parser.parse_args()
    print("Redis install location: " + REDIS_PATH)
    print("Using Redis Version: " + VERSION)
    log = None
    if args.config_file == None:
        log = '""'
    deployment = RedisDeployment(args.deploy_folder, args.port, args.config_file)
    deployment.start(True,log=log)

if __name__ == '__main__':
    main()
