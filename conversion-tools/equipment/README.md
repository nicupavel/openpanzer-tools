# Equipment converter for Open Panzer

The equipment_export.py will look for all **EQUIP97_REPORT.csv** in pg2-panzermarshal/eqp sub folders. 
It will read all these files that it had found and generate json equipment files that are used by Open Panzer.
It will also generate **icons.list** used by uniticons/icons_convert.py to convert unit icons.
 
# Generating EQUIP97_REPORT.csv
 
1. Run PG2 Editor(SuitePG2) (http://luis-guzman.com/downloads.html) 
2. Load *EQUIP97.EQP* in PG2 Editor from the corresponding eqp folder (eg: eqp-adlerkorps/EQUIP97.EQP)
3. Use: **Report Items ALL Data or Known Data** from the editor to generate the *EQUIP97_REPORT.csv* and
save it in the equipment folder (eg: eqp-adlerkorps)


