import os
import json
import numpy
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd


RAW_STATS_FILE = "campaign-scenarios.json"
GRAPHS_DIR = "graphs"
EQUIPMENT_LOCATION = "../../resources/equipment"

UNIT_CLASS_NAMES = [
    "No Class", "Infantry", "Tank", "Recon", "Anti Tank", "Flak", "Fortification",
    "Ground Transport", "Artillery", "Air Defence", "Fighter Aircraft", "Tactical Bomber",
    "Level Bomber", "Air Transport", "Submarine" , "Destroyer", "Battleship",
    "Aircraft Carrier", "Naval Transport", "Battle Cruiser", "Cruiser", "Light Cruiser"
]

SKIP_SCENARIO_GRAPHS = False

def load_equipment():
    equipment = {}
    for file in os.listdir(EQUIPMENT_LOCATION):
        try:
            with open(os.path.join(EQUIPMENT_LOCATION, file), "r") as f:
                json_data = json.load(f)
            equipment.update(json_data["units"])
        except Exception, e:
            print "Ignoring equipment: %s: %s " % (file, e)
            continue

    return equipment


def flatten_dict(dict, index, size):
    a = [ None ] * (size + 1)

    for k in dict.keys():
        try:
            i = int(k)
            a[i] = dict[k][index]
        except:
            continue

    return a

def normalize(list):
    m = max(list)
    a = []
    for i in list:
        if i is not None:
            a.append(float(i)/m)
        else:
            a.append(None)
    return a

