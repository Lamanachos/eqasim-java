package org.eqasim.ile_de_france.dr_um;

import org.eqasim.core.components.config.ConfigAdapter;
import org.eqasim.core.components.config.EqasimConfigGroup;
import org.eqasim.ile_de_france.IDFConfigurator;
import org.eqasim.ile_de_france.mode_choice.IDFModeChoiceModule;
import org.matsim.api.core.v01.TransportMode;
import org.matsim.contribs.discrete_mode_choice.modules.DiscreteModeChoiceModule;
import org.matsim.contribs.discrete_mode_choice.modules.config.DiscreteModeChoiceConfigGroup;
import org.matsim.core.config.CommandLine.ConfigurationException;
import org.matsim.core.config.Config;
import org.matsim.core.config.groups.PlansConfigGroup;
import org.matsim.core.config.groups.ReplanningConfigGroup;
import org.matsim.core.config.groups.ReplanningConfigGroup.StrategySettings;
import org.matsim.core.config.groups.RoutingConfigGroup;
import org.matsim.core.config.groups.ScoringConfigGroup;

import java.util.Arrays;

import static org.matsim.core.config.groups.PlansConfigGroup.TripDurationHandling.shiftActivityEndTimes;

public class RunAdaptConfig_CarInternal {
	String sc_name;
	static public void runAdaptConfiguration(String sc_name, String residents) throws ConfigurationException {
		String input_path = "ile_de_france\\scenarios\\" + sc_name + "\\ile_de_france_config.xml";
		String output_path = "ile_de_france\\scenarios\\"+sc_name+"\\ile_de_france_config_carInternal.xml";
		String[] args = new String[] {"--input-path", input_path,
				"--output-path", output_path};
		IDFConfigurator configurator = new IDFConfigurator();
		if (residents.equals("yes")) {
			ConfigAdapter.run(args, configurator.getConfigGroups(), RunAdaptConfig_CarInternal::adaptConfigurationRes);
		}
		else {
			ConfigAdapter.run(args, configurator.getConfigGroups(), RunAdaptConfig_CarInternal::adaptConfigurationNoRes);
		}
	}

