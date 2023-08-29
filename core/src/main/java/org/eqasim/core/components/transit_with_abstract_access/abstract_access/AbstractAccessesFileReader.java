package org.eqasim.core.components.transit_with_abstract_access.abstract_access;

import org.matsim.api.core.v01.Id;
import org.matsim.api.core.v01.IdMap;
import org.matsim.core.utils.io.MatsimXmlParser;
import org.matsim.pt.transitSchedule.api.TransitSchedule;
import org.matsim.pt.transitSchedule.api.TransitStopFacility;
import org.xml.sax.Attributes;

import java.util.Stack;

public class AbstractAccessesFileReader extends MatsimXmlParser {


    public final static String ABSTRACT_ACCESS_TAG_NAME = "abstractAccessItem";

    public final static String ROOT_TAG_NAME = "abstractAccessItems";

    public final static String TRANSIT_STOP_ID_ATTR_NAME = "transitStopId";

    public final static String ACCESS_ID_ATTR_NAME = "id";

    public final static String RADIUS_ATTR_NAME = "radius";

    public final static String AVG_SPEED_ATTR_NAME = "averageSpeed";

    private final TransitSchedule transitSchedule;

    private final IdMap<AbstractAccessItem, AbstractAccessItem> accessItems;

    public AbstractAccessesFileReader(TransitSchedule transitSchedule) {
        this.transitSchedule = transitSchedule;
        this.accessItems = new IdMap<>(AbstractAccessItem.class);
        this.setValidating(false);
    }

    @Override
    public void startTag(String name, Attributes atts, Stack<String> context) {
        if(name.equals(ABSTRACT_ACCESS_TAG_NAME)) {
            Id<TransitStopFacility> transitStopFacilityId;
            Id<AbstractAccessItem> abstractAccessItemId;
            double radius;
            double averageSpeed;

            if(atts.getValue(ACCESS_ID_ATTR_NAME) != null) {
                abstractAccessItemId = Id.create(atts.getValue(ACCESS_ID_ATTR_NAME), AbstractAccessItem.class);
                if(this.accessItems.containsKey(abstractAccessItemId)) {
                    throw new IllegalStateException("abstract access item " + abstractAccessItemId.toString() + " defined more than once");
                }
            } else {
                throw new IllegalStateException(ACCESS_ID_ATTR_NAME + " is required in " + ABSTRACT_ACCESS_TAG_NAME + " element");
            }

            if(atts.getValue(TRANSIT_STOP_ID_ATTR_NAME) != null) {
                transitStopFacilityId = Id.create(atts.getValue(TRANSIT_STOP_ID_ATTR_NAME), TransitStopFacility.class);
                if(!this.transitSchedule.getFacilities().containsKey(transitStopFacilityId)) {
                    throw new IllegalStateException("Transit stop facility " + transitStopFacilityId.toString() + " specified for access item " + abstractAccessItemId.toString() + " does not exist");
                }
            } else {
                throw new IllegalStateException(TRANSIT_STOP_ID_ATTR_NAME + " is required in " + ABSTRACT_ACCESS_TAG_NAME + " element");
            }

            if(atts.getValue(RADIUS_ATTR_NAME) != null) {
                radius = Double.parseDouble(atts.getValue(RADIUS_ATTR_NAME));
            } else {
                throw new IllegalStateException(RADIUS_ATTR_NAME + " is required in " + ABSTRACT_ACCESS_TAG_NAME + " element");
            }

            if(atts.getValue(AVG_SPEED_ATTR_NAME) != null) {
                averageSpeed = Double.parseDouble(atts.getValue(AVG_SPEED_ATTR_NAME));
            } else {
                throw new IllegalStateException(AVG_SPEED_ATTR_NAME + " is required in " + ABSTRACT_ACCESS_TAG_NAME + " element");
            }
            this.accessItems.put(abstractAccessItemId, new AbstractAccessItem(abstractAccessItemId, this.transitSchedule.getFacilities().get(transitStopFacilityId), radius, averageSpeed));
        }
    }

    @Override
    public void endTag(String name, String content, Stack<String> context) {

    }

    public IdMap<AbstractAccessItem, AbstractAccessItem> getAccessItems(){
        return this.accessItems;
    }
}
