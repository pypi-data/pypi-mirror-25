import os
import json
import logging
from betfairlightweight.filters import (
    streaming_market_filter,
    streaming_market_data_filter,
)

from ..utils import create_short_uuid

logger = logging.getLogger(__name__)


class BaseRecorder:
    """Base recorder which connects to all
    markets by default.
    """

    NAME = 'BASE_RECORDER'

    def __init__(self, storage_engine, market_filter=None, market_data_filter=None):
        self.storage_engine = storage_engine
        self.market_filter = market_filter or streaming_market_filter()
        self.market_data_filter = market_data_filter or streaming_market_data_filter(
            fields=[
                'EX_ALL_OFFERS', 'EX_TRADED', 'EX_TRADED_VOL', 'EX_LTP', 'EX_MARKET_DEF', 'SP_TRADED', 'SP_PROJECTED'
            ]
        )
        self.stream_id = create_short_uuid()
        self.live_markets = []  # list of markets to be processed
        self._setup()
        logger.info('Recorder created %s' % self.stream_id)

    def __call__(self, market_books, publish_time):
        """Checks market using market book parameters
        function then passes market_book to be processed.

        :param market_books: List of Market Book objects
        :param publish_time: Publish time of market book
        """
        for market_book in market_books:
            market_id = market_book.get('id')
            self.check_market_book(market_id, market_book)
            if market_id in self.live_markets:
                self.process_market_book(market_book, publish_time)

    def check_market_book(self, market_id, market_book):
        """Logic used to decide if market_book should
        be processed

        :param market_id: Market id
        :param market_book: Market Book object
        """
        if market_id not in self.live_markets:
            self.live_markets.append(market_id)

    def process_market_book(self, market_book, publish_time):
        """Function that processes market book

        :param market_book: Market Book object
        :param publish_time: Publish time of market book
        """
        raise NotImplementedError

    def on_market_closed(self, market_book):
        """Function run when market is closed.
        """
        market_id = market_book.get('id')
        market_definition = market_book.get('marketDefinition')
        logger.info('Closing market %s' % market_id)
        self.storage_engine(market_id, market_definition, self.stream_id)

    def _setup(self):
        """Create stream folder in /tmp  # todo
        """
        directory = os.path.join('/tmp', self.stream_id)
        if not os.path.exists(directory):
            os.makedirs(directory)

    def __str__(self):
        return '<%s>' % self.NAME


class StreamRecorder(BaseRecorder):
    """Data recorder, records stream data
    to /tmp/market_id
    """

    NAME = 'STREAM_RECORDER'

    def process_market_book(self, market_book, publish_time):
        filename = '%s' % market_book.get('id')
        file_directory = os.path.join('/tmp', self.stream_id, filename)

        with open(file_directory, 'a') as outfile:
            outfile.write(
                json.dumps({
                    "op": "mcm",
                    "clk": None,
                    "pt": publish_time,
                    "mc": [market_book]
                }) + '\n'
            )

        if 'marketDefinition' in market_book and market_book['marketDefinition']['status'] == 'CLOSED':
            self.on_market_closed(market_book)
