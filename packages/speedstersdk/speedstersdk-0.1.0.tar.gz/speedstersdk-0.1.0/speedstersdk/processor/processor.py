# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from smdutils import logging
from smdutils.monitor.idle import idle
import json


logger = logging.getLogger(__name__)


class Processor(object):
    SEQ_STORAGE_KEY = 'seq'
    SEQ_STORAGE_FOLDER_PREFIX = 'mves-one-speedster'

    def __init__(self, resolver_class, streamer, oneapi, seq, seq_storage, seq_storage_key):
        self.resolver_class = resolver_class
        self.streamer = streamer
        self.oneapi = oneapi
        self.seq = seq
        self.seq_storage = seq_storage
        self.seq_storage_key = None
        self._init_seq(seq_storage_key)

    def run(self):
        logger.warning("Starting streamer event processing")

        while True:
            logger.debug("Connecting to backlog [%s] from sequence [%d]", self.streamer.backloger_bid, self.seq)
            stream = self.streamer.get_stream(self.seq)

            try:
                # Read events line by line
                for line in stream.iter_lines():
                    # Ignore empty lines
                    line = line.strip()
                    if line == '':
                        continue

                    self.process_line(line)

            except KeyboardInterrupt:
                logger.warning('Stopping... Keyboard stop signal received.')
                return

            except:
                # Ignores unexpected exceptions to reconnect again with the streamer
                logger.exception('Unexpected exception processing streamer events. Sequence: [%d]. Backlog: [%s]',
                                 self.seq, self.streamer.backloger_bid)

    def process_line(self, line):
        try:
            event = json.loads(line)
        except:
            # Raise the exception to stop processing additional events and retry
            # a new connection with the streamer
            logger.exception('Received event with invalid JSON: %s', line)
            raise

            # Create a logging context to use the event sequence as the log transaction id
        with logging.logTransactionContext(event['seq']):
            try:
                self._process_event(event)
                self._inc_seq(event)

                # Notify the idle monitor only when it is clear that the event was sent
                # and the next event is going to be processed
                idle.knock()

            except Exception as e:
                logger.exception('Exception processing event from backlog [%s]: %s',
                                 self.streamer.backloger_bid, event)
                raise

    def _init_seq(self, seq_storage_key):
        seq_storage_folder = self.SEQ_STORAGE_FOLDER_PREFIX + '-' + seq_storage_key
        self.seq_storage_key = '/'.join([seq_storage_folder, self.SEQ_STORAGE_KEY])

        if self.seq is None:
            if self.seq_storage is not None:
                self.seq = self.seq_storage.read(self.seq_storage_key)
                if self.seq is None:
                    msg = 'Cannot load previous sequence number from sequence storage'
                    logger.critical(msg)
                    raise Exception(msg)
                else:
                    self.seq = int(self.seq)
            else:
                self.seq = 0

    def _inc_seq(self, event):
        self.seq = event['seq'] + 1
        if self.seq_storage is not None:
            self.seq_storage.write(self.seq_storage_key, self.seq)

    def _process_event(self, event):
        resolver = self.resolver_class(self.oneapi)
        resolver.resolve(event)

