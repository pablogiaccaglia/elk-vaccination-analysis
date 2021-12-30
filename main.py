from elasticsearch import Elasticsearch
import configparser
import constants
import csvmanipulation

config = configparser.ConfigParser()
config.read('setup.ini')

client = Elasticsearch(
        cloud_id = config['DEFAULT']['cloud_id'],
        api_key = (config['DEFAULT']['apikey_id'], config['DEFAULT']['apikey_key']),
)

# print(client.info())

constants.setupConstants()
# updateItalyVaccinationCsv()
# translateItalyVaccinationCsv()
# csvmanipulation.createRegionsCoordinatesCsv()
# csvmanipulation.addRegionCoordinatesToCsv()
csvmanipulation.csvToJson(
        csvFilePath = constants.vaccinationCampaignItalyFinalCsvPath,
        jsonFilePath = constants.vaccinationCampaignItalyFinalJsonPath
)