# Get emissions
In both cases you need an output folder that should contain at least :
 - output_events.xml.gz
 - output_network.xml.gz
 - output_facilities.xml.gz
 - output_households.xml.gz
 - output_transitSchedule.xml.gz
 - output_transitVehicles.xml.gz
 - output_vehicles.xml.gz
 - output_plans.xml.gz
 - output_config.xml (only in the first case probably)
## Using eqasim to get the output_emissions_events file (how I did it, could be wrong)
Uses Matsim 2025
### 1) Modify your config file
- Set "outputDirectory" to an existing directory in your system
- "routingAlgorithmType" cannot be "FastAStarLandmarks" but can be "AStarLandmarks"
- comment parameter "travelTimeCalculator" in "travelTimeCalculator" module
- replace each filename by the output one in the config file (ex : "ile_de_france_events.xml.gz -> "output_events.xml.gz)
### 2) Add some code to RunComputeEmissionsEvents.java
The file is located at `.\core\src\main\java\org\eqasim\core\components\emissions\RunComputeEmissionsEvents.java`
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
### 3) Run
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
## Using Biao's code
Uses Matsim 13.0
### 1) Clone the git repo 
```bash
https://github.com/lvmt-matsim/eqasim-java/tree/lvmt_emission
```
Open in IntelliJ and switch to branch lvmt_emission
### 2) Modify some values
The file is located at `org/eqasim/ile_de_france/emission/RunAverageOfflineAirPollution_v13.java`
At the beginning of RunAverageOfflineAirPollution_v13.java, modify scenarioID to the name of the folder containing your data and outputPath to the location of this folder (without it's name).
Comment lines 60 and 61 :
```java
config.vehicles().setVehiclesFile(inputFilePath + "./output_vehicles_modified.xml");
config.vehicles().setVehiclesFile(inputFilePath + "./output_vehicles.xml.gz");
```
Verify that these lines are pointing to existing files :
```java
config.vehicles().setVehiclesFile(outputPath + "./output_vehicles.xml.gz");
config.network().setInputFile(outputPath+ "./output_network.xml.gz");
config.plans().setInputFile(outputPath + "./output_plans.xml.gz");
```
### 3) Run
With java 11. No need for any special argument.
