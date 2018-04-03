from profiles.common import *

config = BuildConfig(defaultConfig)
config["includeFiles"].append("manifest.webapp")
config["selectedCampaigns"] = ["023.json", "056.json"]
config["buildPrefix"] = "firefox-debug-"
config["platform"] = "generic"
config["useCompiled"] = False
