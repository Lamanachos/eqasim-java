package org.eqasim.ile_de_france.intermodality;

import org.eqasim.core.components.ParkRideManager;
import org.eqasim.core.components.car_pt.routing.EqasimCarPtModule;
import org.eqasim.core.components.car_pt.routing.EqasimPtCarModule;
import org.eqasim.core.components.config.EqasimConfigGroup;
import org.eqasim.core.simulation.analysis.EqasimAnalysisModule;
import org.eqasim.core.simulation.mode_choice.EqasimModeChoiceModuleCarPt;
import org.eqasim.core.tools.TestCarPtPara;
import org.eqasim.ile_de_france.IDFConfigurator;
import org.eqasim.ile_de_france.mode_choice.IDFModeChoiceModule;
import org.eqasim.ile_de_france.mode_choice.IDFModeChoiceModuleCarPt;
import org.matsim.api.core.v01.Coord;
import org.matsim.api.core.v01.Id;
import org.matsim.api.core.v01.Scenario;
import org.matsim.api.core.v01.network.Network;
import org.matsim.api.core.v01.population.*;
import org.matsim.contribs.discrete_mode_choice.modules.config.DiscreteModeChoiceConfigGroup;
import org.matsim.core.config.CommandLine;
import org.matsim.core.config.CommandLine.ConfigurationException;
import org.matsim.core.config.Config;
import org.matsim.core.config.ConfigUtils;
import org.matsim.core.config.groups.ReplanningConfigGroup;
import org.matsim.core.config.groups.RoutingConfigGroup;
import org.matsim.core.config.groups.ScoringConfigGroup;
import org.matsim.core.config.groups.ScoringConfigGroup.ActivityParams;
import org.matsim.core.config.groups.ScoringConfigGroup.ModeParams;
import org.matsim.core.config.groups.QSimConfigGroup;
import org.matsim.core.controler.Controler;
import org.matsim.core.controler.OutputDirectoryHierarchy;
import org.matsim.core.scenario.ScenarioUtils;
import org.matsim.pt.config.TransitConfigGroup;
import org.matsim.vehicles.VehicleType;
import org.matsim.vehicles.VehiclesFactory;

import java.io.IOException;
import java.util.*;

public class RunSimulationCarPt_DrivingRestriction {

