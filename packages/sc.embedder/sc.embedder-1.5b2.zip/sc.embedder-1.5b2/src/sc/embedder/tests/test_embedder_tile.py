# -*- coding: utf-8 -*-
"""Tests in this module are executed only if collective.cover is installed."""
from sc.embedder.testing import HAS_COVER
from sc.embedder.testing import INTEGRATION_TESTING

import unittest


if HAS_COVER:
    from collective.cover.tests.base import TestTileMixin
    from sc.embedder.tiles.embedder import EmbedderTile
    from sc.embedder.tiles.embedder import IEmbedderTile
else:
    class TestTileMixin:
        pass

    def test_suite():
        return unittest.TestSuite()


class EmbedderTileTestCase(TestTileMixin, unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        super(EmbedderTileTestCase, self).setUp()
        self.tile = EmbedderTile(self.cover, self.request)
        self.tile.__name__ = u'sc.embedder'
        self.tile.id = u'test'

    @unittest.expectedFailure  # FIXME: raises BrokenImplementation
    def test_interface(self):
        self.interface = IEmbedderTile
        self.klass = EmbedderTile
        super(EmbedderTileTestCase, self).test_interface()

    def test_default_configuration(self):
        self.assertTrue(self.tile.is_configurable)
        self.assertTrue(self.tile.is_editable)
        self.assertTrue(self.tile.is_droppable)

    def test_accepted_content_types(self):
        self.assertEqual(self.tile.accepted_ct(), ['sc.embedder'])
