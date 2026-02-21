# -*- coding:utf-8 -*-

from .. import logger
from .freespacebase import FreeSpaceConditionBase
from autoremovetorrents.compatibility.disk_usage_ import disk_usage_
from ..util.convertbytes import convert_bytes

class FreeSpaceCondition(FreeSpaceConditionBase):
    def __init__(self, settings):
        FreeSpaceConditionBase.__init__(self, settings)
        self._path = settings['path']
        self._logger = logger.Logger.register(__name__)

    def apply(self, client_status, torrents):
        du = disk_usage_(self._path)
        free_space = du['free']
        self._logger.info(
            'Local disk usage for %s: total=%s, used=%s, free=%s (min required: %s)' % (
                self._path,
                convert_bytes(du['total']),
                convert_bytes(du['used']),
                convert_bytes(free_space),
                convert_bytes(self._min),
            )
        )
        FreeSpaceConditionBase.apply(self, free_space, torrents)
