import json
from typing import List, Dict


def load_json(path):
    res = {}
    try:
        with open(path, "r", encoding="utf-8") as f:
            res = json.load(f)
    except IOError:
        print("Error: file not found. PATH:" + path)
    else:
        return res


def text_process(text):
    return text.title().replace("\"", "").replace("'S", "s").replace("'", "").replace("-", "").replace(" ", "")


def get_sub_attr(sub_map: Dict[str, Dict[float, int]],
                 sub_stats: List[Dict[str, any]], attr_map: Dict[str, str]) -> List[int]:
    def cal_sub_attr(val_map: Dict[float, int], target: float) -> List[int]:
        all_solve = combination_sum(list(val_map.keys()), target)
        id_list = []
        for sub in all_solve[-1]:
            id_list.append(val_map[sub])
        return id_list

    res = []
    for sub_stat in sub_stats:
        if not sub_stat["key"] is None:
            res.extend(cal_sub_attr(sub_map[attr_map[sub_stat["key"]]], sub_stat["value"]))
    return res


# https://leetcode.com/problems/combination-sum/
def combination_sum(candidates: List[float], target: float) -> List[List[float]]:
    def dfs(candidates, begin, size, path, res, target):
        if target == 0:
            res.append(path)
            return

        for index in range(begin, size):
            residue = target - candidates[index]
            if residue < 0:
                break

            dfs(candidates, index, size, path + [candidates[index]], res, residue)

    size = len(candidates)
    if size == 0:
        return []
    candidates.sort()
    path = []
    res = []
    dfs(candidates, 0, size, path, res, target)
    return res
