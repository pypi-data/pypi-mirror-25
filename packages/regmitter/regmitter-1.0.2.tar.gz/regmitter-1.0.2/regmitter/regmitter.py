import docker
import logger
import traceback

import logging


class Regmitter(object):
    def __init__(self, version="auto", filelog=None):
        global log

        if "log" not in globals():
            if filelog is not None:
                log = logging.getLogger(__name__)
                log.addHandler(logger.FileHandler(filelog))
                log.setLevel(logging.DEBUG)
            else:
                log = logging.getLogger(__name__)
                log.addHandler(logger.StreamHandler())
                log.setLevel(logging.DEBUG)

        self.docker_client = docker.DockerClient(version=version)

    def pull(self, images):
        for idx, name in enumerate(images.iteritems()):
            for tag in name[1]:
                try:
                    self.docker_client.images.pull(name=name[0], tag=tag)
                    log.info("{}:{} pulled successfully".format(name[0], tag))
                except:
                    log.error("{}:{} failed\n{}".format(
                        name[0], tag, traceback.format_exc()))
            log.info("{} of {}".format(idx + 1, len(images)))

    def push(self, images):
        for idx, name in enumerate(images.iteritems()):
            for tag in name[1]:
                try:
                    self.docker_client.images.push(
                        repository=name[0], tag=tag)
                    log.info("{}:{} pushed successfully".format(name[0], tag))
                except:
                    log.error("{}:{} failed\n{}".format(
                        name[0], tag, traceback.format_exc()))
            log.info("{} of {}".format(idx + 1, len(images)))

    def remove(self, images):
        for idx, name in enumerate(images.iteritems()):
            for tag in name[1]:
                try:
                    self.docker_client.images.remove(
                        "{}:{}".format(name[0], tag), force=True)
                    log.info("{}:{} removed successfully".format(name[0], tag))
                except:
                    log.error("{}:{} failed".format(
                        name[0], tag, traceback.format_exc()))
            log.info("{} of {}".format(idx + 1, len(images)))
