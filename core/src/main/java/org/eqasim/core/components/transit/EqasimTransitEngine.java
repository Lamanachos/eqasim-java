package org.eqasim.core.components.transit;

import java.util.*;
import java.util.stream.Collectors;

import ch.sbb.matsim.routing.pt.raptor.SwissRailRaptor;
import org.eqasim.core.components.transit.departure.DepartureFinder;
import org.eqasim.core.components.transit.departure.DepartureFinder.NoDepartureFoundException;
import org.eqasim.core.components.transit.departure.DepartureFinder.StopDeparture;
import org.eqasim.core.components.transit.events.PublicTransitEvent;
import org.matsim.api.core.v01.Id;
import org.matsim.api.core.v01.events.PersonStuckEvent;
import org.matsim.api.core.v01.network.Link;
import org.matsim.api.core.v01.population.Leg;
import org.matsim.api.core.v01.population.PlanElement;
import org.matsim.core.api.experimental.events.EventsManager;
import org.matsim.core.api.experimental.events.TeleportationArrivalEvent;
import org.matsim.core.mobsim.framework.MobsimAgent;
import org.matsim.core.mobsim.framework.PlanAgent;
import org.matsim.core.mobsim.qsim.InternalInterface;
import org.matsim.core.mobsim.qsim.agents.TransitAgent;
import org.matsim.core.mobsim.qsim.interfaces.AgentCounter;
import org.matsim.core.mobsim.qsim.interfaces.DepartureHandler;
import org.matsim.core.mobsim.qsim.interfaces.MobsimEngine;
import org.matsim.core.router.DefaultRoutingRequest;
import org.matsim.core.router.RoutingRequest;
import org.matsim.facilities.Facility;
import org.matsim.pt.routes.TransitPassengerRoute;
import org.matsim.pt.transitSchedule.api.*;

import com.google.inject.Singleton;

@Singleton
public class EqasimTransitEngine implements DepartureHandler, MobsimEngine {
	final static boolean letPeopleStuck = true; //UM if false, people stuck because they can't take their transit will find another one (but not the optimal just one that get there
	final private TransitSchedule transitSchedule;
	final private DepartureFinder departureFinder;
	private InternalInterface internalInterface;
	final private EventsManager eventsManager;
	final private AgentCounter agentCounter;

	final private PriorityQueue<AgentDeparture> departures = new PriorityQueue<>();
	final private PriorityQueue<AgentArrival> arrivals = new PriorityQueue<>();

	private class AgentDeparture implements Comparable<AgentDeparture> {
		final public MobsimAgent agent;
		final public double departureTime;
		final public Id<Link> departureLinkId;

		public AgentDeparture(MobsimAgent agent, double departureTime, Id<Link> departureLinkId) {
			this.agent = agent;
			this.departureTime = departureTime;
			this.departureLinkId = departureLinkId;
		}

		@Override
		public int compareTo(AgentDeparture other) {
			return Double.compare(departureTime, other.departureTime);
		}
	}

	private class AgentArrival implements Comparable<AgentArrival> {
		final public MobsimAgent agent;
		final public double arrivalTime;
		final public Id<Link> arrivalLinkId;
		final public PublicTransitEvent event;

		public AgentArrival(MobsimAgent agent, double arrivalTime, Id<Link> arrivalLinkId, PublicTransitEvent event) {
			this.agent = agent;
			this.arrivalTime = arrivalTime;
			this.arrivalLinkId = arrivalLinkId;
			this.event = event;
		}

		@Override
		public int compareTo(AgentArrival other) {
			return Double.compare(arrivalTime, other.arrivalTime);
		}
	}

	public EqasimTransitEngine(EventsManager eventsManager, TransitSchedule transitSchedule,
			DepartureFinder departureFinder, AgentCounter agentCounter) {
		this.eventsManager = eventsManager;
		this.transitSchedule = transitSchedule;
		this.departureFinder = departureFinder;
		this.agentCounter = agentCounter;
	}

