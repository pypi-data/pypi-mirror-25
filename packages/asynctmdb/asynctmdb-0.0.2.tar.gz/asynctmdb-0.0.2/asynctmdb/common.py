from enum import IntEnum

DATE_FORMAT = '%Y-%m-%d'
TIME_FORMAT = '%H:%M:%S'
DATE_TIME_FORMAT = ('{date_format} {time_format} %Z'
                    .format(date_format=DATE_FORMAT,
                            time_format=TIME_FORMAT))


class StatusCode(IntEnum):
    SUCCESS = 1
    AUTHENTICATION_FAILED = 3
    INVALID_API_KEY = 7
    INTERNAL_ERROR = 11
    SUCCESSFULLY_DELETED = 13
    SESSION_DENIED = 17
    INVALID_PAGE = 22
    RESOURCE_NOT_FOUND = 34
