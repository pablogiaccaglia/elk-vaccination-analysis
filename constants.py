import configparser

vaccinationCampaignItalyCsvUrl = "https://raw.githubusercontent.com/italia/covid19-opendata-vaccini/master/dati/somministrazioni-vaccini-latest.csv"

vaccinationCampaignItalyCsvPath = None
backupVaccinationCampaignCsvPath = None
datasetsFolderPath = 'datasets'

def setupConstants():
    config = configparser.ConfigParser()
    config.read('setup.ini')
    pathsConfigDict = config['PATHS']

    global vaccinationCampaignItalyCsvPath
    global backupVaccinationCampaignCsvPath
    vaccinationCampaignItalyCsvPath = pathsConfigDict['italy_vaccinations_csv_path']
    backupVaccinationCampaignCsvPath = pathsConfigDict['backup_italy_vaccinations_csv_path']