	@Override
	public boolean handleDeparture(double now, MobsimAgent agent, Id<Link> departureLinkId) {
		if (agent.getMode().equals("pt")) {
			Leg leg = (Leg) ((PlanAgent) agent).getCurrentPlanElement();
			TransitPassengerRoute route = (TransitPassengerRoute) leg.getRoute();

			//Somethin I started thinking stopIds are not universal
//			TransitRoute eRoute = (TransitRoute) leg.getRoute();
//			Map<Id<TransitLine>, TransitLine> transitLines = transitSchedule.getTransitLines();
//			List<TransitLine> validTransitLines = new ArrayList<>();
//			for (Id<TransitLine> id : transitLines.keySet()){
//				TransitLine tempTransitLine = transitLines.get(id);
//				Collection<TransitRoute> tempTransitRoutes = tempTransitLine.getRoutes().values();
//				boolean valid = false;
//				for (TransitRoute transitRoute : tempTransitRoutes){
//					boolean ok = true;
//					for (TransitRouteStop stop : eRoute.getStops()){
//						if (transitRoute.getStops().contains(stop)){
//						}
//						else {
//							ok = false;
//						}
//					}
//					if (ok){
//						valid = true;
//					}
//				}
//				if (valid){
//					validTransitLines.add(tempTransitLine);
//				}
//			}

			TransitLine transitLine = transitSchedule.getTransitLines().get(route.getLineId());
			TransitRoute transitRoute = transitLine.getRoutes().get(route.getRouteId());
			boolean foundTransit = false;

			try {
				StopDeparture stopDeparture = departureFinder.findNextDeparture(transitRoute, route.getAccessStopId(),
						route.getEgressStopId(), now);

				double vehicleDepartureTime = stopDeparture.departure.getDepartureTime()
						+ stopDeparture.stop.getDepartureOffset().seconds();

				double waitingTime = route.getBoardingTime().seconds() - leg.getDepartureTime().seconds();
				double inVehicleTime = leg.getTravelTime().seconds() - waitingTime;

				double arrivalTime = vehicleDepartureTime + inVehicleTime;

				if (Math.abs(arrivalTime - now) < 1.0) {
					arrivalTime = now + 1.0;
				}

				Id<Link> arrivalLinkId = transitSchedule.getFacilities().get(route.getEgressStopId()).getLinkId();

				PublicTransitEvent transitEvent = new PublicTransitEvent(arrivalTime, agent.getId(),
						transitLine.getId(), transitRoute.getId(), route.getAccessStopId(), route.getEgressStopId(),
						vehicleDepartureTime, route.getDistance());

				internalInterface.registerAdditionalAgentOnLink(agent);
				departures.add(new AgentDeparture(agent, vehicleDepartureTime, departureLinkId));
				arrivals.add(new AgentArrival(agent, arrivalTime, arrivalLinkId, transitEvent));
				foundTransit = true;

			} catch (NoDepartureFoundException e) {
				//Get optimal (not working yet)
//				List<TransitRouteStop> stops = transitRoute.getStops();
//				TransitStopFacility access = null;
//				TransitStopFacility egress = null;
//				for (TransitRouteStop stop : stops){
//					TransitStopFacility stopFacility = stop.getStopFacility();
//					if (stopFacility.getId() == route.getAccessStopId()){
//						access = stopFacility;
//					}
//					if (stopFacility.getId() == route.getEgressStopId()){
//						egress = stopFacility;
//					}
//				}
//				TransitAgent agentTr = (TransitAgent) agent;
//
//				RoutingRequest routingRequest = DefaultRoutingRequest.of(access, egress, now,agentTr.getPerson(), null);
//				List<? extends PlanElement> ptElements = ptRoutingModule.calcRoute(routingRequest);

				if (!letPeopleStuck) {
					List<TransitLine> transitLines = transitSchedule.getTransitLines().values().stream().toList();
					int max_i = transitLines.size();
					int i = 0;
					while (i < max_i) {
						transitLine = transitLines.get(i);
						List<TransitRoute> transitRoutes = transitLine.getRoutes().values().stream().toList();
						int max_j = transitRoutes.size();
						int j = 0;
						while (j < max_j) {
							transitRoute = transitRoutes.get(j);
							try {
								StopDeparture stopDeparture = departureFinder.findNextDeparture(transitRoute, route.getAccessStopId(),
										route.getEgressStopId(), now);

								double vehicleDepartureTime = stopDeparture.departure.getDepartureTime()
										+ stopDeparture.stop.getDepartureOffset().seconds();

								double waitingTime = route.getBoardingTime().seconds() - leg.getDepartureTime().seconds();
								double inVehicleTime = leg.getTravelTime().seconds() - waitingTime;

								double arrivalTime = vehicleDepartureTime + inVehicleTime;

								if (Math.abs(arrivalTime - now) < 1.0) {
									arrivalTime = now + 1.0;
								}

								Id<Link> arrivalLinkId = transitSchedule.getFacilities().get(route.getEgressStopId()).getLinkId();

								PublicTransitEvent transitEvent = new PublicTransitEvent(arrivalTime, agent.getId(),
										transitLine.getId(), transitRoute.getId(), route.getAccessStopId(), route.getEgressStopId(),
										vehicleDepartureTime, route.getDistance());

								internalInterface.registerAdditionalAgentOnLink(agent);
								departures.add(new AgentDeparture(agent, vehicleDepartureTime, departureLinkId));
								arrivals.add(new AgentArrival(agent, arrivalTime, arrivalLinkId, transitEvent));
								i = max_i;
								j = max_j;
								foundTransit = true;
							}
							catch (NoDepartureFoundException | IllegalStateException f) {
								j += 1;
							}
						}
						i += 1;
					}
				}
			}
			if (!foundTransit){
				eventsManager.processEvent(new PersonStuckEvent(now, agent.getId(), agent.getCurrentLinkId(), "pt"));
				agentCounter.decLiving();
			}
			return true;
		}

		return false;
	}

