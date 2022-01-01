import configparser
from datetime import datetime
from enum import Enum
from geojson import Point
import googlemaps
from elasticsearch_dsl.connections import connections

vaccinationCampaignItalyCsvUrl = None
vaccinesDeliveriesItalyCsvUrl = None
vaccineRegistryItalyCsvUrl = None

vaccinationCampaignItalyCsvPath = None
backupVaccinationCampaignCsvPath = None
vaccinationCampaignItalyTranslatedCsvPath = None
datasetsFolderPath = 'datasets'
italyOpenDataDatasetsFolderPath = datasetsFolderPath + '/' + 'italy-opendata'

italyRegionsCoordinatesCsvPath = None
italyRegionsTxtPath = None

vaccinationCampaignItalyFinalCsvPath = None
vaccinationCampaignItalyFinalJsonPath = None

vaccinationCampaignItalyFinal_mergedCoordinates_CsvPath = None
vaccinationCampaignItalyFinal_merged_coordinates_JsonPath = None

# ---------

vaccineDeliveriesItalyCsvPath = None
backupVaccineDeliveriesItalyCsvPath = None
vaccineDeliveriesItalyTranslatedCsvPath = None

vaccinesDeliveriesItalyCsvFinalPath = None
vaccinesDeliveriesItalyJsonFinalPath = None

vaccinesDeliveriesItalyFinal_mergedCoordinates_CsvPath = None
vaccinesDeliveriesItalyFinal_mergedCoordinates_JsonPath = None

# ---------

vaccineRegistryItalyCsvPath = None
backupVaccineRegistryItalyCsvPath = None
vaccineRegistryItalyTranslatedCsvPath = None

vaccinesRegistryItalyCsvFinalPath = None
vaccinesRegistryItalyJsonFinalPath = None

vaccinesRegistryItalyCsvFinal_splittedAgeRange_Path = None
vaccinesRegistryItalyJsonFinal_splittedAgeRange_Path = None

# ---------

elasticCloudID = None
elasticApiKeyID = None
elasticApiKeyKey = None

elasticConnection = None

# ---------

tempCsvPath = None

class italyVaccinesCSVFieldsTranslationEnum(Enum):
    index = 'index'
    area = 'area'
    fornitore = 'supplier'
    data_somministrazione = 'administration_date'
    fascia_anagrafica = 'age_group'
    sesso_maschile = 'male_count'
    sesso_femminile = 'female_count'
    prima_dose = 'first_doses'
    seconda_dose = 'second_doses'
    pregressa_infezione = 'post_infection_doses'
    dose_addizionale_booster = 'booster_doses'
    codice_NUTS1 = 'NUTS1_code'
    codice_NUTS2 = 'NUTS2_code'
    codice_regione_ISTAT = 'region_ISTAT_code'
    nome_area = 'region_name'


class italyVaccinesCSVFieldsDataTypesEnum(Enum):
    index = int
    area = str
    supplier = str
    administration_date = datetime
    age_group = str
    male_count = int
    female_count = int
    first_doses = int
    second_doses = int
    post_infection_doses = int
    booster_doses = int
    NUTS1_code = str
    NUTS2_code = str
    region_ISTAT_code = int
    region_name = str
    coordinates = Point


class italyVaccineDeliveriesCSVFieldsTranslationEnum(Enum):
    area = 'area'
    fornitore = 'supplier'
    numero_dosi = 'doses_amount'
    data_consegna = 'delivery_date'
    codice_NUTS1 = 'NUTS1_code'
    codice_NUTS2 = 'NUTS2_code'
    codice_regione_ISTAT = 'region_ISTAT_code'
    nome_area = 'region_name'


class italyVaccineDeliveriesCSVFieldsDataTypesEnum(Enum):
    area = str
    supplier = str
    doses_amount = int
    delivery_date = datetime
    NUTS1_code = str
    NUTS2_code = str
    region_ISTAT_code = int
    region_name = str
    coordinates = Point

class italyVaccineRegistryCSVFieldsTranslationEnum(Enum):
    fascia_anagrafica = 'age_group'
    totale = 'total_administered'
    sesso_maschile = 'male_count'
    sesso_femminile = 'female_count'
    prima_dose = 'first_doses'
    seconda_dose = 'second_doses'
    pregressa_infezione = 'post_infection_doses'
    dose_addizionale_booster = 'booster_doses'
    ultimo_aggiornamento = 'last_update'





googleMapsAPIKEY = None

gmapsClient = None


