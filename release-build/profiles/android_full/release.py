from profiles.common import *

config = BuildConfig(defaultConfig)
#config["includeFiles"].append("manifest.json")
config["includeFiles"].append("resources/ui/splash/splash-android-1x.png")
config["includeFiles"].append("resources/ui/splash/splash-android-2x.png")
config["selectedCampaigns"] = ["018.json","023.json", "056.json", "062d.json"]
config["buildPrefix"] = "android-release-"
config["platform"] = "generic"