	@Override
	public void doSimStep(double time) {
		while (!departures.isEmpty() && departures.peek().departureTime <= time) {
			AgentDeparture departure = departures.poll();
			internalInterface.unregisterAdditionalAgentOnLink(departure.agent.getId(), departure.departureLinkId);
		}

		while (!arrivals.isEmpty() && arrivals.peek().arrivalTime <= time) {
			AgentArrival arrival = arrivals.poll();
			arrival.agent.notifyArrivalOnLinkByNonNetworkMode(arrival.arrivalLinkId);
			eventsManager.processEvent(new PublicTransitEvent(time, arrival.event));
			eventsManager.processEvent(new TeleportationArrivalEvent(time, arrival.agent.getId(),
					arrival.event.getTravelDistance(), "pt"));
			arrival.agent.endLegAndComputeNextState(time);
			internalInterface.arrangeNextAgentState(arrival.agent);
		}
	}

	@Override
	public void onPrepareSim() {
		departures.clear();
		arrivals.clear();
	}

	@Override
	public void afterSim() {
		double time = internalInterface.getMobsim().getSimTimer().getTimeOfDay();
		Set<MobsimAgent> processedAgents = new HashSet<>();

		for (AgentDeparture departure : departures) {
			eventsManager
					.processEvent(new PersonStuckEvent(time, departure.agent.getId(), departure.departureLinkId, "pt"));
			agentCounter.decLiving();
			processedAgents.add(departure.agent);
		}

		for (AgentArrival arrival : arrivals) {
			if (!processedAgents.contains(arrival.agent)) {
				eventsManager
						.processEvent(new PersonStuckEvent(time, arrival.agent.getId(), arrival.arrivalLinkId, "pt"));
				agentCounter.decLiving();
			}
		}
	}

	@Override
	public void setInternalInterface(InternalInterface internalInterface) {
		this.internalInterface = internalInterface;
	}
}
