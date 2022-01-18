import constants
from csvmanipulation import (
    ItalyVaccinationCsvManipulation,
    ItalyVaccineRegistryCsvManipulation,
    ItalyVaccineDeliveriesCsvManipulation
)

import elasticutils


def populateDatabase() -> None:
    elasticutils.createVaccinationCampaignIndex(connection = constants.elasticConnection)
    elasticutils.uploadCSVToElastic(
            csvPath = constants.vaccinationCampaignItalyFinal_mergedCoordinates_CsvPath,
            document = elasticutils.VaccinationCampaign)

    elasticutils.createVaccineDeliveriesIndex(connection = constants.elasticConnection)
    elasticutils.uploadCSVToElastic(
            csvPath = constants.vaccinesDeliveriesItalyFinal_mergedCoordinates_CsvPath,
            document = elasticutils.VaccineDeliveries)

    elasticutils.createVaccineRegistryIndex(connection = constants.elasticConnection)
    elasticutils.uploadCSVToElastic(
            csvPath = constants.vaccinesRegistryItalyCsvFinalPath,
            document = elasticutils.VaccineRegistry)


def csvRoutines() -> None:
    ItalyVaccinationCsvManipulation.routine()
    ItalyVaccineRegistryCsvManipulation.routine()
    ItalyVaccineDeliveriesCsvManipulation.routine()


def dailyElasticRoutine() -> None:
    constants.setupConstants()
    csvRoutines()
    elasticutils.deleteAllCovidIndexes(connection = constants.elasticConnection)
    populateDatabase()


if __name__ == '__main__':
    dailyElasticRoutine()
