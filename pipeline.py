import shutil
from typing import Optional
import requests
from os import getcwd

import constants as c


def getFileFormatFromUrl(resourceUrl: str) -> str:
    try:
        dotCharIndexes = [pos for pos, char in enumerate(resourceUrl) if char == '.']
        lastDotCharIndex = dotCharIndexes[-1]
        return resourceUrl[lastDotCharIndex + 1:]
    except:
        return ""


def getFileNameFromUrl(resourceUrl: str) -> str:
    try:
        slashCharIndexes = [pos for pos, char in enumerate(resourceUrl) if char == '/']
        lastSlashCharIndex = slashCharIndexes[-1]
        return resourceUrl[lastSlashCharIndex + 1:]
    except:
        return ""


def downloadResource(resourceUrl: str) -> Optional[bytes]:
    if resourceUrl is None:
        return None

    try:
        r = requests.get(url = resourceUrl)
        return r.content
    except Exception:
        return None


def writeBytesToFile(byts: bytes, filename: str = None) -> None:
    if filename is None:
        filename = getcwd() + '/' + "somefile.txt"

    try:
        f = open(filename, 'wb')
        f.write(byts)
    except:
        pass


def updateItalyVaccinationCsv() -> None:
    try:

        if not c.vaccinationCampaignItalyCsvPath:
            name = getFileNameFromUrl(resourceUrl = c.vaccinationCampaignItalyCsvUrl)
            c.vaccinationCampaignItalyCsvPath = c.datasetsFolderPath + '/' + name
            c.backupVaccinationCampaignCsvPath = c.datasetsFolderPath + '/' + "BACKUP-" + name

        resourceBytes = downloadResource(resourceUrl = c.vaccinationCampaignItalyCsvUrl)
        writeBytesToFile(byts = resourceBytes, filename = c.vaccinationCampaignItalyCsvPath)
        writeBytesToFile(byts = resourceBytes, filename = c.backupVaccinationCampaignCsvPath)
    except:
        shutil.copyfile(c.backupVaccinationCampaignCsvPath, c.vaccinationCampaignItalyCsvPath)


if __name__ == '__main__':
    c.setupConstants()
    updateItalyVaccinationCsv()
