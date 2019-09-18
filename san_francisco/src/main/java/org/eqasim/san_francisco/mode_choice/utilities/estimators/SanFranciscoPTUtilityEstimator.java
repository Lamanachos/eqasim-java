package org.eqasim.san_francisco.mode_choice.utilities.estimators;

import java.util.List;

import org.eqasim.core.simulation.mode_choice.utilities.estimators.PtUtilityEstimator;
import org.eqasim.core.simulation.mode_choice.utilities.predictors.PersonPredictor;
import org.eqasim.core.simulation.mode_choice.utilities.predictors.PtPredictor;
import org.eqasim.san_francisco.mode_choice.parameters.SanFranciscoModeParameters;
import org.eqasim.san_francisco.mode_choice.utilities.predictors.SanFranciscoPersonPredictor;
import org.eqasim.san_francisco.mode_choice.utilities.variables.SanFranciscoPersonVariables;
import org.matsim.api.core.v01.population.Person;
import org.matsim.api.core.v01.population.PlanElement;

import com.google.inject.Inject;

import ch.ethz.matsim.discrete_mode_choice.model.DiscreteModeChoiceTrip;

public class SanFranciscoPTUtilityEstimator extends PtUtilityEstimator {
	private final SanFranciscoModeParameters parameters;
	private final SanFranciscoPersonPredictor predictor;

	@Inject
	public SanFranciscoPTUtilityEstimator(SanFranciscoModeParameters parameters, PersonPredictor personPredictor,
			PtPredictor ptPredictor, SanFranciscoPersonPredictor predictor) {
		super(parameters, ptPredictor);

		this.parameters = parameters;
		this.predictor = predictor;
	}

	protected double estimateRegionalUtility(SanFranciscoPersonVariables variables) {
		return (variables.cityTrip) ? parameters.sfPT.alpha_pt_city : 0.0;
	}

	@Override
	public double estimateUtility(Person person, DiscreteModeChoiceTrip trip, List<? extends PlanElement> elements) {
		SanFranciscoPersonVariables variables = predictor.predictVariables(person, trip, elements);

		double utility = 0.0;
        
		utility += super.estimateUtility(person, trip, elements);
		utility += estimateRegionalUtility(variables);

		return utility;
	}
}
