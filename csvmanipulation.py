import json
import shutil
from typing import Optional
import pipeline
import constants as c
import csv
import utils
import pandas as pd

def updateItalyVaccinationCsv() -> None:
    try:
        if not c.vaccinationCampaignItalyCsvPath:
            name = pipeline.getFileNameFromUrl(resourceUrl = c.vaccinationCampaignItalyCsvUrl)
            c.vaccinationCampaignItalyCsvPath = c.italyOpenDataDatasetsFolderPath + '/original' + '/' + name
            c.backupVaccinationCampaignCsvPath = c.italyOpenDataDatasetsFolderPath + '/original' + '/' + "BACKUP-" + name

        resourceBytes = pipeline.downloadResource(resourceUrl = c.vaccinationCampaignItalyCsvUrl)
        pipeline.writeBytesToFile(byts = resourceBytes, filename = c.vaccinationCampaignItalyCsvPath)
        pipeline.writeBytesToFile(byts = resourceBytes, filename = c.backupVaccinationCampaignCsvPath)
    except:
        shutil.copyfile(c.backupVaccinationCampaignCsvPath, c.vaccinationCampaignItalyCsvPath)

def getTranslatedField(field: str) -> Optional[str]:
    try:
        return c.italyVaccinesCSVFieldsTranslationEnum[field].value
    except Exception as e:
        print(str(e))
        return None

def translateItalyVaccinationCsv() -> None:
    with open(c.vaccinationCampaignItalyCsvPath) as originalCSV, open(c.vaccinationCampaignItalyCsvTranslatedCsvPath,
                                                                      'w') as translatedCSV:
        reader = csv.reader(originalCSV)
        writer = csv.writer(translatedCSV)

        # read the header
        header = next(reader)

        # modify the column title

        for i in range(0, len(header)):
            field = header[i]
            translatedField = getTranslatedField(field = field)
            header[i] = translatedField if translatedField else field

        # write the new header out
        writer.writerow(header)

        # copy all other rows unmodified
        for row in reader:
            writer.writerow(row)

def createRegionsCoordinatesCsv() -> None:
    lines = open(c.italyRegionsTxtPath).read().splitlines()

    with open(c.italyRegionsCoordinatesCsvPath, 'w', newline = '') as file:
        writer = csv.writer(file)
        writer.writerow(["region_name", "longitude", "latitude"])

        for line in lines:
            coordinates = utils.getRegionCoordinates(gmaps = c.gmapsClient, region = 'Italia, ' + line)
            writer.writerow([line, coordinates.longitude,  coordinates.latitude])

def addRegionCoordinatesToCsv() -> None:

    vaccinationDictReader = csv.DictReader(open(c.vaccinationCampaignItalyCsvTranslatedCsvPath), delimiter = ",")
    italianRegionsCoordinatesDictsList = list(csv.DictReader(open(c.italyRegionsCoordinatesCsvPath), delimiter = ','))

    headers = list(vaccinationDictReader.fieldnames)

    headers.append('region_longitude')
    headers.append('region_latitude')

    dictWriter = csv.DictWriter(open(c.vaccinationCampaignItalyFinalCsvPath, 'w'), fieldnames = headers, delimiter = ',')
    dictWriter.writeheader()

    for row in vaccinationDictReader:
        region = row['region_name']

        for entry in italianRegionsCoordinatesDictsList:
            if entry['region_name'] == region:
                row['region_longitude'] = entry['longitude']
                row['region_latitude'] = entry['latitude']

        dictWriter.writerow(row)

def csvToJson(csvFilePath: str, jsonFilePath: str) -> None:

    try:
        jsonfile = open(jsonFilePath, 'w')
        reader = csv.DictReader(open(csvFilePath), delimiter = ",")
        data = json.dumps([row for row in reader], indent = 4)
        jsonfile.write(data)
    except Exception as e:
        print(str(e))




