from enum import Enum

# noinspection PyArgumentList
TYPE = Enum('TYPE', 'stimulus measurement scan_config analysis emka', module=__name__)

FILE_TYPES = {
    TYPE.stimulus: ('.mat', [('matlab', '.mat'), ('json', '.json'), ('python', '.pkl')]),
    TYPE.measurement: ('.csv', [('table', '.csv'), ('matlab', '.mat'), ('python', '.pkl')]),
    TYPE.scan_config: ('.cfg', [('scanImage', '.cfg')]),
    TYPE.analysis: ('.csv', [('data frame', '.pandas'), ('table', '.csv'), ('python', '.pkl')]),
    TYPE.emka: ('.raw', [('raw file', '.raw'), ('raw file txt', '.txt')])}
