# Using eqasim to get the output_emissions_events file (how I did it, could be wrong)
## 1) Get your output folder from a simulation
Should contain at least :
 - output_events.xml.gz
 - output_network.xml.gz
 - output_facilities.xml.gz
 - output_households.xml.gz
 - output_transitSchedule.xml.gz
 - output_transitVehicles.xml.gz
 - output_vehicles.xml.gz
 - output_plans.xml.gz
 - output_config.xml
## 2) Modify your config file
- Set "outputDirectory" to an existing directory in your system
- "routingAlgorithmType" cannot be "FastAStarLandmarks" but can be "AStarLandmarks"
- comment parameter "travelTimeCalculator" in "travelTimeCalculator" module
- replace each filename by the output one in the config file (ex : "ile_de_france_events.xml.gz -> "output_events.xml.gz)
## 3) Add some code to RunComputeEmissionsEvents.java
- Add this line 83 :
  ```java
  if (NetworkUtils.getType(link).contains("pedestrian")) {
      NetworkUtils.setType(link, "unclassified");
  }
  if (NetworkUtils.getType(link).contains("construction")) {
      NetworkUtils.setType(link, "unclassified");
  }
  if (NetworkUtils.getType(link).contains("busway")) {
      NetworkUtils.setType(link, "unclassified");
  }
  if (NetworkUtils.getType(link).contains("footway")) {
      NetworkUtils.setType(link, "unclassified");
  }
  if (NetworkUtils.getType(link).contains("cycleway")) {
      NetworkUtils.setType(link, "unclassified");
  }
  ```
- Line 50, replace "tryDetailedThenTechnologyAverageThenAverageTable" by "directlyTryAverageTable"
## 4) Run
Run RunComputeEmissionsEvents.java with this config, replacing each argument by the localisation of the files :

`
--config-path
simulation_output/simout_IdF_egt1pct_rpf2019_it100/emissions_config.xml
`

`
--hbefa-cold-avg
../../HBEFA/2022_IDF_EFA_ColdStart_Vehcat_Average_OnlyCar_Marjolaine.csv
`

`
--hbefa-hot-avg
../../HBEFA/2022_IDF_EFA_HOT_Vehcat_Average_OnlyCar_Marjolaine.csv
`

