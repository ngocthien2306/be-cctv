import io
import datetime
import xlsxwriter

from bson.objectid import ObjectId

from src.utils import model
from src.db.mongo_db import db_connect

def convert_objectid(record):
    record_id = str(record["_id"])
    record["id"] = record_id
    del record["_id"]
    return record

def get_all(filter: model.Filter):
    query = {}
    if filter.module_id is not None:
        query["module_id"] = filter.module_id
    if filter.camera_id is not None:
        query["camera_id"] = filter.camera_id
    if filter.shift is not None:
        query["shift"] = filter.shift
    if filter.line is not None:
        query["line"] = filter.line

    if filter.size > 50:
        filter.size = 50

    if filter.start_timestamp > 0:
        if not query.get("timestamp"):
            query["timestamp"] = {}
        query["timestamp"]["$gte"] = filter.start_timestamp
    if filter.end_timestamp > 0:
        if not query.get("timestamp"):
            query["timestamp"] = {}
        query["timestamp"]["$lte"] = filter.end_timestamp

    collection = db_connect.get_collection()
    cursor = collection.find(query).sort("timestamp", -1)
    count = collection.count_documents(query)
    skips = filter.size * filter.page
    records = cursor.skip(skips).limit(filter.size)
    return map(convert_objectid, records), count

def report_false(id: str):
    collection = db_connect.get_collection()
    collection.update_one({"_id": ObjectId(id)}, {"$set": { "set_false": True }})

def export_xlsx(filter: model.Filter):
    records, _ = get_all(filter)
    
    output = io.BytesIO()
    workbook = xlsxwriter.Workbook(output, {'in_memory': True})
    worksheet = workbook.add_worksheet()

    worksheet.write(0, 0, "THOI GIAN")
    worksheet.write(0, 1, "CAMERA")
    worksheet.write(0, 2, "MODULE")
    worksheet.write(0, 3, "CA LAM VIEC")
    worksheet.write(0, 4, "LINE")


    for index, record in enumerate(records):
        row_index = index + 1
        timestamp = record["timestamp"]
        date_time = datetime.datetime.fromtimestamp(timestamp).strftime("%d/%m/%Y, %H:%M:%S")
        camera_id = record["camera_id"]
        module_id = record["module_id"]
        shift = record["shift"]
        line = record["line"]

        worksheet.write(row_index, 0, date_time)
        worksheet.write(row_index, 1, camera_id)
        worksheet.write(row_index, 2, module_id)
        worksheet.write(row_index, 3, shift)
        worksheet.write(row_index, 4, line)
    workbook.close()
    output.seek(0)
    return output