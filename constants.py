import configparser
from datetime import datetime
from enum import Enum

import googlemaps

vaccinationCampaignItalyCsvUrl = "https://raw.githubusercontent.com/italia/covid19-opendata-vaccini/master/dati/somministrazioni-vaccini-latest.csv"

vaccinationCampaignItalyCsvPath = None
backupVaccinationCampaignCsvPath = None
vaccinationCampaignItalyCsvTranslatedCsvPath = None
datasetsFolderPath = 'datasets'
italyOpenDataDatasetsFolderPath = datasetsFolderPath + '/' + 'italy-opendata'
italyRegionsCoordinatesCsvPath = None
italyRegionsTxtPath = None
vaccinationCampaignItalyFinalCsvPath = None
vaccinationCampaignItalyFinalJsonPath = None


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


class italyVaccinesCSVFieldsDataTypes(Enum):
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


googleMapsAPIKEY = None

gmapsClient = None


def setupConstants():
    config = configparser.ConfigParser()
    config.read('setup.ini')
    pathsConfigDict = config['PATHS']

    global vaccinationCampaignItalyCsvPath
    global backupVaccinationCampaignCsvPath
    global vaccinationCampaignItalyCsvTranslatedCsvPath
    global italyRegionsCoordinatesCsvPath
    global italyRegionsTxtPath
    global vaccinationCampaignItalyFinalCsvPath
    global vaccinationCampaignItalyFinalJsonPath

    vaccinationCampaignItalyCsvPath = pathsConfigDict['italy_vaccinations_csv_path']
    backupVaccinationCampaignCsvPath = pathsConfigDict['backup_italy_vaccinations_csv_path']
    vaccinationCampaignItalyCsvTranslatedCsvPath = pathsConfigDict['italy_vaccinations_csv_translated_path']
    italyRegionsCoordinatesCsvPath = pathsConfigDict['italy_regions_coordinates_csv_path']
    italyRegionsTxtPath = pathsConfigDict['italy_regions_txt_path']
    vaccinationCampaignItalyFinalCsvPath = pathsConfigDict['italy_vaccinations_csv_final']
    vaccinationCampaignItalyFinalJsonPath = pathsConfigDict['italy_vaccinations_json_final']

    pathsConfigDict = config['GOOGLE-API']
    global googleMapsAPIKEY
    global gmapsClient
    googleMapsAPIKEY = pathsConfigDict['google_maps_api_key']
    gmapsClient = googlemaps.Client(key = googleMapsAPIKEY)
