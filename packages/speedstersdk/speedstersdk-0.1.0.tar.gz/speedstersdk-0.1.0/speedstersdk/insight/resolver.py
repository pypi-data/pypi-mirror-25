# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from smdutils import logging
from abc import ABCMeta, abstractmethod

logger = logging.getLogger(__name__)


class InsightResolverException(Exception):
    pass


class InsightResolver:
    __metaclass__ = ABCMeta

    def __init__(self, dormerapi):
        self.dormerapi = dormerapi
        self.insights = {}
        self.updated_insights = {}

    @abstractmethod
    def resolve(self):
        pass

    def save_updated_insights(self):
        for msisdn, insigths in self.updated_insights.iteritems():
            logger.debug('Updating insights for MSISDN: %s - %s', msisdn, insigths)
            for insigth in insigths:
                payload = insigths[insigth]
                payload["msisdn"] = msisdn
                self.dormerapi.post(insigth, payload)

    def get_insight(self, msisdn, insight_name):
        if msisdn not in self.insights:
            return None
        else:
            insights = self.insights[msisdn]
            if insight_name not in insights:
                return None
            return insights[insight_name]

    def update_insight(self, msisdn, insight_name, insight):
        if msisdn not in self.insights:
            self.insights[msisdn] = {}

        self.insights[msisdn][insight_name] = insight

        if msisdn not in self.updated_insights:
            self.updated_insights[msisdn] = {}

        self.updated_insights[msisdn][insight_name] = insight