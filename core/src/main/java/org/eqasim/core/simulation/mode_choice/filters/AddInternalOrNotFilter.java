package org.eqasim.core.simulation.mode_choice.filters;

import java.util.List;

import org.matsim.api.core.v01.population.Person;
import org.matsim.contribs.discrete_mode_choice.model.DiscreteModeChoiceTrip;
import org.matsim.contribs.discrete_mode_choice.model.tour_based.TourFilter;

public class AddInternalOrNotFilter implements TourFilter {
    @Override
    public boolean filter(Person person, List<DiscreteModeChoiceTrip> tour) {
        Object attribute = person.getAttributes().getAttribute("HomeLink");
        for (DiscreteModeChoiceTrip trip : tour){
            trip.getTripAttributes().putAttribute("HomeLink", attribute);
        }
        return true;
    }
}