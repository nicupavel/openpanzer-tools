from profiles.common import *

config = BuildConfig(defaultConfig)
config["selectedCampaigns"] = ["018.json","023.json", "056.json", "062d.json"]
config["buildPrefix"] = "ios-release-"
config["platform"] = "ios"
