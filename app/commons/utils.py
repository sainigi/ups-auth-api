from datetime import datetime, timedelta, timezone
from dateutil import parser, tz
from typing import Dict, List
from uuid import UUID
import pytz
import base64

def format_date(dt: str):
    try:
        return dt[:-3]+'Z'
    except:
        raise


def get_now_date_time():
    try:
        now = datetime.now()
        date_str = now.strftime('%Y-%m-%dT%H:%M:%S.%f')
        return format_date(date_str)
    except:
        raise

def sub_dict(dictionary: Dict, columns: List):
    try:
        return {key: dictionary[key] for key in columns}
    except:
        raise

def stringify_dt(dt: datetime):
    return dt.strftime('%m/%d/%Y %H:%M:%S %p')

def get_latest_date(date_list):
    try:
        parse_dt_list = []
        for dt in date_list:
            parse_dt= parser.parse(dt)
            if parse_dt.tzinfo is None:
                parse_dt = parse_dt.replace(tzinfo=tz.tzutc())
            parse_dt_list.append(parse_dt)

        latest_date = max(parse_dt_list)
        return format_date(latest_date.strftime("%Y-%m-%dT%H:%M:%S.%f"))
    except:
        raise

def isValidUUID(id_):
    try:
        UUID(id_, version=4)
        return True
    except ValueError:
        return False

def get_now_date():
    now = datetime.now()
    date_str = now.strftime('%Y-%m-%d')
    return date_str


def get_now_date_time_by_timezone(time_zone):
    now_in_tz = datetime.now(pytz.timezone(time_zone))
    return now_in_tz


def get_execute_at(time_zone):
    now_in_tz = get_now_date_time_by_timezone(time_zone)
    # logger.debug(f"Current Local Time in {time_zone} : {now_in_tz.strftime('%m/%d/%Y %H:%M:%S %p')}")
    today12am_in_tz = pytz.timezone(time_zone).localize(datetime.combine(now_in_tz.date(), datetime.min.time()))
    today12_01am_in_tz = today12am_in_tz + timedelta(minutes=1)
    next12_01am_in_tz = today12_01am_in_tz if now_in_tz < today12_01am_in_tz else today12_01am_in_tz + timedelta(days=1)
    # logger.debug(f"Next 12:01 a.m. in {time_zone} : {next12_01am_in_tz.strftime('%m/%d/%Y %H:%M:%S %p')}")
    next12_01am_in_utc = next12_01am_in_tz.astimezone(timezone.utc)
    # logger.debug(f"Next 12:01 a.m. in UTC : {next12_01am_in_utc.strftime('%m/%d/%Y %H:%M:%S %p')}")
    return next12_01am_in_utc.strftime('%m/%d/%Y %H:%M:%S %p')

def decode_image_string_to_varbinary(imagebase:str):
    return base64.b64decode(imagebase)

def encode_image_string_to_varbinary(imagebase):
    return base64.b64encode(imagebase).decode('utf-8')

