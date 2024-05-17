package org.eqasim.ile_de_france.dr_um;

import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;
import org.locationtech.jts.geom.Coordinate;
import org.locationtech.jts.geom.Geometry;
import org.locationtech.jts.geom.GeometryFactory;
import org.locationtech.jts.geom.Point;
import org.matsim.api.core.v01.Coord;
import org.matsim.api.core.v01.Id;
import org.matsim.api.core.v01.Scenario;
import org.matsim.api.core.v01.network.Link;
import org.matsim.core.config.ConfigUtils;
import org.matsim.core.network.io.MatsimNetworkReader;
import org.matsim.core.scenario.ScenarioUtils;
import org.matsim.core.utils.geometry.geotools.MGC;
import org.matsim.core.utils.gis.ShapeFileReader;
import org.opengis.feature.simple.SimpleFeature;

import java.io.BufferedWriter;
import java.io.FileWriter;
import java.io.IOException;
import java.util.*;


public class LinksInArea {
    private static final Logger LOG = LogManager.getLogger(LinksInArea.class);
    private final static GeometryFactory geometryFactory = new GeometryFactory();
    public static void main (String[] args) throws IOException {
        // Input and output files
        String networkInputFile = "ile_de_france/scenarios/idf_1pc_pr/base_case/ile_de_france_network.xml.gz";
        String linkIDOutputFile = "ile_de_france/scenarios/idf_1pc_pr/driving_restriction/internal_linksID.txt";
        String areaShapeFile = "ile_de_france/scenarios/paris.shp";

        // Get network
        Scenario scenario = ScenarioUtils.createScenario(ConfigUtils.createConfig());
        MatsimNetworkReader reader = new MatsimNetworkReader(scenario.getNetwork());
        reader.readFile(networkInputFile);

        // Store relevant area of city as geometry
        Collection<SimpleFeature> features = (new ShapeFileReader()).readFileAndInitialize(areaShapeFile);
        Map<String, Geometry> zoneGeometries = new HashMap<>();
        for (SimpleFeature feature : features) {
            zoneGeometries.put((String) feature.getAttribute("scenario"), (Geometry) feature.getDefaultGeometry());
        }
        Geometry areaGeometry = zoneGeometries.get(null);
        // Collect all links that within the area
        Set<Id<Link>> retainedLinkIds = new HashSet<>();

        for (Link link : scenario.getNetwork().getLinks().values()) {
            Coord coord = link.getCoord();
            Coordinate coordinate = new Coordinate(coord.getX(), coord.getY());
            Point point = geometryFactory.createPoint(coordinate);
            if (!areaGeometry.contains(point)) {
                scenario.getNetwork().removeLink(link.getId());
            }
            if (areaGeometry.contains(point)) {
                retainedLinkIds.add(link.getId());
            }
        }
        // Write modified network to file
//        NetworkWriter writer = new NetworkWriter(scenario.getNetwork());
//        writer.write(networkOutputFile);
        // Write linkIDs to file
        BufferedWriter fileWriter = new BufferedWriter(new FileWriter(linkIDOutputFile));
        Iterator it = retainedLinkIds.iterator();
        while (it.hasNext()) {
            fileWriter.write(it.next().toString());
            fileWriter.newLine();
        }
        fileWriter.close();

    }
}
