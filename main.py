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

    elastichutils.createVaccineRegistryIndex(connection = constants.elasticConnection)
    elastichutils.uploadCSVToElastic(
            csvPath = constants.vaccinesDeliveriesItalyFinal_mergedCoordinates_CsvPath,
            document = elastichutils.VaccineRegistry)

    elastichutils.createVaccineDeliveriesIndex(connection = constants.elasticConnection)
    elastichutils.uploadCSVToElastic(
            csvPath = constants.vaccinesRegistryItalyCsvFinalPath,
            document = elastichutils.VaccineDeliveries)

def csvRoutines() -> None:
    ItalyVaccinationCsvManipulation.routine()
    ItalyVaccineRegistryCsvManipulation.routine()
    ItalyVaccineDeliveriesCsvManipulation.routine()


if __name__ == '__main__':
    constants.setupConstants()
    # csvRoutines()
    populateDatabase()
