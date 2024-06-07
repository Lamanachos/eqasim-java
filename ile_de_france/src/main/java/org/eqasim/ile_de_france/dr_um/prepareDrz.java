package org.eqasim.ile_de_france.dr_um;

import org.matsim.core.config.CommandLine;

import java.io.IOException;

public class prepareDrz {
    public static void main(String[] args) throws CommandLine.ConfigurationException, IOException {
        CommandLine cmd = new CommandLine.Builder(args) //
                .requireOptions("sc_name","sc_shp","residents") //
                .build();
        String sc_name = cmd.getOptionStrict("sc_name");
        String sc_shp = cmd.getOptionStrict("sc_shp");
        String residents = cmd.getOptionStrict("residents");
        LinksInArea.getLinks(sc_name,sc_shp);
        NetworkModifier.modifyNetwork(sc_name, residents);
        if (residents.equals("yes")) {
            PopulationModifier.modifyPopulation(sc_name);
        }
        RunAdaptConfig_CarInternal.runAdaptConfiguration(sc_name,residents);
    }
}
