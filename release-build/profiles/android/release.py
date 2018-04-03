from profiles.common import *

config = BuildConfig(defaultConfig)
#config["includeFiles"].append("manifest.json")
config["includeFiles"].append("resources/ui/splash/splash-android-1x.png")
config["includeFiles"].append("resources/ui/splash/splash-android-2x.png")
config["selectedCampaigns"] = ["023.json", "056.json"] # 056 - 27Mb, 023 - 17M, 018 - 44Mb 062d - 35Mb
config["buildPrefix"] = "android-release-"
config["platform"] = "android"