def setupConstants():
    config = configparser.ConfigParser()
    config.read('setup.ini')

    # ------

    pathsConfigDict = config['RESOURCES-URLS']
    global vaccinationCampaignItalyCsvUrl
    global vaccinesDeliveriesItalyCsvUrl
    global vaccineRegistryItalyCsvUrl

    vaccinationCampaignItalyCsvUrl = pathsConfigDict['vaccination_campaign_italy_resource_url']
    vaccinesDeliveriesItalyCsvUrl = pathsConfigDict['vaccine_deliveries_italy_resource_url']
    vaccineRegistryItalyCsvUrl = pathsConfigDict['vaccine_registry_italy_resource_url']

    # ------

    pathsConfigDict = config['PATHS-ITALY-REGIONS']
    global italyRegionsCoordinatesCsvPath
    global italyRegionsTxtPath

    italyRegionsCoordinatesCsvPath = pathsConfigDict['italy_regions_coordinates_csv_path']
    italyRegionsTxtPath = pathsConfigDict['italy_regions_txt_path']

    # ------

    pathsConfigDict = config['PATHS-ITALY-VACCINATIONS']

    global vaccinationCampaignItalyCsvPath
    global backupVaccinationCampaignCsvPath
    global vaccinationCampaignItalyTranslatedCsvPath
    global vaccinationCampaignItalyFinalCsvPath
    global vaccinationCampaignItalyFinalJsonPath
    global vaccinationCampaignItalyFinal_mergedCoordinates_CsvPath
    global vaccinationCampaignItalyFinal_merged_coordinates_JsonPath

    vaccinationCampaignItalyCsvPath = pathsConfigDict['italy_vaccinations_csv_path']
    backupVaccinationCampaignCsvPath = pathsConfigDict['backup_italy_vaccinations_csv_path']
    vaccinationCampaignItalyTranslatedCsvPath = pathsConfigDict['italy_vaccinations_csv_translated_path']

    vaccinationCampaignItalyFinalCsvPath = pathsConfigDict['italy_vaccinations_csv_final_path']
    vaccinationCampaignItalyFinalJsonPath = pathsConfigDict['italy_vaccinations_json_final_path']

    vaccinationCampaignItalyFinal_mergedCoordinates_CsvPath = pathsConfigDict[
        'italy_vaccinations_merged_coordinates_csv_final_path']
    vaccinationCampaignItalyFinal_merged_coordinates_JsonPath = pathsConfigDict[
        'italy_vaccinations_merged_coordinates_json_final_path']

    # ------

    pathsConfigDict = config['GOOGLE-API']

    global googleMapsAPIKEY
    global gmapsClient
    googleMapsAPIKEY = pathsConfigDict['google_maps_api_key']
    gmapsClient = googlemaps.Client(key = googleMapsAPIKEY)

    # -------

    pathsConfigDict = config['ELASTIC-API']

    global elasticCloudID
    global elasticApiKeyID
    global elasticApiKeyKey

    elasticCloudID = pathsConfigDict['cloud_id']
    elasticApiKeyID = pathsConfigDict['apikey_id']
    elasticApiKeyKey = pathsConfigDict['apikey_key']

    # -------

    global elasticConnection
    elasticConnection = connections.create_connection(cloud_id = elasticCloudID,
                                                      api_key = (elasticApiKeyID, elasticApiKeyKey))

    # -------

    pathsConfigDict = config['PATHS-ITALY-VACCINES-DELIVERY']

    global vaccineDeliveriesItalyCsvPath
    global backupVaccineDeliveriesItalyCsvPath
    global vaccineDeliveriesItalyTranslatedCsvPath
    global vaccinesDeliveriesItalyCsvFinalPath
    global vaccinesDeliveriesItalyJsonFinalPath
    global vaccinesDeliveriesItalyFinal_mergedCoordinates_CsvPath
    global vaccinesDeliveriesItalyFinal_mergedCoordinates_JsonPath

    vaccineDeliveriesItalyCsvPath = pathsConfigDict['italy_vaccine_deliveries_csv_path']
    backupVaccineDeliveriesItalyCsvPath = pathsConfigDict['backup_italy_vaccine_deliveries_csv_path']
    vaccineDeliveriesItalyTranslatedCsvPath = pathsConfigDict['italy_vaccine_deliveries_translated_path']
    vaccinesDeliveriesItalyCsvFinalPath = pathsConfigDict['italy_vaccine_deliveries_csv_final_path']
    vaccinesDeliveriesItalyJsonFinalPath = pathsConfigDict['italy_vaccine_deliveries_json_final_path']
    vaccinesDeliveriesItalyFinal_mergedCoordinates_CsvPath = pathsConfigDict[
        'italy_vaccine_deliveries_merged_coordinates_csv_final_path']
    vaccinesDeliveriesItalyFinal_mergedCoordinates_JsonPath = pathsConfigDict[
        'italy_vaccine_deliveries_merged_coordinates_json_final_path']

    # -------

    pathsConfigDict = config['PATHS-ITALY-VACCINE-REGISTRY']

    global vaccineRegistryItalyCsvPath
    global backupVaccineRegistryItalyCsvPath
    global vaccineRegistryItalyTranslatedCsvPath
    global vaccinesRegistryItalyCsvFinalPath
    global vaccinesRegistryItalyJsonFinalPath
    global vaccinesRegistryItalyCsvFinal_splittedAgeRange_Path
    global vaccinesRegistryItalyJsonFinal_splittedAgeRange_Path

    vaccineRegistryItalyCsvPath = pathsConfigDict['italy_vaccine_registry_csv_path']
    backupVaccineRegistryItalyCsvPath = pathsConfigDict['backup_italy_vaccine_registry_csv_path']
    vaccineRegistryItalyTranslatedCsvPath = pathsConfigDict['italy_vaccine_registry_translated_path']
    vaccinesRegistryItalyCsvFinalPath = pathsConfigDict['italy_vaccine_registry_csv_final_path']
    vaccinesRegistryItalyJsonFinalPath = pathsConfigDict['italy_vaccine_registry_json_final_path']
    vaccinesRegistryItalyCsvFinal_splittedAgeRange_Path = pathsConfigDict['italy_vaccine_registry_splitted_agerange_csv_path']
    vaccinesRegistryItalyJsonFinal_splittedAgeRange_Path = pathsConfigDict['italy_vaccine_registry_splitted_agerange_json_path']

    # ----

    pathsConfigDict = config['TEMP-FILES']

    global tempCsvPath

    tempCsvPath = pathsConfigDict['temp_csv']


