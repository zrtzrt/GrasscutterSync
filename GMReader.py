import SyncCore


class IdMap:
    config = {}
    Character = {}
    Weapons = {}
    Materials = {}
    Artifacts = {"set": {}, "name": {}, "main": {}, "sub": {}}
    LivingBeings = {}
    MonsterList = {}
    Scene = {}
    NPC = {}

    def load_gm(self):
        status = ""
        with open(self.config["path"]["handbook"], "r", encoding="utf-8") as f:
            for line in f.readlines():
                line = line.strip('\n')  # 去掉列表中每一个元素的换行符
                if line.startswith("===") and line.endswith("==="):
                    status = SyncCore.text_process(line.strip("==="))
                    continue
                if line == "####################":
                    print("load {} success".format(status))
                    status = ""
                    continue
                if status == "Character" and ":" in line:
                    item = line.split(":")
                    if len(item) == 2:
                        self.Character[SyncCore.text_process(item[1])] = int(item[0])
                    continue
                if status == "Weapons" and ":" in line:
                    item = line.split(":")
                    if len(item) == 2:
                        self.Weapons[SyncCore.text_process(item[1])] = int(item[0])
                    continue
                if status == "Materials" and ":" in line:
                    item = line.split(":")
                    if len(item) == 2:
                        self.Materials[SyncCore.text_process(item[1])] = int(item[0])
                    continue
                if status == "Artifacts" and ":" in line:
                    part_map = ["?", "goblet", "plume", "circlet", "flower", "sands", "?", "?", "?", "?"]
                    set_map = SyncCore.load_json(self.config["path"]["set_map"])
                    item = line.split(":")
                    if len(item) == 2:
                        set_id = item[0][0:2]
                        set_name = set_map[set_id]
                        part = part_map[int(item[0][3])]
                        text = SyncCore.text_process(item[1])
                        level = int(item[0][2])
                        if set_name not in self.Artifacts["set"]:
                            self.Artifacts["set"][set_name] = {}
                        if part not in self.Artifacts["set"][set_name]:
                            self.Artifacts["set"][set_name][part] = {}
                        if level not in self.Artifacts["set"][set_name][part]:
                            self.Artifacts["set"][set_name][part][level] = []
                        self.Artifacts["set"][set_name][part][level].append(int(item[0]))
                        if text not in self.Artifacts["name"]:
                            self.Artifacts["name"][text] = {}
                        if level not in self.Artifacts["name"][text]:
                            self.Artifacts["name"][text][level] = []
                        self.Artifacts["name"][text][level].append(int(item[0]))
                    continue
                if status == "LivingBeings" and ":" in line:
                    item = line.split(":")
                    if len(item) == 2:
                        self.LivingBeings[SyncCore.text_process(item[1])] = int(item[0])
                    continue
                if status == "ArtifactMainAttribution" and ":" in line:
                    part_map = ["sands", "?", "plume", "circlet", "flower", "goblet"]
                    item = line.split(":")
                    if len(item) == 2:
                        text = item[1].replace(" ", "")
                        part = part_map[int(item[0][1])]
                        if text not in self.Artifacts["main"]:
                            self.Artifacts["main"][text] = {}
                        self.Artifacts["main"][text][part] = int(item[0])
                    continue
                if status == "ArtifactSubAttribution" and ":" in line:
                    item = line.split(":")
                    if len(item) == 2:
                        text_list = item[1].split("+")
                        text = text_list[0].replace(" ", "")
                        value = float(text_list[1].replace("%", ""))
                        if text not in self.Artifacts["sub"]:
                            self.Artifacts["sub"][text] = {}
                        if 0 < value < 300:
                            self.Artifacts["sub"][text][value] = int(item[0])
                    continue
                if status == "MonsterList" and ":" in line:
                    item = line.split(":")
                    if len(item) == 2:
                        self.MonsterList[SyncCore.text_process(item[1])] = int(item[0])
                    continue
                if status == "Scene" and ":" in line:
                    item = line.split(":")
                    if len(item) == 2:
                        self.Scene[SyncCore.text_process(item[1])] = int(item[0])
                    continue
                if status == "NPC" and ":" in line:
                    item = line.split(":")
                    if len(item) == 2:
                        self.NPC[SyncCore.text_process(item[1])] = int(item[0])
                    continue

    def __init__(self, config):
        self.config = config
        self.load_gm()
        print("load Handbook finish")
