from profiles.common import *

config = BuildConfig(defaultConfig)
config["buildPrefix"] = "web-debug-"
config["selectedCampaigns"] = ["023.json", "056.json"]
config["platform"] = "generic"
config["useCompiled"] = False
