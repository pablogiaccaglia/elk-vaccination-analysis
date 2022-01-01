import csv
from datetime import date
from enum import Enum
from typing import Optional
from typing import Type
from geojson import Point

from elasticsearch import Elasticsearch
from elasticsearch import helpers
from elasticsearch_dsl import Date, Integer, Text, Document
from elasticsearch_dsl import Field
from elasticsearch_dsl import GeoPoint
from elasticsearch_dsl.connections import connections


class RosettaElasticDSL(Enum):
    int = Integer
    str = Text
    date = Date
    Point = GeoPoint()

def toElasticDataType(pyType: Type) -> Optional[Type[Field]]:
    try:
        return RosettaElasticDSL[pyType.__name__].value
    except KeyError:
        return None

class VaccinationCampaign(Document):
    index = toElasticDataType(pyType = int)
    area = toElasticDataType(pyType = str)
    supplier = toElasticDataType(pyType = str)
    administration_date = toElasticDataType(pyType = date)
    age_group = toElasticDataType(pyType = str)
    start_age = toElasticDataType(pyType = int)
    end_age = toElasticDataType(pyType = int)
    male_count = toElasticDataType(pyType = int)
    female_count = toElasticDataType(pyType = int)
    first_doses = toElasticDataType(pyType = int)
    second_doses = toElasticDataType(pyType = int)
    post_infection_doses = toElasticDataType(pyType = int)
    booster_doses = toElasticDataType(pyType = int)
    NUTS1_code = toElasticDataType(pyType = str)
    NUTS2_code = toElasticDataType(pyType = str)
    region_ISTAT_code = toElasticDataType(pyType = int)
    region_name = toElasticDataType(pyType = str)
    region_coordinates = toElasticDataType(pyType = Point)

    class Index:
        name = "vaccination-campaign"

class VaccineRegistry(Document):
    age_group = toElasticDataType(pyType = str)
    start_age = toElasticDataType(pyType = int)
    end_age = toElasticDataType(pyType = int)
    total_administered = toElasticDataType(pyType = int)
    male_count = toElasticDataType(pyType = int)
    female_count = toElasticDataType(pyType = int)
    first_doses = toElasticDataType(pyType = int)
    second_doses = toElasticDataType(pyType = int)
    post_infection_doses = toElasticDataType(pyType = int)
    booster_doses = toElasticDataType(pyType = int)
    last_update = toElasticDataType(pyType = date)

    class Index:
        name = "vaccine-registry"

class VaccineDeliveries(Document):
    administration_date = toElasticDataType(pyType = date)
    supplier = toElasticDataType(pyType = str)
    area = toElasticDataType(pyType = str)
    age_group = toElasticDataType(pyType = str)
    start_age = toElasticDataType(pyType = int)
    end_age = toElasticDataType(pyType = int)
    male_count = toElasticDataType(pyType = int)
    female_count = toElasticDataType(pyType = int)
    first_doses = toElasticDataType(pyType = int)
    second_doses = toElasticDataType(pyType = int)
    post_infection_doses = toElasticDataType(pyType = int)
    NUTS1_code = toElasticDataType(pyType = str)
    NUTS2_code = toElasticDataType(pyType = str)
    region_ISTAT_code = toElasticDataType(pyType = int)
    region_name = toElasticDataType(pyType = str)
    region_coordinates = toElasticDataType(pyType = Point)

    class Index:
        name = "vaccine-deliveries"


def createVaccineDeliveriesIndex(connection: Elasticsearch) -> None:
    VaccineDeliveries.init(using=connection)

def createVaccineRegistryIndex(connection: Elasticsearch) -> None:
    VaccineRegistry.init(using=connection)

def createVaccinationCampaignIndex(connection: Elasticsearch) -> None:
    VaccinationCampaign.init(using=connection)

def uploadCSVToElastic(csvPath: str, document: Type[Document]) -> None:
    with open(csvPath) as f:
        reader = csv.DictReader(f)
        helpers.bulk(
                connections.get_connection(),
                (document(**row).to_dict(True) for row in reader)
        )
