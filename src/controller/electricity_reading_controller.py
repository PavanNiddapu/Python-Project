from flask import abort

from service.time_converter import iso_format_to_unix_time, unix_to_iso

from repository.electricity_reading_repository import ElectricityReadingRepository
from service.electricity_reading_service import ElectricityReadingService

repository = ElectricityReadingRepository()
service = ElectricityReadingService(repository)


def store(data):
    service.store_reading(data)
    return data


def read(smart_meter_id):
    readings = service.retrieve_readings_for(smart_meter_id)
    if len(readings) < 1:
        abort(404)
    else:
        return [r.to_json() for r in readings]


def read_t(smart_meter_id):
    readings = service.retrieve_readings_for(smart_meter_id)
    lis = []
    if len(readings) < 1:
        abort(404)
    else:

        times = [r.to_json()["time"] for r in readings]
        for t in times:
            lis.append(unix_to_iso(t))
        return lis


def sum_readings(smart_meter_id):
    readings = service.retrieve_readings_for(smart_meter_id)
    if len(readings) < 1:
        abort(404)
    else:
        readings = [r.to_json()["reading"] for r in readings]
        return sum(readings)
