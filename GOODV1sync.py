import time
import SyncCore


class GoodV1sync:
    uid = 10001
    data = {}
    idMap = {}
    db = {}
    config = {}

    def set_avatars(self):
        main = self.db["players"].find_one(self.uid)["mainCharacterId"]
        deleted = self.db["avatars"].delete_many({"ownerId": self.uid, "avatarId": {"$ne": main}})
        print("deleted {} avatars".format(deleted.deleted_count))
        characters = self.data["characters"]
        avt_map = SyncCore.load_json(self.config["path"]["avt_map"])
        char_map = self.idMap.Character
        ids = []
        for character in characters:
            try:
                avt_id = str(char_map[character["key"]])
                avatar = avt_map[avt_id]
                avatar["ownerId"] = self.uid
                avatar["bornTime"] = time.time()
                avatar["promoteLevel"] = character["ascension"]
                avatar["coreProudSkillLevel"] = character["constellation"]
                avatar["level"] = character["level"]
                if avatar["promoteLevel"] > 0:
                    avatar["proudSkillList"].append(int(avt_id[-2:] + "2101"))
                if avatar["promoteLevel"] > 3:
                    avatar["proudSkillList"].append(int(avt_id[-2:] + "2201"))
                talents = ["auto", "skill", "burst"]
                for index, key in enumerate(list(avatar["skillLevelMap"].keys())):
                    if index > 3:
                        avatar["skillLevelMap"][key] = character["talent"][talents[index]]
                inserted = self.db["avatars"].insert_one(avatar)
                ids.append(inserted.inserted_id)
            except KeyError as e:
                print("Error: avatar:{} insert fail. Key:{}".format(character["key"], e.args))
        print("inserted {} avatar finish".format(len(ids)))

    def set_artifacts(self):
        artifacts = self.data["artifacts"]
        art_map = self.idMap.Artifacts["set"]
        attr_map = SyncCore.load_json(self.config["path"]["attr_map"])
        main_map = self.idMap.Artifacts["main"]
        sub_map = self.idMap.Artifacts["sub"]
        char_map = self.idMap.Character
        ids = []
        for artifact in artifacts:
            try:
                item = {
                    "ownerId": self.uid,
                    "itemId": art_map[artifact["setKey"]][artifact["slotKey"]][artifact["rarity"]][0],
                    "count": 1,
                    "level": artifact["level"] + 1,
                    "exp": 0,
                    "totalExp": 0,
                    "promoteLevel": 0,
                    "locked": artifact["lock"],
                    "affixes": [],
                    "refinement": 0,
                    "mainPropId": main_map[attr_map[artifact["mainStatKey"]]][artifact["slotKey"]],
                    "appendPropIdList": SyncCore.get_sub_attr(sub_map, artifact["substats"], attr_map),
                    "equipCharacter": char_map[artifact["location"]] if artifact["location"] != "" else 0
                }
                inserted = self.db["items"].insert_one(item)
                ids.append(inserted.inserted_id)
            except KeyError as e:
                print("Error: artifact:{}, part:{} insert fail. Key:{}"
                      .format(artifact["setKey"], artifact["slotKey"], e.args))
        print("inserted {} artifact finish".format(len(ids)))

    def set_materials(self):
        materials = self.data["materials"]
        mat_map = self.idMap.Materials
        ids = []
        for material in materials:
            try:
                item = {
                    "ownerId": self.uid,
                    "itemId": mat_map[material],
                    "count": materials[material] if materials[material] != 0 else 1,
                    "level": 0,
                    "exp": 0,
                    "totalExp": 0,
                    "promoteLevel": 0,
                    "locked": False,
                    "affixes": [],
                    "refinement": 0,
                    "mainPropId": 0,
                    "equipCharacter": 0
                }
                inserted = self.db["items"].insert_one(item)
                ids.append(inserted.inserted_id)
            except KeyError as e:
                print("Error: material:{} insert fail. Key:{}".format(material, e.args))
        print("inserted {} material finish".format(len(ids)))

    def set_weapons(self):
        weapons = self.data["weapons"]
        wp_map = self.idMap.Weapons
        char_map = self.idMap.Character
        ids = []
        for weapon in weapons:
            try:
                item = {
                    "ownerId": self.uid,
                    "itemId": wp_map[weapon["key"]],
                    "count": 1,
                    "level": weapon["level"],
                    "exp": 0,
                    "totalExp": 0,
                    "promoteLevel": weapon["ascension"],
                    "locked": weapon["lock"],
                    "affixes": [],
                    "refinement": weapon["refinement"] - 1,
                    "mainPropId": 0,
                    "equipCharacter": char_map[weapon["location"]] if weapon["location"] != "" else 0
                }
                inserted = self.db["items"].insert_one(item)
                ids.append(inserted.inserted_id)
            except KeyError as e:
                print("Error: weapon:{} insert fail. Key:{}".format(weapon["key"], e))
        print("inserted {} weapon finish".format(len(ids)))

    def __init__(self, uid, data, id_map, db, config):
        self.uid = uid
        self.data = data
        self.idMap = id_map
        self.db = db
        self.config = config

        self.set_avatars()
        res = db["items"].delete_many({"ownerId": uid})
        print("deleted {} items".format(res.deleted_count))
        self.set_weapons()
        self.set_artifacts()
        self.set_materials()
