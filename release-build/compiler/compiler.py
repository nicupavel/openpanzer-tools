#!/usr/bin/python
#https://bitbucket.org/npavel/openpanzer/downloads/compiler.jar
from subprocess import call

def compile(rootDir, compilerDir, hasGenerated):

    COMPILER = ["java", "-jar", compilerDir + "compiler.jar"]

    FILES = [
        rootDir + "js/gamestate.js",
        rootDir + "js/combatlog.js",
        rootDir + "js/equipment.js",
        rootDir + "js/dom.js",
        rootDir + "js/ai.js",
        rootDir + "js/aiscripted.js",
        rootDir + "js/style.js",
        rootDir + "js/sound.js",
        rootDir + "js/animation.js",
        rootDir + "js/gamerules.js",
        rootDir + "js/unit.js",
        rootDir + "js/map.js",
        rootDir + "js/scenarioloader.js",
        rootDir + "js/render.js",
        rootDir + "js/scenario.js",
        rootDir + "js/campaign.js",
        rootDir + "js/uibuilder.js",
        rootDir + "js/ui.js",
        rootDir + "js/uicombatlog.js",
        rootDir + "js/game.js",
        rootDir + "js/osglue.js",
        rootDir + "js/leaders.js"
    ]

    OPTS = [
        "--js_output_file", rootDir + "js/openpanzer.js",
        "--language_in", "ECMASCRIPT5",
        "--compilation_level", "SIMPLE_OPTIMIZATIONS",
        "--summary_detail_level", "3",
    ]

    if hasGenerated:
        FILES.insert(0, "./generated-prototypes.js")
    else:
        FILES.insert(0, rootDir + "js/prototypes.js",)
    
    ARGS = COMPILER + FILES + OPTS
    call(ARGS)

if __name__ == "__main__":
    compile("../../../", "../compiler/", False)

