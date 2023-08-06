"""Tests for model module."""

import unittest
import logging
import vsmlib
from vsmlib.model import Model, ModelDense
logging.basicConfig(level=logging.DEBUG)


class Tests(unittest.TestCase):

    def test_create(self):
        model = ModelDense()
        self.assertIsInstance(model, Model)

    def test_load_plain_text(self):
        model = ModelDense()
        path = "./test/data/embeddings/text/plain_with_file_header/emb.txt"
        model.load_from_text(path)
        print(model.matrix.shape)

    def test_load(self):
        path = "./test/data/embeddings/text/plain_with_file_header/"
        model = vsmlib.model.load_from_dir(path)
        self.assertIsInstance(model, Model)
        model.vocabulary.get_id("apple")
        print(model.name)

    def test_save(self):
        path = "./test/data/embeddings/text/plain_with_file_header/"
        model = vsmlib.model.load_from_dir(path)
        path_save = "/tmp/vsmlib/saved"
        model.save_to_dir(path_save)
        model = vsmlib.model.load_from_dir(path_save)
        print(model.matrix.shape)

    def test_load_numpy(self):
        path = "./test/data/embeddings/npy/"
        model = vsmlib.model.load_from_dir(path)
        self.assertIsInstance(model, Model)
        model.vocabulary.get_id("apple")
        # todo make sure to check vocab
