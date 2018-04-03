from profiles.common import *

config = BuildConfig(defaultConfig)
config["selectedCampaigns"] = ["018.json","023.json", "056.json", "062d.json"]
config["buildPrefix"] = "ios-debug-"
config["platform"] = "ios"
config["useCompiled"] = False
config["campaignDebug"] = True

