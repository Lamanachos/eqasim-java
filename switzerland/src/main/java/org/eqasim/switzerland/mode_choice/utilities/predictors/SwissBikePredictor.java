package org.eqasim.switzerland.mode_choice.utilities.predictors;

import java.util.ArrayList;
import java.util.List;
import java.util.Set;

import com.google.inject.Inject;
import org.eqasim.core.simulation.mode_choice.utilities.predictors.BikePredictor;
import org.eqasim.core.simulation.mode_choice.utilities.predictors.CachedVariablePredictor;
import org.eqasim.core.simulation.mode_choice.utilities.predictors.CarPredictor;
import org.eqasim.core.simulation.mode_choice.utilities.variables.BikeVariables;
import org.eqasim.switzerland.mode_choice.utilities.variables.SwissBikeVariables;
import org.matsim.api.core.v01.Id;
import org.matsim.api.core.v01.Scenario;
import org.matsim.api.core.v01.network.Link;
import org.matsim.api.core.v01.network.Network;
import org.matsim.api.core.v01.population.Person;
import org.matsim.api.core.v01.population.PlanElement;
import org.matsim.api.core.v01.population.Leg;
import org.matsim.contribs.discrete_mode_choice.model.DiscreteModeChoiceTrip;
import org.matsim.core.population.routes.NetworkRoute;


public class SwissBikePredictor extends CachedVariablePredictor<SwissBikeVariables> {
    private final Scenario scenario;


    @Inject
    public SwissBikePredictor(Scenario scenario) {
        this.scenario = scenario;

    }

    @Override
    public SwissBikeVariables predict(Person person, DiscreteModeChoiceTrip trip, List<? extends PlanElement> elements) {
//        if (elements.size() > 1) {
//            throw new IllegalStateException("We do not support multi-stage bike trips yet.");
//        }
        Leg leg = (Leg) elements.get(2);

        double travelTime_min = leg.getTravelTime().seconds() / 60.0;

        double S1L1 = 0.0;
        double S2L1 = 0.0;
        double S3L1 = 0.0;
        double S4L1 = 0.0;
        double S1L2 = 0.0;
        double S2L2 = 0.0;
        double S3L2 = 0.0;
        double S4L2 = 0.0;

        double propS1L1 = 0.0;
        double propS2L1 = 0.0;
        double propS3L1 = 0.0;
        double propS4L1 = 0.0;
        double propS1L2 = 0.0;
        double propS2L2 = 0.0;
        double propS3L2 = 0.0;
        double propS4L2 = 0.0;

        double totalUphillDistance = 0.0;
        double totalUphillRise = 0.0;

        double routedDistance_km = leg.getRoute().getDistance()/1000.0; ///g/ what if routed distance on bike leg is zero?

        Network network = scenario.getNetwork();
        Id<Link> startLinkId = leg.getRoute().getStartLinkId();
        Id<Link> endLinkId = leg.getRoute().getEndLinkId();

        List<Id<Link>> linkIdList;
        linkIdList = ((NetworkRoute) leg.getRoute()).getLinkIds();// use (NetworkRoute) to use method getLinkIds
        List<Id<Link>> editLinkIdList = new ArrayList<>(linkIdList); // maybe this solves the problem of adding directly to linkIdList
        editLinkIdList.add(startLinkId); //g/ maybe use half of the start or end of the link?
        editLinkIdList.add(endLinkId);
        for (Id<Link> linkId: editLinkIdList){
            Link link = network.getLinks().get(linkId);

            double numberLanes = link.getNumberOfLanes();
            double freespeed = link.getFreespeed();
            double linkLength_km = link.getLength()/1000.0;

            if (numberLanes == 1){
                if (freespeed <= 8.33334){ // <=30km/h
                    S1L1 += linkLength_km; //g/ is it possible that the agent does not use the whole length of the link?
                }
                if ((freespeed > 8.33334)&&(freespeed <= 13.8889)){ // <=50km/h
                    S2L1 += linkLength_km;
                }
                if ((freespeed > 13.8889)&&(freespeed <= 16.6667)){ // <=60km/h
                    S3L1 += linkLength_km;
                }
                if (freespeed > 16.6667) { // > 60km/h
                    S4L1 += linkLength_km;
                }
            }
            if (numberLanes > 1){
                if (freespeed <= 8.33334){
                    S1L2 += linkLength_km;
                }
                if ((freespeed > 8.33334)&&(freespeed <= 13.8889)){
                    S2L2 += linkLength_km;
                }
                if ((freespeed > 13.8889)&&(freespeed <= 16.6667)){
                    S3L2 += linkLength_km;
                }
                if (freespeed > 16.6667) {
                    S4L2 += linkLength_km;
                }
            }
            double gradient;
            if (!link.getAttributes().getAsMap().containsKey("gradient")){ // if there is no gradient in network (links with same start and end node)
                gradient = 0.0;
            }
            else{
                gradient = (Double) link.getAttributes().getAttribute("gradient");
            }
            if (gradient > 0.0){
                totalUphillDistance += link.getLength();
                totalUphillRise += gradient * link.getLength();
            }
        }

        double averageUphillGradient;
        if (totalUphillDistance == 0.0){
            averageUphillGradient = 0.0; // to avoid division by zero errors
        } else {
            averageUphillGradient = totalUphillRise/totalUphillDistance;
        }

        if (routedDistance_km > 0.0){ // to avoid distance/0 => infinity
            propS1L1 = S1L1/routedDistance_km;
            propS2L1 = S2L1/routedDistance_km;
            propS3L1 = S3L1/routedDistance_km;
            propS4L1 = S4L1/routedDistance_km;
            propS1L2 = S1L2/routedDistance_km;
            propS2L2 = S2L2/routedDistance_km;
            propS3L2 = S3L2/routedDistance_km;
            propS4L2 = S4L2/routedDistance_km;
        }


        return new SwissBikeVariables(travelTime_min,
                propS1L1, propS2L1, propS3L1,propS4L1,propS1L2,propS2L2,propS3L2,propS4L2, routedDistance_km,averageUphillGradient);


    }
}