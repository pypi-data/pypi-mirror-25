#!/usr/bin/env python

"""EventStreamProcessor.py: This is a quick hack. This is tested with OpenShift 3.6.0"""

__version__ = '0.4.0'
__license__ = "GPLv3+"

import os
import logging
import requests
import json
from threading import Thread
from urllib.parse import urlparse

from kafka import KafkaConsumer, KafkaProducer


RAW_TOPIC_NAME = 'openshift.raw'
DEPLOYMENTS_DISCOVERED_TOPIC_NAME = 'openshift.deployments.discovered'
DEPLOYMENTS_INFO_TOPIC_NAME = 'openshift.deployments.info'
DEPLOYMENTS_OBJECTS_TOPIC_NAME = 'openshift.deployments.objects'
BUILDS_DISCOVERED_TOPIC_NAME = 'openshift.builds.discovered'
BUILDS_COMPLETED_TOPIC_NAME = 'openshift.builds.completed'
BUILDS_OUTPUTINFO_TOPIC_NAME = 'openshift.builds.outputinfo'
PROJECTS_TOPIC_NAME = 'openshift.projects'
PODS_OBJECTS_TOPIC_NAME = 'openshift.pods.objects'

module_logger = logging.getLogger('EventStreamProcessor')

requests_log = logging.getLogger("requests.packages.urllib3")
module_logger.setLevel(logging.DEBUG)
module_logger.propagate = True


class EventStreamProcessor():
    """This is a very basic EventStreamProcessor, it will connect to Kafka and consume events for one certain topic.
    """

    def __init__(self, topic, bootstrap_servers=['localhost:9092']):
        self.bootstrap_servers = bootstrap_servers
        self.topic = topic

        # TODO make topic a list and subscribe to all the topics in that list..

        self.consumer = KafkaConsumer(self.topic,
                                      value_deserializer=lambda m: json.loads(
                                          m.decode('utf-8')),
                                      bootstrap_servers=self.bootstrap_servers)

    def consume(self):
        for message in self.consumer:
            module_logger.info("%s:%d:%d: key=%s value=%s" % (message.topic, message.partition,
                                                              message.offset, message.key,
                                                              message.value))


class EventStreamProcessorAndOpenShiftClient(EventStreamProcessor):
    """This EventStreamProcessor is an OpenShift client too.
    """

    def __init__(self, endpoint, token, topic, bootstrap_servers):
        super(EventStreamProcessorAndOpenShiftClient,
              self).__init__(topic, bootstrap_servers)

        self.threads = []
        self.endpoint = endpoint
        self.token = token
        self.classlogger = logging.getLogger(
            'EventStreamProcessorAndOpenShiftClient')

    def fetch(self, path, params=None):
        # TODO if we timeout on this request, do not ack the message

        self.classlogger.info("fetching %s form OpenShift Master API" %
                              (path))
        # ask Kubernetes rather than OpenShift
        if 'pods' in path:
            endpoint = self.endpoint.replace('oapi', 'api')
        else:
            endpoint = self.endpoint

        if not params == None:
            self.classlogger.debug("endpoint: %s, params: %s" %
                                   (endpoint, params))

        headers = {
            "Authorization": "Bearer %s" % self.token,
        }

        try:
            resp = requests.get(endpoint + path, params=params,
                                headers=headers, verify=False)

            if resp.status_code == 401:
                self.classlogger.warn("user is not authorized to view %s" %
                                      (path))
                return None
            elif resp.status_code == 404:
                self.classlogger.error("%s has not been found" % path)
                return None

            resp_content = resp.content
            return resp_content.decode('utf-8').splitlines()

        # TODO except more specific
        except Exception as e:
            self.classlogger.debug(self.endpoint + path,
                                   headers=headers, verify=False)
            self.classlogger.error(e)
            return None


class BuildsAndBuildInfoProcessor(EventStreamProcessorAndOpenShiftClient, Thread):
    """This EventStreamProcessor will identify completed Builds and emit BuildInfo
    to topic BUILDS_OUTPUTINFO_TOPIC_NAME.
    """
    daemon = True

    def __init__(self, endpoint, token, topic, bootstrap_servers,
                 group=None, target=None, name=None, args=(), kwargs=None):
        super(BuildsAndBuildInfoProcessor, self).__init__(
            endpoint, token, topic, bootstrap_servers)
        Thread.__init__(self, group=group, target=target, name=name)

        self.producer = KafkaProducer(bootstrap_servers=self.bootstrap_servers,
                                      value_serializer=lambda m: json.dumps(
                                          m).encode('utf-8'),
                                      retries=5)

        self.classlogger = logging.getLogger('BuildsAndBuildInfoProcessor')

    def run(self):
        self.consume()

    def consume(self):
        for message in self.consumer:
            event = message.value['event']

            if 'reason' in event.keys():
                if event['reason'] == 'BuildCompleted':  # lets get all the completed builds
                    self.classlogger.info("Found a Build that has been completed: %s/%s" %
                                          (event['involvedObject']['namespace'],
                                           event['involvedObject']['name']))

                    b = {}
                    b['kind'] = 'BuildOutputInfo'
                    b['metadata'] = {}
                    b['metadata']['namespace'] = event[
                        'involvedObject']['namespace']
                    b['metadata']['name'] = event['involvedObject']['name']
                    b['metadata']['annotations'] = {}
                    b['metadata']['annotations'][
                        'openshift.io/build.name'] = event['involvedObject']['name']

                    build = self._fetchAndPublishBuild(event['involvedObject']['namespace'],
                                                       event['involvedObject']['name'])

                    if build == None:
                        continue

                    g = {}
                    g['source'] = {}
                    try:
                        g['source'] = build['spec']['source']['git']
                        g['revision'] = build['spec'][
                            'revision']['git']['commit']
                    except KeyError as e:
                        pass

                    d = {}
                    d['namespace'] = build['metadata']['namespace']
                    d['imageStreamTagName'] = build[
                        'spec']['output']['to']['name']
                    d['imageDigest'] = build['status'][
                        'output']['to']['imageDigest']

                    b['sourceInfo'] = g
                    b['outputInfo'] = d

                    self.producer.send(BUILDS_OUTPUTINFO_TOPIC_NAME, b)

    def _fetchAndPublishBuild(self, namespace, name):
        build = self.fetch("namespaces/%s/builds/%s" % (namespace, name))

        if build != None:
            try:
                _buildlog = json.loads("".join(build))
            except json.JSONDecodeError as e:
                self.classlogger.error(e)
                return None

            self.producer.send(BUILDS_COMPLETED_TOPIC_NAME, _buildlog)
            self.producer.flush()

            return _buildlog

        return None

if __name__ == '__main__':
    pass
