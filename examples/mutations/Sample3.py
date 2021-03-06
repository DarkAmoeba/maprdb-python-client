"""Following example works with Python Client"""
from mapr.ojai.ojai_query.QueryOp import QueryOp
from mapr.ojai.storage.ConnectionFactory import ConnectionFactory
"""Sample for check_and_update operation"""

# create a connection
connection_string = "localhost:5678?auth=basic;user=mapr;password=mapr;" \
          "ssl=true;" \
          "sslCA=/opt/mapr/conf/ssl_truststore.pem;" \
          "sslTargetNameOverride=node.mapr.com"
connection = ConnectionFactory.get_connection(connection_str=connection_string)

# Get a store and assign it as a DocumentStore object
if connection.is_store_exists(store_path='/update_store1'):
    document_store = connection.get_store(store_path='/update_store1')
else:
    document_store = connection.create_store(store_path='/update_store1')

# Create a condition
condition = connection.new_condition()\
    .and_()\
    .equals_('name', 'John')\
    .is_('age', QueryOp.GREATER_OR_EQUAL, 35).close().build()

# Create a document mutation
doc_mutation = connection.new_mutation().set_or_replace('address.city', 'NY')

# Execute operation
document_store.check_and_update('user0000', condition, doc_mutation)

# Fetch record with _id field 'user0000'
document = document_store.find_by_id('user0000')

print(document)
