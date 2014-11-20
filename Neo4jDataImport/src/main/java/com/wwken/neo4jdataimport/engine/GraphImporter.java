/*
 * 
 * Copyright (c) 2014 Ken Wu
 * 
 */

package com.wwken.neo4jdataimport.engine;

import java.util.HashMap;
import java.util.Map;

import org.apache.log4j.Logger;
import org.neo4j.unsafe.batchinsert.BatchInserter;
import org.neo4j.unsafe.batchinsert.BatchInserters;

import com.wwken.neo4jdataimport.domain.WikiLabel;

public class GraphImporter {
	private Logger log = Logger.getLogger(GraphImporter.class);
    private final BatchInserter inserter;
    private final Map<String, Long> inMemoryIndex;

    public GraphImporter(String dataDir) {
        inserter = BatchInserters.inserter(dataDir);
        inserter.createDeferredSchemaIndex(WikiLabel.Page).on("title").create();
        inMemoryIndex = new HashMap<String, Long>();
    }

    public void createNodes(String fileName) throws Exception {
    	log.info("Importing pages...");
        NodeExtractor nodeCreator = new NodeExtractor(inserter, inMemoryIndex);
        long startTime = System.currentTimeMillis();
        nodeCreator.parse(fileName);
        long elapsedSeconds = (System.currentTimeMillis() - startTime) / 1000;
        log.info("Imported "+nodeCreator.getPageCount()+" pages in "+elapsedSeconds+" seconds.\n");
    }

    public void createRelationships(String fileName) throws Exception {
    	log.info("Importing links...");
        RelationshipExtractor relationshipCreator = new RelationshipExtractor(inserter, inMemoryIndex);
        long startTime = System.currentTimeMillis();
        relationshipCreator.parse(fileName);
        long elapsedSeconds = (System.currentTimeMillis() - startTime) / 1000;
        log.info("Imported "+relationshipCreator.getLinkCount()+" links in "+elapsedSeconds+""
        		+ " seconds; "+relationshipCreator.getBadLinkCount()+" broken links ignored");
    }

    public void finish() {
        inserter.shutdown();
    }

}
