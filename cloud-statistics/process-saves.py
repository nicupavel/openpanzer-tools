__author__ = 'panic'

import sys, os
import json

saves_dir = "downloaded"
standalone_scenarios = {}
campaign_scenarios = {}

file_count = 0

def find_human_player(players_json):
    if players_json is None:
        return None

    for player in players_json:
        if player["type"] == 0:
            return player

    return None

def create_data_structure(data, key):

    if key not in data:
            data[key] = {}

    if turn not in data[key]:
        data[key][turn] = {}
        data[key][turn]["occurences"] = 0

    if "prestige" not in data[key][turn]:
        data[key][turn]["prestige"] = []

    if "score" not in data[key][turn]:
        data[key][turn]["score"] = []

def get_units_totals(units_json, totals = None):

    if totals is None:
        totals = {
            "entrenched": 0,
            "entrenchment" : 0,
            "experience" : 0,
            "moved" : 0,
            "fired" : 0,
            "supply" : 0,
            "hits" : 0,
            "noammo" : 0,
            "nofuel" : 0,
            "leaders" : 0,
            "strength" : 0,
            "damaged" : 0,
            "transporting" : 0,
            "surprised" : 0,
            "spotted" : 0,
            "units": []
        }

    if units_json is None:
        return totals

    for unit in units_json:
        if unit["eqid"] < 0:
            continue

        totals["units"].append(unit["eqid"])
        totals["entrenchment"] += unit["entrenchment"]
        totals["experience"] += unit["experience"]
        totals["hits"] += unit["hits"]
        totals["strength"] += unit["strength"]

        if unit["entrenchment"] > 0:
            totals["entrenched"] += 1
        if unit["hasMoved"]:
            totals["moved"] += 1
        if unit["hasFired"]:
            totals["fired"] += 1
        if unit["hasResupplied"]:
            totals["supply"] += 1
        if unit["ammo"] <= 0:
            totals["noammo"] += 1
        if unit["fuel"] <= 0:
            totals["nofuel"] += 1
        if "leader" in unit and unit["leader"] > -1:  # Old save games
            totals["leaders"] += 1
        if unit["strength"] < 10:
            totals["damaged"] += 1
        if unit["isMounted"]:
            totals["transporting"] += 1
        if unit["isSurprised"]:
            totals["surprised"] += 1
        if unit["tempSpotted"]:
            totals["spotted"] += 1

    return totals


if __name__ == "__main__":
    for file in os.listdir(saves_dir):
        file_count += 1
        is_campaign = False
        current_dict = standalone_scenarios
        try:
            with open(os.path.join(saves_dir, file), "r") as f:
                save = json.load(f)
        except Exception, e:
            print("Error processing save: %s ! Skipping." % file)
            continue

        if "campaign" in save and save["campaign"] is not None:
            is_campaign = True
            current_dict = campaign_scenarios

        player = find_human_player(save.get("players", None))
        if player is None:
            print "Invalid save game no human player found"
            continue

        turn = player["playedTurn"]

        if int(turn) > 30:
            continue

        name = save["scenario"]["name"]

        print "Processing file %s, %s scenario %s, turn %d" % (file, ("campaign" if is_campaign else "standalone"), save["scenario"]["name"], turn)

        create_data_structure(current_dict, name)
        current_dict[name][turn]["prestige"].append(player["prestige"])
        current_dict[name][turn]["score"].append(player["score"])
        current_dict[name][turn]["occurences"] += 1

        if is_campaign:
            unit_data = save["campaign"]["coreUnits"]
        else:
            unit_data = None

        previous_totals = current_dict[name][turn].get("totals", None)
        current_dict[name][turn]["totals"] = get_units_totals(unit_data, previous_totals)

        #current_dict[name][turn][file] = save

        #if file_count > 200:
        #    break


    with open("standalone-scenarios.json", "w") as f:
        json.dump(standalone_scenarios, f, sort_keys=True, indent=2)

    with open("campaign-scenarios.json", "w") as f:
        json.dump(campaign_scenarios, f, sort_keys=True, indent=2)

