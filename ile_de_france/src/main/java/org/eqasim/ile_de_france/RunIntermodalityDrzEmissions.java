package org.eqasim.ile_de_france;
import org.eqasim.core.components.emissions.RunComputeEmissionsEvents;
import org.eqasim.ile_de_france.dr_um.Adapt_config_emissions;
import org.eqasim.ile_de_france.dr_um.prepareDrz;
import org.eqasim.ile_de_france.intermodality.RunSimulationCarPt_DrivingRestriction;
import org.matsim.core.config.CommandLine;
import java.io.IOException;

public class RunIntermodalityDrzEmissions {
    public static void main(String[] args) throws CommandLine.ConfigurationException, IOException {
        CommandLine cmd = new CommandLine.Builder(args) //
                .requireOptions("sc_name","sc_shp","res","output_name","last_it") //
                .build();
        String sc_name = cmd.getOptionStrict("sc_name");
        String sc_shp = cmd.getOptionStrict("sc_shp");
        String res = cmd.getOptionStrict("res");
        String output_name = cmd.getOptionStrict("output_name");
        String last_it = cmd.getOptionStrict("last_it");
        String[] preparedrz_args = new String[] {"--sc_name",sc_name,"--sc_shp","gis/"+sc_shp,"--res",res};
        String[] runsim_args = new String[] {"--config-path",
                "ile_de_france/scenarios/"+sc_name+"/ile_de_france_config_carInternal.xml",
                "--config:controller.outputDirectory=simulation_output/"+output_name,
                "--config:eqasim.analysisInterval=10",
                "--config:controler.firstIteration=0",
                "--config:controler.lastIteration="+last_it};
        String[] adapt_config_em = new String[] {"--sc_name",output_name};
        String[] em_args = new String[] {"--config-path","simulation_output/"+output_name+"/output_config_emissions.xml","--hbefa-cold-avg","../../HBEFA/2022_IDF_EFA_ColdStart_Vehcat_Average_OnlyCar_Marjolaine.csv","--hbefa-hot-avg","../../HBEFA/2022_IDF_EFA_HOT_Vehcat_Average_OnlyCar_Marjolaine.csv"};
        prepareDrz.main(preparedrz_args);
        RunSimulationCarPt_DrivingRestriction.main(runsim_args);
        Adapt_config_emissions.main(adapt_config_em);
        RunComputeEmissionsEvents.main(em_args);
    }
}