	static public void main(String[] args) throws ConfigurationException, IOException {
		String locationFile = "ile_de_france/scenarios/parcs-relais-idf_rer_train_outside_paris.csv";
		double car_pt_constant = 0.75;

		CommandLine cmd = new CommandLine.Builder(args) //
				.requireOptions("config-path","residents") //
				.allowPrefixes("mode-choice-parameter", "cost-parameter") //
				.build();
		//Get res or not
		String residents = cmd.getOptionStrict("residents");

		//Get config
		IDFConfigurator configurator = new IDFConfigurator();
		Config config = ConfigUtils.loadConfig(cmd.getOptionStrict("config-path"), configurator.getConfigGroups());
		configurator.addOptionalConfigGroups(config);

		//modify some parameters in config file
		config.controller().setOverwriteFileSetting(OutputDirectoryHierarchy.OverwriteFileSetting.deleteDirectoryIfExists);

		// multi-stage car trips
		config.routing().setAccessEgressType(RoutingConfigGroup.AccessEgressType.accessEgressModeToLink);
		config.qsim().setUsingTravelTimeCheckInTeleportation( true );

		//transit (UM)
		//TransitConfigGroup transitConfig = config.transit();
		//transitConfig.setBoardingAcceptance(TransitConfigGroup.BoardingAcceptance.checkStopOnly);


		//1) driving restriction setting
		//UM : config.network().setInputFile("ile_de_france_network_carInternal.xml.gz");
		//UM : config.plans().setInputFile("ile_de_france_population_carInternal_residentOnly.xml.gz");  //ile_de_france_population_carInternal_residentOnly.xml.gz
		//config.vehicles().setVehiclesFile("ile_de_france_vehicles.xml.gz");
		//config.qsim().setVehiclesSource(QSimConfigGroup.VehiclesSource.modeVehicleTypesFromVehiclesData);  //original value is defaultVehicle
		//config.qsim().setVehiclesSource(QSimConfigGroup.VehiclesSource.defaultVehicle);  //UM
		//BYIN: qsim visulasation (can be shown in via) : can also put this setting in RunAdaptConfig_CarInternal.java

		//Get configs
		ScoringConfigGroup scoringConfig = config.scoring();
		EqasimConfigGroup eqasimConfig = EqasimConfigGroup.get(config);

		if (residents.equals("yes")) {
			config.qsim().setMainModes(Arrays.asList("car", "carInternal"));//attention: car_passenger is excluded, corresponding adds in emissionRunner
			// add carInternal to traveltimeCalculator
			Set<String> analyzedModes = new HashSet<>(config.travelTimeCalculator().getAnalyzedModes());
			analyzedModes.add("carInternal");
			config.travelTimeCalculator().setAnalyzedModes(analyzedModes);
		/*for (ReplanningConfigGroup.StrategySettings ss : config.replanning().getStrategySettings()) {
			if (ss.getStrategyName().equals("KeepLastSelected")) {
				ss.setWeight(0.95);
			}
			if (ss.getStrategyName().equals("DiscreteModeChoice")) {
				ss.setWeight(0.05);
			}*/

			//add parameters of the new mode and related: discrete mode choice in eqasim
			// Scoring config
			ModeParams carInternalParams = new ModeParams("carInternal");
			carInternalParams.setMarginalUtilityOfTraveling(-1.0);
			scoringConfig.addModeParams(carInternalParams);
			// consider carInternal as a special car, using the same parameters of car and the same others

			eqasimConfig.setCostModel("carInternal", IDFModeChoiceModule.CAR_COST_MODEL_NAME);
			eqasimConfig.setEstimator("carInternal", IDFModeChoiceModule.CAR_ESTIMATOR_NAME);
		}
		// Eqasim config definition to add the mode car_pt estimation
		eqasimConfig.setEstimator("car_pt", "CarPtUtilityEstimator");
		eqasimConfig.setEstimator("pt_car", "PtCarUtilityEstimator");

		// Scoring config definition to add the mode car_pt parameters
		//PlanCalcScoreConfigGroup scoringConfig = config.planCalcScore();
		ModeParams carPtParams = new ModeParams("car_pt");
		ModeParams ptCarParams = new ModeParams("pt_car");
		scoringConfig.addModeParams(carPtParams);
		scoringConfig.addModeParams(ptCarParams);

		// "car_pt interaction" definition
		ActivityParams paramscarPtInterAct = new ActivityParams("carPt interaction");
		paramscarPtInterAct.setTypicalDuration(100.0);
		paramscarPtInterAct.setScoringThisActivityAtAll(false);

		// "pt_car interaction" definition
		ActivityParams paramsPtCarInterAct = new ActivityParams("ptCar interaction");
		paramsPtCarInterAct.setTypicalDuration(100.0);
		paramsPtCarInterAct.setScoringThisActivityAtAll(false);

		// Adding "car_pt interaction" to the scoring
		scoringConfig.addActivityParams(paramscarPtInterAct);
		scoringConfig.addActivityParams(paramsPtCarInterAct);

		// DMC config definition
		// Adding the mode "car_pt" and "pt_car" to CachedModes
		DiscreteModeChoiceConfigGroup dmcConfig = (DiscreteModeChoiceConfigGroup) config.getModules()
				.get(DiscreteModeChoiceConfigGroup.GROUP_NAME);
		Collection<String> cachedModes = new HashSet<>(dmcConfig.getCachedModes());
		cachedModes.add("car_pt");
		cachedModes.add("pt_car");
		if (residents.equals("yes")) {
			cachedModes.add("carInternal");
		}
		dmcConfig.setCachedModes(cachedModes);

		// Activation of constraint intermodal modes Using
		Collection<String> tourConstraints = new HashSet<>(dmcConfig.getTourConstraints());
		tourConstraints.add("IntermodalModesConstraint");
		dmcConfig.setTourConstraints(tourConstraints);

		if (residents.equals("yes")) {
			dmcConfig.getVehicleTourConstraintConfig().setRestrictedModes(Arrays.asList("car", "carInternal", "bike"));
		}
		else {
			dmcConfig.getVehicleTourConstraintConfig().setRestrictedModes(Arrays.asList("car", "bike"));

		}
		cmd.applyConfiguration(config);
		Scenario scenario = prepareScenario( config, configurator, residents);
		Controler controller = new Controler(scenario);
		configurator.configureController(controller);


		//set Park and ride lot locations
		List<Coord> parkRideCoords;
		readParkRideCoordsFromFile readFile = new readParkRideCoordsFromFile(locationFile);
		parkRideCoords = readFile.readCoords;
		ParkRideManager parkRideManager = new ParkRideManager();
		parkRideManager.setParkRideCoords(parkRideCoords);
		Network network = scenario.getNetwork();
		parkRideManager.setNetwork(network);

		controller.addOverridingModule(new EqasimAnalysisModule());
		controller.addOverridingModule(new EqasimModeChoiceModuleCarPt());
		controller.addOverridingModule(new IDFModeChoiceModuleCarPt(cmd, parkRideCoords, scenario.getNetwork(), scenario.getPopulation().getFactory()));
		controller.addOverridingModule(new EqasimCarPtModule(parkRideCoords));
		controller.addOverridingModule(new EqasimPtCarModule(parkRideCoords));

		TestCarPtPara tp = new TestCarPtPara();
		tp.setPara(car_pt_constant);
		String outputPath = controller.getConfig().controller().getOutputDirectory();
		tp.setCarPtSavePath(outputPath);
		controller.run();
	}

	private static Scenario prepareScenario(Config config, IDFConfigurator configurator, String residents) {
		final Scenario scenario = ScenarioUtils.createScenario( config );

		if (residents.equals("yes")) {
			// Add carInternal vehicle type
			VehiclesFactory vehiclesFactory = scenario.getVehicles().getFactory();
			VehicleType carInternalVehicleType = vehiclesFactory.createVehicleType(Id.create("carInternal", VehicleType.class));
			scenario.getVehicles().addVehicleType(carInternalVehicleType);
		}

		configurator.configureScenario(scenario);
		ScenarioUtils.loadScenario(scenario);
		configurator.adjustScenario(scenario);
		// Delete all initial links and routes in the plan
		for (Person person : scenario.getPopulation().getPersons().values()) {
			for (Plan plan : person.getPlans()) {
				for (PlanElement pe : plan.getPlanElements()) {
					if (pe instanceof Activity) {
						((Activity) pe).setLinkId(null);
					} else if (pe instanceof Leg) {
						((Leg) pe).setRoute(null);
					} else {
						throw new RuntimeException("Plan element can either be activity or leg.");
					}
				}
			}
		}

		return scenario;
	}

}