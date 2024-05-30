package org.eqasim.core.simulation.mode_choice.utilities.predictors;

import com.google.inject.Inject;
import com.google.inject.name.Named;
import org.eqasim.core.components.ParkRideManager;
import org.eqasim.core.simulation.mode_choice.cost.CostModel;
import org.eqasim.core.simulation.mode_choice.parameters.ModeParameters;
import org.eqasim.core.simulation.mode_choice.utilities.variables.CarPtVariables;
import org.matsim.api.core.v01.Id;
import org.matsim.api.core.v01.TransportMode;
import org.matsim.api.core.v01.network.Network;
import org.matsim.api.core.v01.population.*;
import org.matsim.contribs.discrete_mode_choice.model.DiscreteModeChoiceTrip;
import org.matsim.core.router.RoutingModule;
import org.matsim.pt.routes.TransitPassengerRoute;

import java.util.ArrayList;
import java.util.LinkedList;
import java.util.List;
import java.util.Objects;

public class CarPtPredictor extends CachedVariablePredictor<CarPtVariables>{
    private final RoutingModule carRoutingModule;
    private final RoutingModule ptRoutingModule;
    private final CostModel carCostModel;
    private final CostModel ptCostModel;
    private final ModeParameters parameters;
    // private final List<Coord> parkRideCoords;
    private final Network network;
    private final PopulationFactory populationFactory;
    private final ParkRideManager parkRideMana;

    @Inject
    public CarPtPredictor(ModeParameters parameters, Network network, @Named("car") RoutingModule carRoutingModule,
                          @Named("pt") RoutingModule ptRoutingModule, PopulationFactory populationFactory, @Named("car") CostModel carCostModel,
                          @Named("pt") CostModel ptCostModel, ParkRideManager parkRideMana) {
        this.carCostModel = carCostModel;
        this.ptCostModel = ptCostModel;
        this.parameters = parameters;
        // this.parkRideCoords = parkRideCoords;
        this.network = network;
        this.carRoutingModule = carRoutingModule;
        this.ptRoutingModule = ptRoutingModule;
        this.populationFactory = populationFactory;
        this.parkRideMana = parkRideMana;
    }

