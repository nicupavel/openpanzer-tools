from profiles.common import *

config = BuildConfig(defaultConfig)
config["buildPrefix"] = "web-release-"
config["selectedCampaigns"] = ["018.json", "023.json", "056.json", "062d.json"]
config["platform"] = "generic"