	static public void adaptConfigurationNoRes(Config config) {
		// Adjust eqasim config
		EqasimConfigGroup eqasimConfig = EqasimConfigGroup.get(config);

		eqasimConfig.setCostModel(TransportMode.car, IDFModeChoiceModule.CAR_COST_MODEL_NAME);
		eqasimConfig.setCostModel(TransportMode.pt, IDFModeChoiceModule.PT_COST_MODEL_NAME);

		eqasimConfig.setEstimator(TransportMode.car, IDFModeChoiceModule.CAR_ESTIMATOR_NAME);
		eqasimConfig.setEstimator(TransportMode.bike, IDFModeChoiceModule.BIKE_ESTIMATOR_NAME);

		config.network().setInputFile("ile_de_france_network_carInternal.xml.gz");
		//BYIN:
		// Routing config
		RoutingConfigGroup routingConfig = config.routing();
		PlansConfigGroup plansConfigGroup = config.plans();
		plansConfigGroup.setTripDurationHandling(shiftActivityEndTimes);
		//and others
		//strategyConfig.setFractionOfIterationsToDisableInnovation(0.8);

		DiscreteModeChoiceConfigGroup dmcConfig = (DiscreteModeChoiceConfigGroup) config.getModules()
				.get(DiscreteModeChoiceConfigGroup.GROUP_NAME);
		dmcConfig.setModeAvailability(IDFModeChoiceModule.MODE_AVAILABILITY_NAME);

		//BYIN: we consider mode choice strategy without sizeofMemories = 1
//		dmcConfig.setEnforceSinglePlan(false);
		ScoringConfigGroup scoringConfig = config.scoring();
		scoringConfig.setMarginalUtlOfWaitingPt_utils_hr(-1.0);

		// Calibration results for 5%
		if (eqasimConfig.getSampleSize() == 0.05) {
			// Adjust flow and storage capacity
			config.qsim().setFlowCapFactor(0.045);
			config.qsim().setStorageCapFactor(0.045);
		}
	}
	static public void adaptConfigurationRes(Config config) {
		// Adjust eqasim config
		EqasimConfigGroup eqasimConfig = EqasimConfigGroup.get(config);

		eqasimConfig.setCostModel(TransportMode.car, IDFModeChoiceModule.CAR_COST_MODEL_NAME);
		eqasimConfig.setCostModel(TransportMode.pt, IDFModeChoiceModule.PT_COST_MODEL_NAME);

		eqasimConfig.setEstimator(TransportMode.car, IDFModeChoiceModule.CAR_ESTIMATOR_NAME);
		eqasimConfig.setEstimator(TransportMode.bike, IDFModeChoiceModule.BIKE_ESTIMATOR_NAME);

		config.network().setInputFile("ile_de_france_network_carInternal.xml.gz");
		config.plans().setInputFile("ile_de_france_population_carInternal_residentOnly.xml.gz");
		//BYIN:
		// Routing config
		RoutingConfigGroup routingConfig = config.routing();
		routingConfig.setNetworkModes(Arrays.asList("car", "car_passenger", "truck", "carInternal"));

		PlansConfigGroup plansConfigGroup = config.plans();
		plansConfigGroup.setTripDurationHandling(shiftActivityEndTimes);

		//BYIN: strategy settings:
		//Replace default strategy settings in eqasim considering DRZ
		for (StrategySettings ss : config.replanning().getStrategySettings()) {
			if (ss.getStrategyName().equals(DiscreteModeChoiceModule.STRATEGY_NAME)) {
				ss.setSubpopulation("personExternal");
				ss.setWeight(0.05);
			}
			if (ss.getStrategyName().equals("KeepLastSelected")) {
//				ss.setStrategyName("ChangeExpBeta");
				ss.setSubpopulation("personExternal");
				ss.setWeight(0.95);
			}
		}

		//1-1) for subpopulation = personInternal
		StrategySettings strategySettings_mode_int = new StrategySettings();
		strategySettings_mode_int.setStrategyName("DiscreteModeChoice");  //others: ReRoute, TimeAllocationMutator
		strategySettings_mode_int.setSubpopulation("personInternal");
		strategySettings_mode_int.setWeight(0.05);

		StrategySettings strategySettings_mode_int2 = new StrategySettings();
		strategySettings_mode_int2.setStrategyName("KeepLastSelected");  //ChangeExpBeta
		strategySettings_mode_int2.setSubpopulation("personInternal");
		strategySettings_mode_int2.setWeight(0.95);

		ReplanningConfigGroup strategyConfig = config.replanning();
		strategyConfig.addStrategySettings(strategySettings_mode_int);
		strategyConfig.addStrategySettings(strategySettings_mode_int2);
		//and others
		//strategyConfig.setFractionOfIterationsToDisableInnovation(0.8);

		DiscreteModeChoiceConfigGroup dmcConfig = (DiscreteModeChoiceConfigGroup) config.getModules()
				.get(DiscreteModeChoiceConfigGroup.GROUP_NAME);
		dmcConfig.setModeAvailability(IDFModeChoiceModule.MODE_AVAILABILITY_NAME);

		//BYIN: we consider mode choice strategy without sizeofMemories = 1
//		dmcConfig.setEnforceSinglePlan(false);
		ScoringConfigGroup scoringConfig = config.scoring();
		scoringConfig.setMarginalUtlOfWaitingPt_utils_hr(-1.0);

		// Calibration results for 5%
		if (eqasimConfig.getSampleSize() == 0.05) {
			// Adjust flow and storage capacity
			config.qsim().setFlowCapFactor(0.045);
			config.qsim().setStorageCapFactor(0.045);
		}
	}
}