    @Override
    public CarPtVariables predict(Person person, DiscreteModeChoiceTrip trip, List<? extends PlanElement> elements) {
   // elements include the new carpt trip, so no need to recalculate carelements and ptelements
        List<String> list_stuck = new ArrayList<>();
        list_stuck.add("11223040");
        list_stuck.add("11399053");
        list_stuck.add("9445770");
        list_stuck.add("10628436");
        list_stuck.add("8670465");
        list_stuck.add("452764");
        list_stuck.add("4816736");
        list_stuck.add("9196646");
        list_stuck.add("7760364");
        list_stuck.add("8207851");
        list_stuck.add("291890");
        list_stuck.add("7839402");
        list_stuck.add("1575215");
        list_stuck.add("10947292");
        list_stuck.add("12166086");
        list_stuck.add("7969941");
        list_stuck.add("11369978");
        list_stuck.add("11060248");
        list_stuck.add("8360722");
        list_stuck.add("9606725");
        list_stuck.add("8634267");
        list_stuck.add("4732458");
        list_stuck.add("9054604");
        list_stuck.add("10033073");
        list_stuck.add("9672046");
        list_stuck.add("11879941");
        list_stuck.add("8860321");
        list_stuck.add("9756490");
        list_stuck.add("11755775");
        list_stuck.add("4805323");
        list_stuck.add("7074388");
        list_stuck.add("3188250");
        list_stuck.add("8961135");
        list_stuck.add("4691722");
        list_stuck.add("10465457");
        list_stuck.add("9834608");
        list_stuck.add("43781");
        list_stuck.add("39467");
        list_stuck.add("11718768");
        list_stuck.add("11375209");
        list_stuck.add("1800432");
        list_stuck.add("3725072");
        list_stuck.add("8098558");
        list_stuck.add("6606557");
        list_stuck.add("1371105");
        list_stuck.add("4724231");
        list_stuck.add("4497685");
        list_stuck.add("3512067");
        list_stuck.add("2798646");
        list_stuck.add("4181992");

        List<PlanElement> carElements = new LinkedList<>();
        List<PlanElement> ptElements = new LinkedList<>();
        if (list_stuck.contains(person.getId().toString())) {
            System.out.println("--------------------HI !!!!-----------------");
        }
        boolean flag = true;
        for (PlanElement element : elements) {
            if (list_stuck.contains(person.getId().toString())) {
                System.out.println(element.getAttributes());
            }
            if (flag == true) {
                carElements.add(element);
            } else {
                ptElements.add(element);
            }

            if(element instanceof Activity) {
                Activity act = (Activity) element;
                if (act.getType().equals("carPt interaction")) {
                    flag = false;
                }
            }
        }

        double vehicleTravelTime = 0.0;
        double accessEgressTime_min_car = 0.0;
        for (PlanElement element : carElements) {
            if (element instanceof Leg) {
                Leg leg = (Leg) element;
                switch (leg.getMode()) {
                    case TransportMode.walk:
                        accessEgressTime_min_car += leg.getTravelTime().seconds() / 60.0;
                        break;
                    case "carInternal":
                    case TransportMode.car:
                        vehicleTravelTime += leg.getTravelTime().seconds() / 60.0 + parameters.car.constantParkingSearchPenalty_min;
                        break;
                    default:
                        throw new IllegalStateException("Unknown mode in car trip: " + leg.getMode());
                }
            }
        }

        // We take 5 min to park the car and access to PT (transfer time)
        double timeToAccessPt = 5;
        vehicleTravelTime += timeToAccessPt;

        PlanElement last_element = carElements.get(carElements.size()-1);
        Activity car_pt = (Activity) last_element;
        DiscreteModeChoiceTrip trip_car = new DiscreteModeChoiceTrip(trip.getOriginActivity(), car_pt, "car",
                carElements, person.hashCode(), carElements.get(0).hashCode(),1000, trip.getTripAttributes());
        double cost_MU_car = carCostModel.calculateCost_MU(person, trip_car, carElements);
        double euclideanDistance_km_car = PredictorUtils.calculateEuclideanDistance_km(trip_car);

        DiscreteModeChoiceTrip trip_pt = new DiscreteModeChoiceTrip(car_pt, trip.getDestinationActivity(), "pt",
                ptElements, person.hashCode(), ptElements.get(0).hashCode(), 1000, trip.getTripAttributes());

        int numberOfVehicularTrips = 0;
        boolean isFirstWaitingTime = true;

        // Track relevant variables
        double inVehicleTime_min = 0.0;
        double waitingTime_min = 0.0;
        double accessEgressTime_min_pt = 0.0;

        for (PlanElement element : ptElements) {
            if (element instanceof Leg) {
                Leg leg = (Leg) element;

                switch (leg.getMode()) {
                    case TransportMode.walk:
                    case TransportMode.non_network_walk:
                        accessEgressTime_min_pt += leg.getTravelTime().seconds() / 60.0;
                        break;
                    case TransportMode.transit_walk:
                        waitingTime_min += leg.getTravelTime().seconds() / 60.0;
                        break;
                    case TransportMode.pt:
                        TransitPassengerRoute route = (TransitPassengerRoute) leg.getRoute();

                        double departureTime = leg.getDepartureTime().seconds();
                        double waitingTime = route.getBoardingTime().seconds() - departureTime;
                        double inVehicleTime = leg.getTravelTime().seconds() - waitingTime;

                        inVehicleTime_min += inVehicleTime / 60.0;

                        if (!isFirstWaitingTime) {
                            waitingTime_min += waitingTime / 60.0;
                        } else {
                            isFirstWaitingTime = false;
                        }

                        numberOfVehicularTrips++;
                        break;
                    default:
                        throw new IllegalStateException("Unknown mode in PT trip: " + leg.getMode());
                }
            }
        }

        int numberOfLineSwitches = Math.max(0, numberOfVehicularTrips - 1);

        // Calculate cost
        double cost_MU_pt = ptCostModel.calculateCost_MU(person, trip_pt, ptElements);

        double euclideanDistance_km_pt = PredictorUtils.calculateEuclideanDistance_km(trip_pt);

        return new CarPtVariables(vehicleTravelTime, euclideanDistance_km_car, accessEgressTime_min_car, cost_MU_car,
                inVehicleTime_min, waitingTime_min, numberOfLineSwitches, euclideanDistance_km_pt,
                accessEgressTime_min_pt, cost_MU_pt);
    }
}
