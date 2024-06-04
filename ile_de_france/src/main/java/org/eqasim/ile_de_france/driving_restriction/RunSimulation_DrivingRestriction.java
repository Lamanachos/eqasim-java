package org.eqasim.ile_de_france.driving_restriction;

import org.eqasim.core.components.config.EqasimConfigGroup;
import org.eqasim.core.simulation.analysis.EqasimAnalysisModule;
import org.eqasim.core.simulation.mode_choice.EqasimModeChoiceModule;
import org.eqasim.ile_de_france.IDFConfigurator;
import org.eqasim.ile_de_france.mode_choice.IDFModeChoiceModule;
import org.matsim.api.core.v01.Id;
import org.matsim.api.core.v01.Scenario;
import org.matsim.api.core.v01.population.*;
import org.matsim.contribs.discrete_mode_choice.modules.config.DiscreteModeChoiceConfigGroup;
import org.matsim.core.config.CommandLine;
import org.matsim.core.config.CommandLine.ConfigurationException;
import org.matsim.core.config.Config;
import org.matsim.core.config.ConfigUtils;
import org.matsim.core.config.groups.ReplanningConfigGroup;
import org.matsim.core.config.groups.RoutingConfigGroup;
import org.matsim.core.config.groups.ScoringConfigGroup;
import org.matsim.core.config.groups.ScoringConfigGroup.ModeParams;
import org.matsim.core.config.groups.QSimConfigGroup;
import org.matsim.core.controler.Controler;
import org.matsim.core.controler.OutputDirectoryHierarchy;
import org.matsim.core.scenario.ScenarioUtils;
import org.matsim.vehicles.VehicleType;
import org.matsim.vehicles.VehiclesFactory;

import java.io.FileWriter;
import java.io.IOException;
import java.io.PrintWriter;
import java.util.Arrays;
import java.util.Collection;
import java.util.HashSet;
import java.util.Set;

import static java.lang.Integer.max;