if __name__ == "__main__":
    try:
        os.mkdir(GRAPHS_DIR)
    except Exception:
        pass

    equipment = load_equipment()
    scenarios = None
    try:
        with open(RAW_STATS_FILE, "r") as f:
            scenarios = json.load(f)
    except Exception, e:
        print ("Cannot process file %s ! Aborting" % RAW_STATS_FILE)

    scen_count = 0
    turn_count = 0
    total_turn_stats = []
    for scenario in scenarios:
        scen_count += 1
        scen_stats = {}
        max_turn = -1
        scen_total_units = []
        scen_existing_turns = 0
        scen_turn_occurences = 0

        print ("* Processing scenario: %s" % scenario)
        for turn in scenarios[scenario]:
            data = scenarios[scenario][turn]
            turn_occurences = data["occurences"]
            turn_count += turn_occurences
            scen_turn_occurences += turn_occurences
            scen_existing_turns += 1

            prestige_std = numpy.std(data["prestige"])
            prestige_mean = numpy.mean(data["prestige"])

            score_std = numpy.std(data["score"])
            score_mean = numpy.mean(data["score"])

            totals = data["totals"]
            units = totals["units"]
            nr_units = float(len(units))
            damaged_per = totals["damaged"]/nr_units
            strength_mean = totals["strength"]/nr_units
            moved_per = totals["moved"]/nr_units
            noammo_per = totals["noammo"]/nr_units
            entrenched_per = totals["entrenched"]/nr_units
            entrenchment_mean = totals["entrenchment"]/nr_units
            nofuel_per = totals["nofuel"]/nr_units
            spotted_per = totals["spotted"]/nr_units
            experience_mean = totals["experience"]/nr_units
            fired_per = totals["fired"]/nr_units
            hits_mean = totals["hits"]/nr_units
            supply_per = totals["supply"]/nr_units
            surprised_per = totals["surprised"]/nr_units
            transporting_per = totals["transporting"]/nr_units
            nr_units_mean = nr_units/turn_occurences
            ai_score_per = ((damaged_per * 4) + (surprised_per * 7) + (moved_per * 2) + \
                            (noammo_per * 3) + (nofuel_per * 3) + (spotted_per * 4) - (fired_per * 2) + \
                            (hits_mean * 2)) / (4 + 7 + 2 + 3 + 3 + 4 + 2 + 2)

            scen_total_units += units
            scen_stats[turn] = [
                prestige_mean,#0
                prestige_std,
                score_mean, #2
                score_std,
                damaged_per, #4
                strength_mean,
                moved_per, #6
                noammo_per, #7
                entrenched_per,
                entrenchment_mean,
                nofuel_per, #10
                spotted_per, #11
                experience_mean,
                fired_per,
                hits_mean,
                supply_per,
                surprised_per,
                transporting_per,
                nr_units_mean, #18
                turn_occurences,
                ai_score_per,
            ]

            if int(turn) > 0 and int(turn) < 26 and score_mean < 100000 and nr_units_mean < 1000:
                total_turn_stats.append([int(turn), int(nr_units_mean), int(score_mean)])

            if int(turn) > max_turn:
                max_turn = int(turn)

        if SKIP_SCENARIO_GRAPHS:
            continue

        # Generate frequency of unit classes from scenario units equipment ids
        units_classes = {}

        for unit in scen_total_units:
            c = equipment[str(unit)][8]
            cname = UNIT_CLASS_NAMES[c]
            if cname not in units_classes:
                units_classes[cname] = 1
            else:
                units_classes[cname] += 1

        # normalize with turn occurences
        units_scen_proportion = (scen_turn_occurences/scen_existing_turns)
        for uclass in units_classes:
            units_classes[uclass] /= units_scen_proportion


        units_classes = sorted(units_classes.items(), key=lambda x:x[1], reverse=True) # will transform to list of tuples

        units_classes_names, units_classes_freq = zip(*units_classes)

        # Generate frequency of units (using numpy)
        units_count = numpy.bincount(scen_total_units)
        units_eqid = numpy.nonzero(units_count)[0]
        top_scenario_units = zip(units_eqid, units_count[units_eqid])
        top_scenario_units.sort(key=lambda x: x[1], reverse=True) # sort high to low
        top5_scenario_units = top_scenario_units[:10] # top 5
        # convert eqid to unit name 21th element on equipment
        top5_scenario_units = [(equipment[str(x[0])][21], x[1]) for x in top5_scenario_units]
        units_eqids = zip(*top5_scenario_units)[0]
        units_freq = zip(*top5_scenario_units)[1]

        x = range(-1, max_turn)

        fig = plt.figure(figsize=(14, 18))
        g1 = plt.subplot(411)
        plt.title(scenario + ": player army changes")
        g1.plot(x, normalize(flatten_dict(scen_stats, 0, max_turn)), 'b-', label='prestige', linewidth=2.0)
        g1.plot(x, normalize(flatten_dict(scen_stats, 2, max_turn)), 'r-', label='score', linewidth=2.0)
        g1.plot(x, normalize(flatten_dict(scen_stats, 18, max_turn)), 'y--', label='nr units', linewidth=2.0)
        g1.plot(x, flatten_dict(scen_stats, 15, max_turn), 'g--', label='resupply', linewidth=2.0)
        plt.xlabel("Turn number")
        plt.xticks(range(0, max_turn, 1))
        plt.legend()

        g2 = plt.subplot(412)
        x_pos = numpy.arange(len(units_eqids))
        slope, intercept = numpy.polyfit(x_pos, units_freq, 1)
        trendline = intercept + (slope * x_pos)
        g2.plot(x_pos, trendline, color='red', linestyle='--')
        sns.barplot(x_pos, units_freq)
        plt.xticks(x_pos, units_eqids)
        plt.ylabel('Frequency of units')

        g3 = plt.subplot(413)
        x_pos = numpy.arange(len(units_classes_names))
        slope, intercept = numpy.polyfit(x_pos, units_classes_freq, 1)
        trendline = intercept + (slope * x_pos)
        g3.plot(x_pos, trendline, color='red', linestyle='--')
        sns.barplot(x_pos, units_classes_freq)
        plt.xticks(x_pos, units_classes_names)
        plt.ylabel('Frequency of unit classes')

        g4 = plt.subplot(414)
        g4.plot(x, flatten_dict(scen_stats, 1, max_turn), 'b-', label='sigma prestige', linewidth=2.0)
        g4.plot(x, flatten_dict(scen_stats, 3, max_turn), 'r-', label='sigma score', linewidth=2.0)
        plt.xlabel("Turn number")
        plt.legend()
        plt.xticks(range(0, max_turn, 1))

        #g2.scatter(flatten_dict(scen_stats, 2, max_turn), flatten_dict(scen_stats, 0, max_turn))
        #plt.xlabel("score")
        #plt.ylabel("prestige")
        #plt.show()

        graph_file_name = "%s %d turns (1)" % (scenario, max_turn)
        fig.savefig(os.path.join(GRAPHS_DIR, graph_file_name), bbox_inches='tight')
        plt.cla()
        plt.close(fig)

        fig = plt.figure(figsize=(14, 14))
        g1 = plt.subplot(411)
        plt.title(scenario + ': turn statistics')
        g1.plot(x, flatten_dict(scen_stats, 4, max_turn), 'b-', label='damaged', linewidth=2.0)
        g1.plot(x, flatten_dict(scen_stats, 6, max_turn), 'r-', label='moved', linewidth=2.0)
        g1.plot(x, flatten_dict(scen_stats, 11, max_turn), 'y--', label='spotted', linewidth=2.0)
        plt.xlabel("Turn number")
        plt.xticks(range(0, max_turn, 1))
        plt.legend()

        g2 = plt.subplot(412)
        g2.plot(x, flatten_dict(scen_stats, 7, max_turn), 'b-', label='no ammo', linewidth=2.0)
        g2.plot(x, flatten_dict(scen_stats, 10, max_turn), 'r-', label='no fuel', linewidth=2.0)
        g2.plot(x, flatten_dict(scen_stats, 15, max_turn), 'y--', label='resupplied', linewidth=2.0)
        plt.xlabel("Turn number")
        plt.xticks(range(0, max_turn, 1))
        plt.legend()

        g3 = plt.subplot(413)
        g3.plot(x, flatten_dict(scen_stats, 6, max_turn), 'r-', label='moved', linewidth=2.0)
        g3.plot(x, flatten_dict(scen_stats, 16, max_turn), 'b-', label='moved in transport', linewidth=2.0)
        g3.plot(x, flatten_dict(scen_stats, 17, max_turn), 'y--', label='surprised', linewidth=2.0)
        plt.xlabel("Turn")
        plt.xticks(range(0, max_turn, 1))
        plt.legend()

        g4 = plt.subplot(414)
        g4.plot(x, flatten_dict(scen_stats, 4, max_turn), 'r-', label='damaged', linewidth=2.0)
        g4.plot(x, flatten_dict(scen_stats, 13, max_turn), 'b-', label='fired', linewidth=2.0)
        g4.plot(x, flatten_dict(scen_stats, 14, max_turn), 'y--', label='hits avg', linewidth=2.0)
        plt.xlabel("Turn number")
        plt.xticks(range(0, max_turn, 1))
        plt.legend()

        graph_file_name = "%s %d turns (2)" % (scenario, max_turn)
        fig.savefig(os.path.join(GRAPHS_DIR, graph_file_name), bbox_inches='tight')
        plt.cla()
        plt.close(fig)

        fig = plt.figure(figsize=(14, 14))
        g1 = plt.subplot(211)
        plt.title(scenario + ": AI performance")
        ai_performance = flatten_dict(scen_stats, 20, max_turn)
        x_pos = numpy.arange(len(ai_performance))
        sns.barplot(x_pos, ai_performance)
        g1.plot(x, normalize(flatten_dict(scen_stats, 5, max_turn)), 'b-', label='player army strength', linewidth=2.0)
        g1.plot(x, normalize(flatten_dict(scen_stats, 18, max_turn)), 'y--', label='nr units', linewidth=2.0)
        plt.xlabel("Turn number")
        plt.ylabel('AI performance')
        plt.xticks(range(0, max_turn, 1))
        plt.legend()

        g2 = plt.subplot(212)
        sns.barplot(x_pos, ai_performance)
        g2.plot(x, normalize(flatten_dict(scen_stats, 0, max_turn)), 'b-', label='player prestige', linewidth=2.0)
        g2.plot(x, normalize(flatten_dict(scen_stats, 2, max_turn)), 'y--', label='player score', linewidth=2.0)
        plt.xlabel("Turn number")
        plt.xticks(range(0, max_turn, 1))
        plt.ylabel('AI performance')
        plt.legend()

        graph_file_name = "%s %d turns (3)" % (scenario, max_turn)
        fig.savefig(os.path.join(GRAPHS_DIR, graph_file_name), bbox_inches='tight')
        plt.cla()
        plt.close(fig)


    # Regression
    regr_turns =  [i[0] for i in total_turn_stats]
    regr_nr_units = [i[1] for i in total_turn_stats]
    regr_score = [i[2] for i in total_turn_stats]
    regr = pd.DataFrame({
        'turn': regr_turns,
        'nr_units': regr_nr_units,
        'score': regr_score
        })


    #http://stackoverflow.com/questions/28239359/showing-data-and-model-predictions-in-one-plot-using-seaborn-and-statsmodels
    pal = sns.cubehelix_palette(4, 1.5, .75, light=.6, dark=.2)
    #tips = sns.load_dataset("tips")
    g = sns.lmplot(x="turn", y="nr_units", data=regr, palette=pal)
    #g = sns.lmplot(x="tip", y="total_bill", data=tips, palette=pal)
    g.set_axis_labels("Turn number", "Number of units")

    graph_file_name = "General - Units per turn regression.png"
    g.savefig(os.path.join(GRAPHS_DIR, graph_file_name))
    plt.cla()

    g = sns.lmplot(x="turn", y="score", data=regr, palette=pal)
    g.set_axis_labels("Turn number", "Player Score")

    graph_file_name = "General - Score per turn regression.png"
    g.savefig(os.path.join(GRAPHS_DIR, graph_file_name))
    plt.cla()


    print("Processed %d scenarios and a %d turns" % (scen_count, turn_count))
