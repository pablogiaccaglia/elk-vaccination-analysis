from elasticsearch import Elasticsearch
import configparser

config = configparser.ConfigParser()
config.read('setup.ini')

client = Elasticsearch(
    cloud_id=config['DEFAULT']['cloud_id'],
    api_key=(config['DEFAULT']['apikey_id'], config['DEFAULT']['apikey_key']),
)

print(client.info())



