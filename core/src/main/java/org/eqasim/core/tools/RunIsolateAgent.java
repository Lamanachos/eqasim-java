package org.eqasim.core.tools;

import java.util.Arrays;
import java.util.Collection;
import java.util.HashSet;

import org.matsim.api.core.v01.Id;
import org.matsim.api.core.v01.Scenario;
import org.matsim.api.core.v01.population.Person;
import org.matsim.core.api.experimental.events.EventsManager;
import org.matsim.core.config.CommandLine;
import org.matsim.core.config.CommandLine.ConfigurationException;
import org.matsim.core.config.Config;
import org.matsim.core.config.ConfigUtils;
import org.matsim.core.events.EventsManagerImpl;
import org.matsim.core.events.EventsReaderXMLv1;
import org.matsim.core.events.MatsimEventsReader;
import org.matsim.core.events.algorithms.EventWriter;
import org.matsim.core.network.io.NetworkChangeEventsWriter;
import org.matsim.core.population.io.PopulationReader;
import org.matsim.core.population.io.PopulationWriter;
import org.matsim.core.scenario.ScenarioUtils;

public class RunIsolateAgent {
	static public void main(String[] args) throws ConfigurationException {
		args = new String[] {"--input-path", "simulation_output/test/it.54/54.plans.xml.gz",
		"--output-path","simulation_output/test/it.54/54_bis.plans.xml.gz",
		"--agent-id","11223040"};

		CommandLine cmd = new CommandLine.Builder(args) //
				.requireOptions("input-path", "output-path", "agent-id") //
				.build();

		Config config = ConfigUtils.createConfig();
		Scenario scenario = ScenarioUtils.createScenario(config);

		// Load population
		String inputPath = cmd.getOptionStrict("input-path");
		new PopulationReader(scenario).readFile(inputPath);

		// Reduce population
		Collection<Id<Person>> allIds = new HashSet<>(scenario.getPopulation().getPersons().keySet());
		allIds.removeAll(Arrays.asList(Id.createPersonId(cmd.getOptionStrict("agent-id"))));
		allIds.forEach(scenario.getPopulation()::removePerson);

		// Write population
		String outputPath = cmd.getOptionStrict("output-path");
		new PopulationWriter(scenario.getPopulation()).write(outputPath);
	}
}
