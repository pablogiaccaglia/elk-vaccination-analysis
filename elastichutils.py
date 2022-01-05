import csv
from datetime import date
from enum import Enum
from typing import Optional
from typing import Type
from geojson import Point

from elasticsearch import Elasticsearch
from elasticsearch import helpers
from elasticsearch_dsl import Date, Integer, Text, Document, Float, Keyword, Long
from elasticsearch_dsl import Field
from elasticsearch_dsl import GeoPoint
from elasticsearch_dsl.connections import connections


class RosettaElasticDSL(Enum):
    int = Integer
    str = Text
    date = Date
    Point = GeoPoint
    float = Float
    key = Keyword
    long = Long


class INDEXES(Enum):
    VACCINATON_CAMPAIGN = "vaccination-campaign"
    VACCINE_DELIVERIES = "vaccine-deliveries"
    VACCINE_REGISTRY = "vaccine-registry"


def toElasticDataType(pyType: Type = None, isKeyword = False, isLong = False, byName: str = None) -> Optional[Type[Field]]:
    if pyType or isKeyword:
        if isKeyword:
            typ = "key"
        elif isLong:
            typ = "long"
        elif pyType:
            typ = pyType.__name__

        elif byName:
            typ = byName
        try:
            return RosettaElasticDSL[typ].value()
        except KeyError:
            return None
    else:
        return None


class VaccinationCampaign(Document):
    index = toElasticDataType(pyType = int)
    area = toElasticDataType(pyType = str)
    supplier = toElasticDataType(isKeyword = True)
    administration_date = toElasticDataType(pyType = date)
    age_group = toElasticDataType(isKeyword = True)
    male_count = toElasticDataType(pyType = int)
    female_count = toElasticDataType(pyType = int)
    first_doses = toElasticDataType(pyType = int)
    second_doses = toElasticDataType(pyType = int)
    post_infection_doses = toElasticDataType(pyType = int)
    booster_doses = toElasticDataType(pyType = int)
    NUTS1_code = toElasticDataType(pyType = str)
    NUTS2_code = toElasticDataType(pyType = str)
    region_ISTAT_code = toElasticDataType(pyType = int)
    region_name = toElasticDataType(isKeyword = True)
    region_coordinates = toElasticDataType(pyType = Point)

    class Index:
        name = INDEXES.VACCINATON_CAMPAIGN.value


class VaccineDeliveries(Document):
    area = toElasticDataType(pyType = str)
    supplier = toElasticDataType(isKeyword = True)
    doses_amount = toElasticDataType(pyType = int)
    delivery_date = toElasticDataType(pyType = date)
    NUTS1_code = toElasticDataType(pyType = str)
    NUTS2_code = toElasticDataType(pyType = str)
    region_ISTAT_code = toElasticDataType(pyType = int)
    region_name = toElasticDataType(isKeyword = True)
    region_coordinates = toElasticDataType(pyType = Point)

    class Index:
        name = INDEXES.VACCINE_DELIVERIES.value


class VaccineRegistry(Document):
    age_group = toElasticDataType(isKeyword = True)
    total_administered = toElasticDataType(pyType = int)
    male_count = toElasticDataType(pyType = int)
    female_count = toElasticDataType(pyType = int)
    first_doses = toElasticDataType(pyType = int)
    second_doses = toElasticDataType(pyType = int)
    post_infection_doses = toElasticDataType(pyType = int)
    booster_doses = toElasticDataType(pyType = int)
    last_update = toElasticDataType(pyType = date)

    class Index:
        name = INDEXES.VACCINE_REGISTRY.value


def deleteIndex(connection: Elasticsearch, index: INDEXES) -> None:
    connection.indices.delete(index = index.value, ignore = [400, 404])


def deleteAllCovidIndexes(connection: Elasticsearch) -> None:
    connection.indices.delete(index = INDEXES.VACCINE_DELIVERIES.value, ignore = [400, 404])
    connection.indices.delete(index = INDEXES.VACCINATON_CAMPAIGN.value, ignore = [400, 404])
    connection.indices.delete(index = INDEXES.VACCINE_REGISTRY.value, ignore = [400, 404])


def createVaccineRegistryIndex(connection: Elasticsearch) -> None:
    VaccineRegistry.init(using = connection)


def createVaccineDeliveriesIndex(connection: Elasticsearch) -> None:
    VaccineDeliveries.init(using = connection)


def createVaccinationCampaignIndex(connection: Elasticsearch) -> None:
    VaccinationCampaign.init(using = connection)


def uploadCSVToElastic(csvPath: str, document: Type[Document]) -> None:
    with open(csvPath) as f:
        reader = csv.DictReader(f)
        helpers.bulk(
                connections.get_connection(),
                (document(**row).to_dict(True) for row in reader)
        )
