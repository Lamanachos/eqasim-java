package org.eqasim.ile_de_france.dr_um;

import org.matsim.core.config.CommandLine;

import java.io.IOException;

public class prepareDrz {
    public static void main(String[] args) throws CommandLine.ConfigurationException, IOException {
        CommandLine cmd = new CommandLine.Builder(args) //
                .requireOptions("sc_path","shp_path","res","drz_name") //
                .build();
        String sc_path = cmd.getOptionStrict("sc_path");
        String shp_path = cmd.getOptionStrict("shp_path");
        String res = cmd.getOptionStrict("res");
        String drz_name = cmd.getOptionStrict("drz_name");
        LinksInArea.getLinks(sc_path,shp_path);
        NetworkModifier.modifyNetwork(sc_path,res,drz_name);
        if (res.equals("yes")) {
            PopulationModifier.modifyPopulation(sc_path,drz_name);
        }
        RunAdaptConfig_CarInternal.runAdaptConfiguration(sc_path, res, drz_name);
    }
}
