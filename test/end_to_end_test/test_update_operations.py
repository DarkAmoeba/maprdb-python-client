#!/usr/bin/env python
from __future__ import unicode_literals
from __future__ import print_function
from __future__ import division
from __future__ import absolute_import

from future import standard_library
standard_library.install_aliases()
from builtins import *
from mapr.ojai.document.OJAIDocumentMutation import OJAIDocumentMutation
from mapr.ojai.storage.ConnectionFactory import ConnectionFactory
from test.test_utils.constants import CONNECTION_STR, CONNECTION_OPTIONS, DICT_STREAM_UPDATE

try:
    import unittest2 as unittest
except ImportError:
    import unittest


class UpdateTest(unittest.TestCase):
    store_name = '/update-test-store1'

    def test_update_document_set(self):
        connection = ConnectionFactory.get_connection(connection_str=CONNECTION_STR,
                                                      options=CONNECTION_OPTIONS)

        if connection.is_store_exists(store_path=UpdateTest.store_name):
            connection.delete_store(store_path=UpdateTest.store_name)

        document_store = connection.create_store(store_path=UpdateTest.store_name)

        for doc in DICT_STREAM_UPDATE:
            document = connection.new_document(dictionary=doc)
            document_store.insert_or_replace(doc=document)

        self.assertEqual({'_id': 'id08', 'test_int': 51, 'test_str': 'strstr',
                          'test_dict': {'test_int': 5}},
                         document_store.find_by_id('id08'))
        mutation = OJAIDocumentMutation().set('a.b.c', 50)
        document_store.update('id08', mutation)
        self.assertEqual({'_id': 'id08', 'test_int': 51, 'test_str': 'strstr',
                          'test_dict': {'test_int': 5},
                          'a': {'b': {'c': 50}}},
                         document_store.find_by_id('id08'))

    def test_update_document_set_error(self):
        connection = ConnectionFactory.get_connection(connection_str=CONNECTION_STR,
                                                      options=CONNECTION_OPTIONS)

        if connection.is_store_exists(store_path=UpdateTest.store_name):
            document_store = connection.get_store(store_path=UpdateTest.store_name)
        else:
            document_store = connection.create_store(store_path=UpdateTest.store_name)
        self.assertEqual({'_id': 'id11', 'test_int': 51, 'test_str': 'strstr',
                          'test_dict': {'test_int': 5}},
                         document_store.find_by_id('id11'))
        mutation = OJAIDocumentMutation().set_or_replace('test_int', 50)
        document_store.update('id11', mutation)
        self.assertEqual({'_id': 'id11', 'test_int': 50, 'test_str': 'strstr',
                          'test_dict': {'test_int': 5}},
                         document_store.find_by_id('id11'))

    def test_update_document_put(self):
        connection = ConnectionFactory.get_connection(connection_str=CONNECTION_STR,
                                                      options=CONNECTION_OPTIONS)

        if connection.is_store_exists(store_path=UpdateTest.store_name):
            document_store = connection.get_store(store_path=UpdateTest.store_name)
        else:
            document_store = connection.create_store(store_path=UpdateTest.store_name)

        self.assertEqual({'_id': 'id06', 'test_int': 51, 'test_str': 'strstr'},
                         document_store.find_by_id('id06'))
        mutation = OJAIDocumentMutation().set_or_replace('test_int', 50)
        document_store.update('id06', mutation)
        self.assertEqual({'_id': 'id06', 'test_int': 50, 'test_str': 'strstr'},
                         document_store.find_by_id('id06'))
        document_store.update('id06', {"$put": {"a.x": 1}})
        self.assertEqual({'_id': 'id06', 'test_int': 50, 'test_str': 'strstr', 'a': {'x': 1}},
                         document_store.find_by_id('id06'))

    def test_update_document_increment_decrement(self):
        connection = ConnectionFactory.get_connection(connection_str=CONNECTION_STR,
                                                      options=CONNECTION_OPTIONS)

        if connection.is_store_exists(store_path=UpdateTest.store_name):
            document_store = connection.get_store(store_path=UpdateTest.store_name)
        else:
            document_store = connection.create_store(store_path=UpdateTest.store_name)

        self.assertEqual({'_id': 'id07', 'test_int': 51, 'test_str': 'strstr'},
                         document_store.find_by_id('id07'))
        mutation = OJAIDocumentMutation().increment('test_int', 3)
        document_store.update('id07', mutation)
        self.assertEqual({'_id': 'id07', 'test_int': 54, 'test_str': 'strstr'},
                         document_store.find_by_id('id07'))
        document_store.increment('id07', 'test_int', -3)
        self.assertEqual({'_id': 'id07', 'test_int': 51, 'test_str': 'strstr'},
                         document_store.find_by_id('id07'))
        document_store.update('id07', OJAIDocumentMutation().decrement('test_int', 1))
        self.assertEqual({'_id': 'id07', 'test_int': 50, 'test_str': 'strstr'},
                         document_store.find_by_id('id07'))

    def test_update_document_delete(self):
        connection = ConnectionFactory.get_connection(connection_str=CONNECTION_STR,
                                                      options=CONNECTION_OPTIONS)

        if connection.is_store_exists(store_path=UpdateTest.store_name):
            document_store = connection.get_store(store_path=UpdateTest.store_name)
        else:
            document_store = connection.create_store(store_path=UpdateTest.store_name)

        self.assertEqual({'_id': "id01", 'test_int': 51, 'test_str': 'strstr'},
                         document_store.find_by_id('id01'))
        mutation = OJAIDocumentMutation().delete('test_int')
        document_store.update('id01', mutation)
        self.assertEqual({'_id': "id01", 'test_str': 'strstr'},
                         document_store.find_by_id('id01'))

    def test_update_document_append(self):
        connection = ConnectionFactory.get_connection(connection_str=CONNECTION_STR,
                                                      options=CONNECTION_OPTIONS)

        if connection.is_store_exists(store_path=UpdateTest.store_name):
            document_store = connection.get_store(store_path=UpdateTest.store_name)
        else:
            document_store = connection.create_store(store_path=UpdateTest.store_name)

        self.assertEqual({'_id': 'id09', 'test_int': 51, 'test_str': 'strstr',
                          'test_list': [5, 6]},
                         document_store.find_by_id('id09'))
        mutation = OJAIDocumentMutation().append('test_list', [{'name': 'Jo'}, 7, 8])
        document_store.update('id09', mutation)
        self.assertEqual({'_id': 'id09', 'test_int': 51, 'test_str': 'strstr',
                          'test_list': [5, 6, {'name': 'Jo'}, 7, 8]},
                         document_store.find_by_id('id09'))

    def test_update_document_merge(self):
        connection = ConnectionFactory.get_connection(connection_str=CONNECTION_STR,
                                                      options=CONNECTION_OPTIONS)

        if connection.is_store_exists(store_path=UpdateTest.store_name):
            document_store = connection.get_store(store_path=UpdateTest.store_name)
        else:
            document_store = connection.create_store(store_path=UpdateTest.store_name)
        self.assertEqual({'_id': 'id11', 'test_int': 51, 'test_str': 'strstr',
                          'test_dict': {'test_int': 5}},
                         document_store.find_by_id('id11'))
        mutation = OJAIDocumentMutation().merge('test_dict',
                                                {'d': 55, 'g': 'text'})
        document_store.update('id11', mutation)
        self.assertEqual({'_id': 'id11', 'test_int': 51, 'test_str': 'strstr',
                          'test_dict': {'test_int': 5, 'd': 55, 'g': 'text'}},
                         document_store.find_by_id('id11'))

    def test_check_and_update(self):
        connection = ConnectionFactory.get_connection(connection_str=CONNECTION_STR,
                                                      options=CONNECTION_OPTIONS)

        if connection.is_store_exists(store_path=UpdateTest.store_name):
            document_store = connection.get_store(store_path=UpdateTest.store_name)
        else:
            document_store = connection.create_store(store_path=UpdateTest.store_name)
        self.assertEqual({'_id': 'id02', 'mystr': 'str', 'test_int': 51,
                          'test_str': 'strstr'},
                         document_store.find_by_id('id02'))
        mutation = OJAIDocumentMutation().set_or_replace('new_field',
                                                         {'d': 55, 'g': 'text'})
        from mapr.ojai.ojai_query.OJAIQueryCondition import OJAIQueryCondition
        false_condition = OJAIQueryCondition().equals_('test_str', 'rtsrts').close().build()
        self.assertFalse(document_store.check_and_update('id02', mutation=mutation, query_condition=false_condition))
        self.assertEqual({'_id': 'id02', 'mystr': 'str', 'test_int': 51,
                          'test_str': 'strstr'},
                         document_store.find_by_id('id02'))
        true_condition = OJAIQueryCondition().equals_('test_str', 'strstr').close().build()
        document_store.check_and_update('id02', mutation=mutation, query_condition=true_condition)
        self.assertEqual({'_id': 'id02', 'mystr': 'str', 'test_int': 51,
                          'test_str': 'strstr', 'new_field': {'d': 55, 'g': 'text'}},
                         document_store.find_by_id('id02'))

    def test_update_bytearray(self):
        connection = ConnectionFactory.get_connection(connection_str=CONNECTION_STR,
                                                      options=CONNECTION_OPTIONS)
        if connection.is_store_exists(store_path=UpdateTest.store_name):
            document_store = connection.get_store(store_path=UpdateTest.store_name)
        else:
            document_store = connection.create_store(store_path=UpdateTest.store_name)
        doct = {'_id': 'Hty', 'oho': 55}
        doc = connection.new_document(dictionary=doct)
        document_store.insert_or_replace(doc)
        mut = OJAIDocumentMutation()
        mut.set_or_replace('b', bytearray(b'\x06\x06'))
        document_store.update(_id='Hty', mutation=mut)
        res = document_store.find_by_id(_id='Hty')
        self.assertEqual({'_id': 'Hty', 'oho': 55, 'b': bytearray(b'\x06\x06')}, res)


if __name__ == '__main__':
    test_classes_to_run = [UpdateTest]
    loader = unittest.TestLoader()
    suites_list = []
    for test_class in test_classes_to_run:
        suite = loader.loadTestsFromTestCase(test_class)
        suites_list.append(suite)

    big_suite = unittest.TestSuite(suites_list)

    runner = unittest.TextTestRunner()
    results = runner.run(big_suite)
