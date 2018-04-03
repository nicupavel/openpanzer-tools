from profiles.common import *

config = BuildConfig(defaultConfig)
#config["includeFiles"].append("manifest.json")
config["includeFiles"].append("resources/ui/splash/splash-android-1x.png")
config["includeFiles"].append("resources/ui/splash/splash-android-2x.png")
config["selectedCampaigns"] = [""]
config["buildPrefix"] = "android-minimal-release-"
config["platform"] = "generic"
