/*
 * 
 * Copyright (c) 2014 Ken Wu
 * 
 */

package com.wwken.neo4jdataimport.engine;

import java.util.HashMap;
import java.util.Map;

import org.neo4j.unsafe.batchinsert.BatchInserter;
import org.neo4j.unsafe.batchinsert.BatchInserters;

import com.wwken.neo4jdataimport.domain.WikiLabel;

public class GraphImporter {

    private final BatchInserter inserter;
    private final Map<String, Long> inMemoryIndex;

    public GraphImporter(String dataDir) {
        inserter = BatchInserters.inserter(dataDir);
        inserter.createDeferredSchemaIndex(WikiLabel.Page).on("title").create();
        inMemoryIndex = new HashMap<String, Long>();
    }

    public void createNodes(String fileName) throws Exception {
        System.out.println("Importing pages...");
        NodeExtractor nodeCreator = new NodeExtractor(inserter, inMemoryIndex);
        long startTime = System.currentTimeMillis();
        nodeCreator.parse(fileName);
        long elapsedSeconds = (System.currentTimeMillis() - startTime) / 1000;
        System.out.printf("\n%d pages imported in %d seconds.\n", nodeCreator.getPageCount(), elapsedSeconds);
    }

    public void createRelationships(String fileName) throws Exception {
        System.out.println("Importing links...");
        RelationshipExtractor relationshipCreator = new RelationshipExtractor(inserter, inMemoryIndex);
        long startTime = System.currentTimeMillis();
        relationshipCreator.parse(fileName);
        long elapsedSeconds = (System.currentTimeMillis() - startTime) / 1000;
        System.out.printf("\n%d links imported in %d seconds; %d broken links ignored\n",
                relationshipCreator.getLinkCount(), elapsedSeconds, relationshipCreator.getBadLinkCount());
    }

    public void finish() {
        inserter.shutdown();
    }

}
