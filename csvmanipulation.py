import json
import shutil
from enum import Enum
from typing import Optional
from typing import Type

import utils
import constants as c
import csv


class CsvManipulation:

    @staticmethod
    def updateCsvFromUrl(
            url,
            originalCsvPath: str,
            backupOriginalCsvPath: str
    ) -> None:
        try:
            resourceBytes = utils.downloadResource(resourceUrl = url)
            utils.writeBytesToFile(byts = resourceBytes, filename = originalCsvPath)
            utils.writeBytesToFile(byts = resourceBytes, filename = backupOriginalCsvPath)
        except:
            shutil.copyfile(backupOriginalCsvPath, originalCsvPath)

    @staticmethod
    def splitCsvField(originalCsvPath: str,
                      modifiedCsvPath: str,
                      fieldName: str,
                      separator: str,
                      dataType: Type,
                      newFieldsNames: list[str],
                      deleteOldField = False) -> None:
        originalCsvReader = csv.DictReader(open(originalCsvPath), delimiter = ",")

        headers = list(originalCsvReader.fieldnames)

        modifiedCsvWriter = csv.DictWriter(open(modifiedCsvPath, 'w'), fieldnames = headers,
                                           delimiter = ',')

        indexOfFieldToChange = headers.index(fieldName)

        headers.insert(indexOfFieldToChange + 1, newFieldsNames[0])

        startingIndex = indexOfFieldToChange + 1

        for i in range(1, len(newFieldsNames)):
            currentIndex = i + startingIndex
            headers.insert(currentIndex, newFieldsNames[i])

        modifiedCsvWriter.writeheader()

        for row in originalCsvReader:
            newFields = row[fieldName].split(sep = separator)

            for i in range(0, len(newFields)):
                try:
                    newFields[i] = dataType(newFields[i])
                except ValueError:
                    if dataType == int:

                        intField = ''
                        for _, char in enumerate(newFields[i]):
                            if char.isdigit():
                                intField = intField + char

                            else:
                                pass

                        newFields[i] = dataType(intField)

            for i in range(0, len(newFieldsNames)):
                try:
                    row[newFieldsNames[i]] = newFields[i]
                except IndexError:
                    pass

            if deleteOldField:
                del row[fieldName]

            modifiedCsvWriter.writerow(row)

    @staticmethod
    def getTranslatedField(field: str, translatorEnum: Type[Enum]) -> Optional[str]:
        try:
            return translatorEnum[field].value
        except Exception as e:
            print(str(e))
            return None

    @classmethod
    def translateCsvHeader(cls, originalCsvPath: str, translatedCsvPath: str, translatorEnum: Type[Enum]) -> None:
        with open(originalCsvPath) as originalCSV, open(translatedCsvPath,
                                                        'w') as translatedCSV:
            reader = csv.reader(originalCSV)
            writer = csv.writer(translatedCSV)

            # read the header
            header = next(reader)

            # modify the column title

            for i in range(0, len(header)):
                field = header[i]
                translatedField = cls.getTranslatedField(field = field, translatorEnum = translatorEnum)
                header[i] = translatedField if translatedField else field

            # write the new header out
            writer.writerow(header)

            # copy all other rows unmodified
            for row in reader:
                writer.writerow(row)

    @staticmethod
    def createRegionsCoordinatesCsv() -> None:

        if not c.gmapsClient:
            return

        lines = open(c.italyRegionsTxtPath).read().splitlines()

        with open(c.italyRegionsCoordinatesCsvPath, 'w', newline = '') as file:
            writer = csv.writer(file)
            writer.writerow(["region_name", "longitude", "latitude"])

            for line in lines:
                coordinates = utils.getRegionCoordinates(gmaps = c.gmapsClient, region = 'Italia, ' + line)
                writer.writerow([line, coordinates.longitude, coordinates.latitude])

    @staticmethod
    def addRegionCoordinates(originalCsvPath: str, withCoordinatesCsvPath: str, separated: bool = True) -> None:
        originalCsvReader = csv.DictReader(open(originalCsvPath), delimiter = ",")
        italianRegionsCoordinatesDictsList = list(
                csv.DictReader(open(c.italyRegionsCoordinatesCsvPath), delimiter = ','))

        headers = list(originalCsvReader.fieldnames)

        if separated:
            dictWriter = csv.DictWriter(open(withCoordinatesCsvPath, 'w'), fieldnames = headers,
                                        delimiter = ',')
            headers.append('region_longitude')
            headers.append('region_latitude')
        else:
            dictWriter = csv.DictWriter(open(withCoordinatesCsvPath, 'w'),
                                        fieldnames = headers,
                                        delimiter = ',')
            headers.append('region_coordinates')

        dictWriter.writeheader()

        for row in originalCsvReader:
            region = row['region_name']

            for entry in italianRegionsCoordinatesDictsList:
                if entry['region_name'] == region:
                    if separated:
                        row['region_longitude'] = entry['longitude']
                        row['region_latitude'] = entry['latitude']
                    else:
                        row['region_coordinates'] = entry['latitude'] + ', ' + entry['longitude']

            dictWriter.writerow(row)

    @staticmethod
    def csvToJson(csvFilePath: str, jsonFilePath: str) -> None:
        try:
            jsonfile = open(jsonFilePath, 'w')
            reader = csv.DictReader(open(csvFilePath), delimiter = ",")
            data = json.dumps([row for row in reader], indent = 4)
            jsonfile.write(data)
        except Exception as e:
            print(str(e))

    @staticmethod
    def changeCsvColumnNames(originalCsvPath: str,
                             modifiedCsvPath: str,
                             originalColumnNames: list[str],
                             modifiedColumnNames: list[str]) -> None:

        if not originalColumnNames or not modifiedColumnNames:
            return

        if not len(originalColumnNames) == len(modifiedColumnNames):
            return

        with open(originalCsvPath) as originalCSV, open(modifiedCsvPath,
                                                        'w') as modifiedCSV:
            reader = csv.reader(originalCSV)
            writer = csv.writer(modifiedCSV)

            # read the header
            header = next(reader)

            # modify the column title
            for i in range(0, len(originalColumnNames)):
                columnName = originalColumnNames[i]

                for j in range(0, len(header)):
                    if header[j] == columnName:
                        header[j] = modifiedColumnNames[i]

            # write the new header out
            writer.writerow(header)

            # copy all other rows unmodified
            for row in reader:
                writer.writerow(row)

    @staticmethod
    def changeCsvFieldValue(originalCsvPath: str,
                            modifiedCsvPath: str,
                            originalFieldValue: str,
                            modifiedFieldValue: str,
                            columnName: str) -> None:

        originalCsvReader = csv.DictReader(open(originalCsvPath), delimiter = ",")

        headers = originalCsvReader.fieldnames

        modifiedCsvWriter = csv.DictWriter(open(modifiedCsvPath, 'w'), delimiter = ",", fieldnames = headers)

        modifiedCsvWriter.writeheader()

        for row in originalCsvReader:
            if row[columnName] == originalFieldValue:
                row[columnName] = modifiedFieldValue

            modifiedCsvWriter.writerow(row)


