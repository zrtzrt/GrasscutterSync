from GMReader import IdMap
from configparser import ConfigParser
from pymongo import MongoClient
from GOODV1sync import GoodV1sync
from SyncCore import load_json


def input_uid():
    uid = input("UID:")
    account = db["accounts"].find_one(uid)
    if not account:
        print("account not found")
        uid = input_uid()
    else:
        print("using account:" + account["username"])
    return uid


if __name__ == '__main__':
    config = ConfigParser()
    config.read('config.ini', encoding='UTF-8')
    idMap = IdMap(config)
    client = MongoClient(config["database"]["host"], int(config["database"]["port"]))
    db = client[config["database"]["name"]]
    print("connect database success")
    uid = int(input_uid())
    dataPath = input("JSON DATA PATH:")
    data = load_json(dataPath)
    if data["format"] == "GOOD" and data["version"] == 1:
        GoodV1sync(uid, data, idMap, db, config)
    else:
        print("format not support:{}. version:{}".format(data["format"], data["version"]))
