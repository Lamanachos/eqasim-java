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
                .requireOptions("sc_path","shp_path","res","output_path","drz_name","last_it") //
                .build();
        String sc_path = cmd.getOptionStrict("sc_path");
        String shp_path = cmd.getOptionStrict("shp_path");
        String res = cmd.getOptionStrict("res");
        String output_path = cmd.getOptionStrict("output_path");
        String drz_name = cmd.getOptionStrict("drz_name");
        String last_it = cmd.getOptionStrict("last_it");
        String[] preparedrz_args = new String[] {"--sc_path",sc_path,"--shp_path",shp_path,"--res",res,"--drz_name",drz_name};
        String[] runsim_args = new String[] {"--config-path",
                sc_path+"/ile_de_france_config_"+drz_name+".xml",
                "--config:controller.outputDirectory="+output_path,
                "--config:eqasim.analysisInterval=10",
                "--config:controler.firstIteration=0",
                "--config:controler.lastIteration="+last_it};
        String[] adapt_config_em = new String[] {"--ouput_path",output_path};
        String[] em_args = new String[] {"--config-path",output_path+"/output_config_emissions.xml","--hbefa-cold-avg","../../HBEFA/2022_IDF_EFA_ColdStart_Vehcat_Average_OnlyCar_Marjolaine.csv","--hbefa-hot-avg","../../HBEFA/2022_IDF_EFA_HOT_Vehcat_Average_OnlyCar_Marjolaine.csv"};
        prepareDrz.main(preparedrz_args);
        RunSimulationCarPt_DrivingRestriction.main(runsim_args);
        Adapt_config_emissions.main(adapt_config_em);
        RunComputeEmissionsEvents.main(em_args);
    }
}
