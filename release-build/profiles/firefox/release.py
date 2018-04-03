from profiles.common import *

config = BuildConfig(defaultConfig)
config["includeFiles"].append("manifest.webapp")
config["selectedCampaigns"] = ["018.json", "023.json", "056.json", "062d.json"]
config["buildPrefix"] = "firefox-release-"
config["platform"] = "generic"
