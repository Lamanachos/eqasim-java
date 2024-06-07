package org.eqasim.ile_de_france.dr_um;

import org.eqasim.core.components.config.ConfigAdapter;
import org.eqasim.core.components.config.EqasimConfigGroup;
import org.eqasim.ile_de_france.IDFConfigurator;
import org.eqasim.ile_de_france.mode_choice.IDFModeChoiceModule;
import org.matsim.api.core.v01.TransportMode;
import org.matsim.contribs.discrete_mode_choice.modules.DiscreteModeChoiceModule;
import org.matsim.contribs.discrete_mode_choice.modules.config.DiscreteModeChoiceConfigGroup;
import org.matsim.core.config.CommandLine;
import org.matsim.core.config.CommandLine.ConfigurationException;
import org.matsim.core.config.Config;
import org.matsim.core.config.groups.PlansConfigGroup;
import org.matsim.core.config.groups.ReplanningConfigGroup;
import org.matsim.core.config.groups.ReplanningConfigGroup.StrategySettings;
import org.matsim.core.config.groups.RoutingConfigGroup;
import org.matsim.core.config.groups.ScoringConfigGroup;

import java.util.Arrays;

import static org.matsim.core.config.groups.PlansConfigGroup.TripDurationHandling.shiftActivityEndTimes;

public class Adapt_config_emissions {
	String sc_name;
	static public void main(String[] args) throws ConfigurationException {
		CommandLine cmd = new CommandLine.Builder(args) //
				.requireOptions("sc_name") //
				.build();
		String sc_name = cmd.getOptionStrict("sc_name");
		String input_path = "simulation_output\\" + sc_name + "\\output_config_reduced.xml";
		String output_path = "simulation_output\\"+sc_name+"\\output_config_emissions.xml";
		String[] args_c = new String[] {"--input-path", input_path,
				"--output-path", output_path};
		IDFConfigurator configurator = new IDFConfigurator();
		ConfigAdapter.run(args_c, configurator.getConfigGroups(), Adapt_config_emissions::adaptConfiguration);
	}
	static public void adaptConfiguration(Config config) {
		// Adjust eqasim config
		EqasimConfigGroup eqasimConfig = EqasimConfigGroup.get(config);
		config.network().setInputFile("output_network.xml.gz");
		config.plans().setInputFile("output_plans.xml.gz");
		config.facilities().setInputFile("output_facilities.xml.gz");
		config.households().setInputFile("output_households.xml.gz");
		config.transit().setTransitScheduleFile("output_transitSchedule.xml.gz");
		config.transit().setVehiclesFile("output_transitVehicles.xml.gz");
		config.vehicles().setVehiclesFile("output_vehicles.xml.gz");
		config.vehicles().setVehiclesFile("output_vehicles.xml.gz");
	}
}