class ItalyVaccineRegistryCsvManipulation(CsvManipulation):

    @classmethod
    def splitAgeRangeInCsv(cls) -> None:
        cls.splitCsvField(
                originalCsvPath = c.vaccineRegistryItalyTranslatedCsvPath,
                modifiedCsvPath = c.vaccinesRegistryItalyCsvFinalPath,
                fieldName = 'age_group',
                separator = '-',
                dataType = int,
                newFieldsNames = ['start_age', 'end_age'],
                deleteOldField = False
        )

    @classmethod
    def updateCsv(cls) -> None:
        cls.updateCsvFromUrl(
                url = c.vaccineRegistryItalyCsvUrl,
                originalCsvPath = c.vaccineRegistryItalyCsvPath,
                backupOriginalCsvPath = c.backupVaccineRegistryItalyCsvPath
        )

    @classmethod
    def translateCsvHeaders(cls) -> None:
        cls.translateCsvHeader(
                originalCsvPath = c.vaccineRegistryItalyCsvPath,
                translatedCsvPath = c.vaccineRegistryItalyTranslatedCsvPath,
                translatorEnum = c.italyVaccineRegistryCSVFieldsTranslationEnum
        )

    @classmethod
    def toJson(cls) -> None:
        cls.csvToJson(
                csvFilePath = c.vaccinesRegistryItalyCsvFinalPath,
                jsonFilePath = c.vaccinesRegistryItalyJsonFinalPath
        )

    @classmethod
    def routine(cls) -> None:
        cls.updateCsv()
        cls.translateCsvHeaders()
        shutil.copyfile(c.vaccineRegistryItalyTranslatedCsvPath, c.vaccinesRegistryItalyCsvFinalPath)
        cls.toJson()


