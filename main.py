import constants
from csvmanipulation import (
    ItalyVaccinationCsvManipulation,
    ItalyVaccineRegistryCsvManipulation,
    ItalyVaccineDeliveriesCsvManipulation
)

import elastichutils


def populateDatabase() -> None:
    elastichutils.createVaccinationCampaignIndex(connection = constants.elasticConnection)
    elastichutils.uploadCSVToElastic(
            csvPath = constants.vaccinationCampaignItalyFinal_mergedCoordinates_CsvPath,
            document = elastichutils.VaccinationCampaign)

    elastichutils.createVaccineDeliveriesIndex(connection = constants.elasticConnection)
    elastichutils.uploadCSVToElastic(
            csvPath = constants.vaccinesDeliveriesItalyFinal_mergedCoordinates_CsvPath,
            document = elastichutils.VaccineDeliveries)

    elastichutils.createVaccineRegistryIndex(connection = constants.elasticConnection)
    elastichutils.uploadCSVToElastic(
            csvPath = constants.vaccinesRegistryItalyCsvFinalPath,
            document = elastichutils.VaccineRegistry)


def csvRoutines() -> None:
    ItalyVaccinationCsvManipulation.routine()
    ItalyVaccineRegistryCsvManipulation.routine()
    ItalyVaccineDeliveriesCsvManipulation.routine()


def dailyElasticRoutine() -> None:
    constants.setupConstants()
    elastichutils.deleteAllCovidIndexes(connection = constants.elasticConnection)
    csvRoutines()
    populateDatabase()


if __name__ == '__main__':
    dailyElasticRoutine()
