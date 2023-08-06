from c2cwsgiutils import stats
from itertools import chain, groupby, starmap

from tilecloud import TileStore


class MultiTileStore(TileStore):
    def __init__(self, stores, stats_name, default_layer_name=None, **kwargs):
        TileStore.__init__(self, **kwargs)
        self._stores = stores
        self._stats_name = stats_name
        self._default_store = self._stores.get(default_layer_name)

    def _get_store(self, layer):
        return self._stores.get(layer, self._default_store)

    def __contains__(self, tile):
        """
        Return true if this store contains ``tile``.

        :param tile: Tile
        :type tile: :class:`Tile`

        :rtype: bool

        """
        layer = _get_layer(tile)
        with stats.timer_context([self._stats_name, layer, 'contains']):
            return tile in self._get_store(layer)

    def delete_one(self, tile):
        """
        Delete ``tile`` and return ``tile``.

        :param tile: Tile
        :type tile: :class:`Tile` or ``None``

        :rtype: :class:`Tile` or ``None``

        """
        layer = _get_layer(tile)
        with stats.timer_context([self._stats_name, layer, 'delete_one']):
            return self._get_store(layer).delete_one(tile)

    @staticmethod
    def list():
        """
        Generate all the tiles in the store, but without their data.

        :rtype: iterator

        """
        # Too dangerous to list all tiles in all stores. Return an empty iterator instead
        while False:
            yield

    def put_one(self, tile):
        """
        Store ``tile`` in the store.

        :param tile: Tile
        :type tile: :class:`Tile` or ``None``

        :rtype: :class:`Tile` or ``None``

        """
        layer = _get_layer(tile)
        with stats.timer_context([self._stats_name, layer, 'put_one']):
            return self._get_store(layer).put_one(tile)

    def get_one(self, tile):
        """
        Add data to ``tile``, or return ``None`` if ``tile`` is not in the store.

        :param tile: Tile
        :type tile: :class:`Tile` or ``None``

        :rtype: :class:`Tile` or ``None``

        """
        layer = _get_layer(tile)
        with stats.timer_context([self._stats_name, layer, 'get_one']):
            return self._get_store(layer).get_one(tile)

    def get(self, tiles):
        def apply(layer, tiles):
            with stats.timer_context([self._stats_name, layer, 'get']):
                return self._get_store(layer).get(tiles)

        return chain.from_iterable(starmap(apply, groupby(tiles, _get_layer)))

    def put(self, tiles):
        def apply(layer, tiles):
            with stats.timer_context([self._stats_name, layer, 'put']):
                return self._get_store(layer).put(tiles)

        return chain.from_iterable(starmap(apply, groupby(tiles, _get_layer)))

    def delete(self, tiles):
        def apply(layer, tiles):
            with stats.timer_context([self._stats_name, layer, 'delete']):
                return self._get_store(layer).delete(tiles)

        return chain.from_iterable(starmap(apply, groupby(tiles, _get_layer)))


def _get_layer(tile):
    if tile:
        return tile.metadata.get('layer')
    else:
        return None
