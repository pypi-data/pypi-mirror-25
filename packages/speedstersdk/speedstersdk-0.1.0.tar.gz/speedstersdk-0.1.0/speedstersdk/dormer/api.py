# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from smdutils import logging
from smdutils.clients.dormer import DormerClient
import requests
from speedstersdk.insight import insights

logger = logging.getLogger(__name__)


class DormerStorageException(Exception):
    pass


class DormerStorage(object):

    def __init__(self, url, api_key, api_secret, consumer_id, organization):
        headers = [
            "x-consumer-id: {}".format(consumer_id),
            'x-scopes: {\"admin\":true,\"admin_write\":true}'
        ]
        self.dormer = DormerClient(dormer_url=url, dormer_api_key=api_key,
                                   dormer_api_secret=api_secret, custom_dormer_headers=headers)
        self.organization = organization
        self.consumer_id = consumer_id
        self._load_dataset()

    def _load_dataset(self):
        self.dormer.create_organization(self.organization)
        for insigh in [insights.NLC, insights.IMSI, insights.IMEI]:
            self.dormer.create_dataset(self.organization, str(insigh), str("msisdn"),
                                      [self.consumer_id], [self.consumer_id])

    def get_data(self, dataset, msisdn):
        data = self.dormer.get(msisdn, self.organization, dataset)
        if not data:
            logger.error("Error response getting insights of MSISDN: %s - status code: %s",
                         msisdn, "")
            raise DormerStorageException("Error response getting insights of MSISDN %s - %s" % (msisdn, ""))

    def store_data(self, dataset, payload):
        if not self.dormer.store(payload, 0, self.organization, dataset):
            logger.error("Error response creating insights of MSISDN: {}".format(payload["msisdn"]))
            raise DormerStorageException("Error response updating insights of MSISDN {}".format(payload["msisdn"]))
