package org.eqasim.examples.zurich_parking.mode_choice.utilities.variables;

import org.eqasim.core.simulation.mode_choice.utilities.variables.BaseVariables;

public class ZurichParkingCarVariables implements BaseVariables {
	final public double travelTime_min;
	final public double parkingSearchTime_min;
	final public double cost_MU;
	final public double costParking_MU;
	final public double euclideanDistance_km;
	final public double accessEgressTime_min;

	public ZurichParkingCarVariables(double travelTime_min, double parkingSearchTime_min,
									 double cost_MU, double costParking_MU,
									 double euclideanDistance_km, double accessEgressTime_min) {
		this.travelTime_min = travelTime_min;
		this.parkingSearchTime_min = parkingSearchTime_min;
		this.cost_MU = cost_MU;
		this.costParking_MU = costParking_MU;
		this.euclideanDistance_km = euclideanDistance_km;
		this.accessEgressTime_min = accessEgressTime_min;
	}
}