def get_device_type(lastOctet:str,brand:str):
    device_types=[
         {
            "DeviceName": "Ingenico Device / POS Handheld Device",
            "Brand": BrandName.Outback,
            "FirstOctet": "10",
            "LastOctet": "114"
        },
        {
            "DeviceName": "POS Handheld Device",
            "Brand": BrandName.Outback,
            "FirstOctet": "10",
            "LastOctet": "115"
        },
        {
            "DeviceName": "POS Handheld Device",
            "Brand": BrandName.Outback,
            "FirstOctet": "10",
            "LastOctet": "116"
        },
        {
            "DeviceName": "POS Handheld Device",
            "Brand": BrandName.Outback,
            "FirstOctet": "10",
            "LastOctet": "117"
        },
        {
            "DeviceName": "POS Handheld Device",
            "Brand": BrandName.Outback,
            "FirstOctet": "10",
            "LastOctet": "118"
        },
        {
            "DeviceName": "POS Terminal #6",
            "Brand": BrandName.Outback,
            "FirstOctet": "10",
            "LastOctet": "26"
        },
        {
            "DeviceName": "POS Terminal #7",
            "Brand": BrandName.Outback,
            "FirstOctet": "10",
            "LastOctet": "27"
        },
        {
            "DeviceName": "POS Terminal #8",
            "Brand": BrandName.Outback,
            "FirstOctet": "10",
            "LastOctet": "28"
        },
        {
            "DeviceName": "POS Terminal #9",
            "Brand": BrandName.Outback,
            "FirstOctet": "10",
            "LastOctet": "29"
        },
        {
            "DeviceName": "POS Terminal #10",
            "Brand": BrandName.Outback,
            "FirstOctet": "10",
            "LastOctet": "30"
        },
        {
            "DeviceName": "POS Terminal #1 / Backup POS Driver",
            "Brand": BrandName.Bonefish,
            "FirstOctet": "10",
            "LastOctet": "21"
        },
        {
            "DeviceName": "POS Terminal #2",
            "Brand": BrandName.Bonefish,
            "FirstOctet": "10",
            "LastOctet": "22"
        },
        {
            "DeviceName": "POS Terminal #3",
            "Brand": BrandName.Bonefish,
            "FirstOctet": "10",
            "LastOctet": "23"
        },
        {
            "DeviceName": "POS Terminal #4",
            "Brand": BrandName.Bonefish,
            "FirstOctet": "10",
            "LastOctet": "24"
        },
        {
            "DeviceName": "POS Terminal #5",
            "Brand": BrandName.Bonefish,
            "FirstOctet": "10",
            "LastOctet": "25"
        },
        {
            "DeviceName": "POS Terminal #6",
            "Brand": BrandName.Bonefish,
            "FirstOctet": "10",
            "LastOctet": "26"
        },
        {
            "DeviceName": "POS Terminal #7",
            "Brand": BrandName.Bonefish,
            "FirstOctet": "10",
            "LastOctet": "27"
        },
        {
            "DeviceName": "POS Terminal #8",
            "Brand": BrandName.Bonefish,
            "FirstOctet": "10",
            "LastOctet": "28"
        },
        #  {
        #     "DeviceName": "Fleming's Winepad",
        #     "Brand": BrandName.FLEMINGS,
        #     "FirstOctet": "10",
        #     "LastOctet": "161"
        # },
        #  {
        #     "DeviceName": "Fleming's Winepad",
        #     "Brand": BrandName.FLEMINGS,
        #     "FirstOctet": "10",
        #     "LastOctet": "162"
        # },
        #  {
        #     "DeviceName": "Fleming's Winepad",
        #     "Brand": BrandName.FLEMINGS,
        #     "FirstOctet": "10",
        #     "LastOctet": "163"
        # },
        #  {
        #     "DeviceName": "Fleming's Winepad",
        #     "Brand": BrandName.FLEMINGS,
        #     "FirstOctet": "10",
        #     "LastOctet": "164"
        # },
        #  {
        #     "DeviceName": "Fleming's Winepad",
        #     "Brand": BrandName.FLEMINGS,
        #     "FirstOctet": "10",
        #     "LastOctet": "165"
        # },
        #  {
        #     "DeviceName": "Fleming's Winepad",
        #     "Brand": BrandName.FLEMINGS,
        #     "FirstOctet": "10",
        #     "LastOctet": "166"
        # },
        #  {
        #     "DeviceName": "Fleming's Winepad",
        #     "Brand": BrandName.FLEMINGS,
        #     "FirstOctet": "10",
        #     "LastOctet": "167"
        # },
        #  {
        #     "DeviceName": "Fleming's Winepad",
        #     "Brand": BrandName.FLEMINGS,
        #     "FirstOctet": "10",
        #     "LastOctet": "168"
        # },
        #  {
        #     "DeviceName": "Fleming's Winepad",
        #     "Brand": BrandName.FLEMINGS,
        #     "FirstOctet": "10",
        #     "LastOctet": "169"
        # },

        #  {
        #     "DeviceName": "Fleming's Winepad",
        #     "Brand": BrandName.FLEMINGS,
        #     "FirstOctet": "10",
        #     "LastOctet": "170"
        # },
        #  {
        #     "DeviceName": "Tablet1",
        #     "Brand": BrandName.AGO,
        #     "FirstOctet": "10",
        #     "LastOctet": "161"
        # },
        # {
        #     "DeviceName": "Tablet2",
        #     "Brand": BrandName.AGO,
        #     "FirstOctet": "10",
        #     "LastOctet": "162"
        # }
        # ,
        # {
        #     "DeviceName": "Tablet3",
        #     "Brand": BrandName.AGO,
        #     "FirstOctet": "10",
        #     "LastOctet": "163"
        # }
        # ,
        # {
        #     "DeviceName": "Tablet4",
        #     "Brand": BrandName.AGO,
        #     "FirstOctet": "10",
        #     "LastOctet": "164"
        # }
        # ,
        # {
        #     "DeviceName": "Tablet5",
        #     "Brand": BrandName.AGO,
        #     "FirstOctet": "10",
        #     "LastOctet": "165"
        # }
        # ,
        # {
        #     "DeviceName": "Tablet6",
        #     "Brand": BrandName.AGO,
        #     "FirstOctet": "10",
        #     "LastOctet": "166"
        # }
        # ,
        # {
        #     "DeviceName": "Tablet7",
        #     "Brand": BrandName.AGO,
        #     "FirstOctet": "10",
        #     "LastOctet": "167"
        # }
        # ,
        # {
        #     "DeviceName": "Tablet8",
        #     "Brand": BrandName.AGO,
        #     "FirstOctet": "10",
        #     "LastOctet": "168"
        # }
        # ,
        # {
        #     "DeviceName": "Tablet9",
        #     "Brand": BrandName.AGO,
        #     "FirstOctet": "10",
        #     "LastOctet": "169"
        # }
        # ,
        # {
        #     "DeviceName": "Tablet10",
        #     "Brand": BrandName.AGO,
        #     "FirstOctet": "10",
        #     "LastOctet": "170"
        # },
         {
            "DeviceName": "Tablet1",
            "Brand": BrandName.Outback,
            "FirstOctet": "10",
            "LastOctet": "161"
        },
        {
            "DeviceName": "Tablet2",
            "Brand": BrandName.Outback,
            "FirstOctet": "10",
            "LastOctet": "162"
        }
        ,
        {
            "DeviceName": "Tablet3",
            "Brand": BrandName.Outback,
            "FirstOctet": "10",
            "LastOctet": "163"
        }
        ,
        {
            "DeviceName": "Tablet4",
            "Brand": BrandName.Outback,
            "FirstOctet": "10",
            "LastOctet": "164"
        }
        ,
        {
            "DeviceName": "Tablet5",
            "Brand": BrandName.Outback,
            "FirstOctet": "10",
            "LastOctet": "165"
        }
        ,
        {
            "DeviceName": "Tablet6",
            "Brand": BrandName.Outback,
            "FirstOctet": "10",
            "LastOctet": "166"
        }
        ,
        {
            "DeviceName": "Tablet7",
            "Brand": BrandName.Outback,
            "FirstOctet": "10",
            "LastOctet": "167"
        }
        ,
        {
            "DeviceName": "Tablet8",
            "Brand": BrandName.Outback,
            "FirstOctet": "10",
            "LastOctet": "168"
        }
        ,
        {
            "DeviceName": "Tablet9",
            "Brand": BrandName.Outback,
            "FirstOctet": "10",
            "LastOctet": "169"
        }
        ,
        {
            "DeviceName": "Tablet10",
            "Brand": BrandName.Outback,
            "FirstOctet": "10",
            "LastOctet": "170"
        }

    ]
    deviceTypes= next(iter(filter(lambda x: x["LastOctet"]==lastOctet and  x["Brand"]==brand  ,device_types)),None)
    if deviceTypes ==None:
      return ""
    else:
      return deviceTypes["DeviceName"];


class BrandName(enumerate):
    Bonefish = "Bonefish"
    Outback = "Outback"
    FLEMINGS="FLEMING'S"
    AGO="AGO"