class ItalyVaccineDeliveriesCsvManipulation(CsvManipulation):

    @classmethod
    def updateCsv(cls) -> None:
        cls.updateCsvFromUrl(
                url = c.vaccinesDeliveriesItalyCsvUrl,
                originalCsvPath = c.vaccineDeliveriesItalyCsvPath,
                backupOriginalCsvPath = c.backupVaccineDeliveriesItalyCsvPath

        )

    @classmethod
    def translateCsvHeaders(cls) -> None:
        cls.translateCsvHeader(
                originalCsvPath = c.vaccineDeliveriesItalyCsvPath,
                translatedCsvPath = c.vaccineDeliveriesItalyTranslatedCsvPath,
                translatorEnum = c.italyVaccineDeliveriesCSVFieldsTranslationEnum
        )

    @classmethod
    def addRegionCoordinatesToCsv(cls, separated: bool = True) -> None:
        finalCsvPath = c.vaccinesDeliveriesItalyCsvFinalPath if separated else c.vaccinesDeliveriesItalyFinal_mergedCoordinates_CsvPath

        originalCsvPath = c.tempCsvPath

        cls.addRegionCoordinates(
                originalCsvPath = originalCsvPath,
                withCoordinatesCsvPath = finalCsvPath,
                separated = separated
        )

    @classmethod
    def changePfizerPediatricoValues(cls) -> None:
        cls.changeCsvFieldValue(
                originalCsvPath = c.vaccineDeliveriesItalyTranslatedCsvPath,
                modifiedCsvPath = c.tempCsvPath,
                originalFieldValue = "Pfizer Pediatrico",
                modifiedFieldValue = "Pfizer/BioNTech",
                columnName = "supplier"
        )

    @classmethod
    def toJson(cls, withMergedCoordinates = False) -> None:

        if withMergedCoordinates:

            cls.csvToJson(
                    csvFilePath = c.vaccinesDeliveriesItalyFinal_mergedCoordinates_CsvPath,
                    jsonFilePath = c.vaccinesDeliveriesItalyFinal_mergedCoordinates_JsonPath
            )

        else:

            cls.csvToJson(
                    csvFilePath = c.vaccinesDeliveriesItalyCsvFinalPath,
                    jsonFilePath = c.vaccinesDeliveriesItalyJsonFinalPath
            )

    @classmethod
    def routine(cls) -> None:
        cls.updateCsv()
        cls.translateCsvHeaders()

        cls.changePfizerPediatricoValues()
        cls.addRegionCoordinatesToCsv(separated = True)
        cls.toJson(withMergedCoordinates = False)

        cls.addRegionCoordinatesToCsv(separated = False)
        cls.toJson(withMergedCoordinates = True)


class ItalyVaccinationCsvManipulation(CsvManipulation):

    @classmethod
    def updateCsv(cls) -> None:
        cls.updateCsvFromUrl(
                url = c.vaccinationCampaignItalyCsvUrl,
                originalCsvPath = c.vaccinationCampaignItalyCsvPath,
                backupOriginalCsvPath = c.backupVaccinationCampaignCsvPath
        )

    @classmethod
    def translateCsvHeaders(cls) -> None:
        cls.translateCsvHeader(
                originalCsvPath = c.vaccinationCampaignItalyCsvPath,
                translatedCsvPath = c.vaccinationCampaignItalyTranslatedCsvPath,
                translatorEnum = c.italyVaccinesCSVFieldsTranslationEnum
        )

    @classmethod
    def addRegionCoordinatesToCsv(cls, separated: bool = True) -> None:
        finalCsvPath = c.vaccinationCampaignItalyFinalCsvPath if separated else c.vaccinationCampaignItalyFinal_mergedCoordinates_CsvPath
        originalCsvPath = c.tempCsvPath

        cls.addRegionCoordinates(
                originalCsvPath = originalCsvPath,
                withCoordinatesCsvPath = finalCsvPath,
                separated = separated
        )

    @classmethod
    def splitAgeRangeInCsv(cls) -> None:
        cls.splitCsvField(
                originalCsvPath = c.vaccinationCampaignItalyTranslatedCsvPath,
                modifiedCsvPath = c.vaccinationCampaignItalyFinalCsvPath,
                fieldName = 'age_group',
                separator = '-',
                dataType = int,
                newFieldsNames = ['start_age', 'end_age'],
                deleteOldField = False
        )

    @classmethod
    def toJson(cls, withMergedCoordinates = False) -> None:

        if withMergedCoordinates:

            cls.csvToJson(
                    csvFilePath = c.vaccinationCampaignItalyFinal_mergedCoordinates_CsvPath,
                    jsonFilePath = c.vaccinationCampaignItalyFinal_merged_coordinates_JsonPath
            )

        else:

            cls.csvToJson(
                    csvFilePath = c.vaccinationCampaignItalyFinalCsvPath,
                    jsonFilePath = c.vaccinationCampaignItalyFinalJsonPath
            )

    @classmethod
    def changePfizerPediatricoValues(cls) -> None:
        cls.changeCsvFieldValue(
                originalCsvPath = c.vaccinationCampaignItalyTranslatedCsvPath,
                modifiedCsvPath = c.tempCsvPath,
                originalFieldValue = "Pfizer Pediatrico",
                modifiedFieldValue = "Pfizer/BioNTech",
                columnName = "supplier"
        )

    @classmethod
    def routine(cls) -> None:
        cls.updateCsv()
        cls.translateCsvHeaders()

        cls.changePfizerPediatricoValues()
        cls.addRegionCoordinatesToCsv(separated = True)
        cls.toJson(withMergedCoordinates = False)

        cls.addRegionCoordinatesToCsv(separated = False)
        cls.toJson(withMergedCoordinates = True)