public class RunSimulation_DrivingRestriction {
	static public void main(String[] args) throws ConfigurationException, IOException {
		args = new String[] {"--config-path", "ile_de_france/scenarios/ile-de-france-1pm/driving_restriction/ile_de_france_config_carInternal.xml"};

		CommandLine cmd = new CommandLine.Builder(args) //
				.requireOptions("config-path") //
				.allowPrefixes("mode-choice-parameter", "cost-parameter") //
				.build();
		IDFConfigurator configurator = new IDFConfigurator();
		Config config = ConfigUtils.loadConfig(cmd.getOptionStrict("config-path"), configurator.getConfigGroups());

		//modify some parameters in config file
		config.controller().setLastIteration(2);
		config.controller().setOverwriteFileSetting(OutputDirectoryHierarchy.OverwriteFileSetting.deleteDirectoryIfExists);

		// multistage car trips
		config.routing().setAccessEgressType(RoutingConfigGroup.AccessEgressType.accessEgressModeToLink);
		config.qsim().setUsingTravelTimeCheckInTeleportation( true );


		//1) driving restriction setting
		config.vehicles().setVehiclesFile("vehicle_types.xml");
		config.network().setInputFile("ile_de_france_network_carInternal.xml.gz");
		config.plans().setInputFile("ile_de_france_population_carInternal_residentOnly.xml.gz");
		config.qsim().setVehiclesSource(QSimConfigGroup.VehiclesSource.modeVehicleTypesFromVehiclesData);  //original value is defaultVehicle
		//BYIN: qsim visulasation (can be shown in via) : can also put this setting in RunAdaptConfig_CarInternal.java
		config.qsim().setMainModes(Arrays.asList("car","carInternal"));// corresponding adds in emissionRunner

		Set<String> analyzedModes = new HashSet<> (config.travelTimeCalculator().getAnalyzedModes());
		analyzedModes.add("carInternal");
		config.travelTimeCalculator().setAnalyzedModes(analyzedModes);

		//for original setting
		for (ReplanningConfigGroup.StrategySettings ss : config.replanning().getStrategySettings()) {
			if (ss.getStrategyName().equals("KeepLastSelected")) {
				ss.setWeight(0.95);
			}
			if (ss.getStrategyName().equals("DiscreteModeChoice")) {
				ss.setWeight(0.05);
			}
		}
		//add parameters of the new mode and related: discrete mode choice in eqasim
		// Scoring config
		ScoringConfigGroup scoringConfig = config.scoring();
		ModeParams carInternalParams = new ModeParams("carInternal");
		scoringConfig.addModeParams(carInternalParams);
		// consider carInternal as a special car, using the same parameters of car and the same others
		EqasimConfigGroup eqasimConfig = EqasimConfigGroup.get(config);
		eqasimConfig.setCostModel("carInternal", IDFModeChoiceModule.CAR_COST_MODEL_NAME);
		eqasimConfig.setEstimator("carInternal", IDFModeChoiceModule.CAR_ESTIMATOR_NAME);

		DiscreteModeChoiceConfigGroup dmcConfig = (DiscreteModeChoiceConfigGroup) config.getModules()
				.get(DiscreteModeChoiceConfigGroup.GROUP_NAME);
		Collection<String> cachedModes = new HashSet<>(dmcConfig.getCachedModes());
		cachedModes.add("carInternal");
		dmcConfig.setCachedModes(cachedModes);
		dmcConfig.getVehicleTourConstraintConfig().setRestrictedModes(Arrays.asList("car", "carInternal", "bike"));

		 //
		cmd.applyConfiguration(config);
		Scenario scenario = prepareScenario( config, configurator );
		Controler controller = new Controler(scenario);

		configurator.configureController(controller);
		controller.addOverridingModule(new EqasimAnalysisModule());
		controller.addOverridingModule(new EqasimModeChoiceModule());
		controller.addOverridingModule(new IDFModeChoiceModule(cmd));

		/*// 1) driving restriction setting : 2nd of 2 parts: Add a new plan strategy module with mode choice: considering the mode carInternal for subpopulation: residents
		controller.addOverridingModule( new AbstractModule() {
			@Override
			public void install() {
				bind(PermissibleModesCalculator.class).to(PermissibleModesCalculatorImpl.class);// for subTourModeChoice in v13
				// define second mode choice strategy: other name: DiscreteModeChoiceInternal? but rename is impossible when setEnforceSinglePlan=true
				this.addPlanStrategyBinding("DiscreteModeChoice").toProvider(new Provider<PlanStrategy>(){
					@Inject
					private GlobalConfigGroup globalConfigGroup;
					@Inject
					private Provider<TripRouter> tripRouterProvider;
					@Inject
					private ActivityFacilities activityFacilities;
					@Inject
					private Provider<DiscreteModeChoiceModel> modeChoiceModelProvider;
					@Inject
					private Provider<TripListConverter> tripListConverterProvider;
					@Inject
					private PopulationFactory populationFactory;
					@Inject
					private PermissibleModesCalculator permissibleModesCalculator;

					@Override  //here is the option of discrete mode choice
					public PlanStrategy get() {

						DiscreteModeChoiceConfigGroup dmcConfig = (DiscreteModeChoiceConfigGroup) config.getModules()
								.get(DiscreteModeChoiceConfigGroup.GROUP_NAME);
						//dmcConfig.setEnforceSinglePlan(true);
						Collection<String> cachedModes = new HashSet<>(dmcConfig.getCachedModes());
						cachedModes.add("carInternal");// doesn't need to set in IDFModeAvailability?
						dmcConfig.setCachedModes(cachedModes);
						dmcConfig.getVehicleTourConstraintConfig().setRestrictedModes(Arrays.asList("car","carInternal", "bike"));

						PlanStrategyImpl.Builder builder = new PlanStrategyImpl.Builder(new RandomPlanSelector<>());
						builder.addStrategyModule(new DiscreteModeChoiceReplanningModule(globalConfigGroup, modeChoiceModelProvider,
								tripListConverterProvider, populationFactory));
						if (dmcConfig.getPerformReroute()) {
							builder.addStrategyModule(new ReRoute(activityFacilities, tripRouterProvider, globalConfigGroup));
						} else {
							builder.addStrategyModule(new CheckConsistentRoutingReplanningModule(globalConfigGroup));
						}

						return builder.build();
					}*/

					// here is the option of subTourModeChoice.
					/*public PlanStrategy get() {

						SubtourModeChoiceConfigGroup modeChoiceConfig = new SubtourModeChoiceConfigGroup() ;
						modeChoiceConfig.setModes( new String[] {TransportMode.walk,TransportMode.pt,"carInternal","car_passenger","bike"} );
						modeChoiceConfig.setChainBasedModes( new String[] {"carInternal","bike"});

						PlanStrategyImpl.Builder builder = new PlanStrategyImpl.Builder(new RandomPlanSelector<>());
						builder.addStrategyModule(new SubtourModeChoice(globalConfigGroup, modeChoiceConfig, permissibleModesCalculator));
						builder.addStrategyModule(new ReRoute(activityFacilities, tripRouterProvider, globalConfigGroup));

						return builder.build();
					}*/
			/*	} ) ;
			}
		} ) ;
*/
		long startTime = System.nanoTime();
		controller.run();
		long endTime = System.nanoTime();
		long duration = (endTime - startTime);
		String outputPath = config.controller().getOutputDirectory();
		long nb_iterations = config.controller().getLastIteration() - config.controller().getFirstIteration();
		nb_iterations += 1;
		FileWriter fileWriter = new FileWriter(outputPath + "/exec_time.txt");
		PrintWriter printWriter = new PrintWriter(fileWriter);
		printWriter.printf("Time taken to execute the sim was %d s\n", duration/1000000000);
		printWriter.printf("Which means an average of %d s per iteration\n", duration/(nb_iterations*1000000000));
		printWriter.close();
	}

	private static Scenario prepareScenario(Config config, IDFConfigurator configurator) {
		final Scenario scenario = ScenarioUtils.createScenario( config );

		// Add carInternal vehicle type
		VehiclesFactory vehiclesFactory = scenario.getVehicles().getFactory();
		VehicleType carInternalVehicleType = vehiclesFactory.createVehicleType(Id.create("carInternal", VehicleType.class));
		scenario.getVehicles().addVehicleType(carInternalVehicleType);

		configurator.configureScenario(scenario);
		ScenarioUtils.loadScenario(scenario);

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