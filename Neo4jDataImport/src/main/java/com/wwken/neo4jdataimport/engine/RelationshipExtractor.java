/*
 * 
 * Copyright (c) 2014 Ken Wu
 * 
 */

package com.wwken.neo4jdataimport.engine;

import java.util.Arrays;
import java.util.Map;

import com.wwken.neo4jdataimport.ProgressCounter;
import com.wwken.neo4jdataimport.domain.WikiRelationship;

import org.neo4j.unsafe.batchinsert.BatchInserter;

public class RelationshipExtractor extends StaxExtractor {

    private final BatchInserter inserter;
    private final Map<String, Long> inMemoryIndex;

    private final ProgressCounter linkCounter = new ProgressCounter();

    private long nodeId;
    private int badLinkCount = 0;

    public RelationshipExtractor(BatchInserter inserter,  Map<String, Long> inMemoryIndex) {
        super(Arrays.asList("t", "l"));
        this.inserter = inserter;
        this.inMemoryIndex = inMemoryIndex;
    }

    public int getLinkCount() {
        return linkCounter.getCount();
    }

    public int getBadLinkCount() {
        return badLinkCount;
    }

    @Override
    protected void handleElement(String element, String value) {
        if ("t".equals(element)) {
            nodeId = findNodeId(value);
        } else if ("l".equals(element)) {
            createRelationship(nodeId, value);
        }
    }

    private void createRelationship(long nodeId, String link) {
        Long linkNodeId = findNodeId(link);
        if (linkNodeId != null) {
            inserter.createRelationship(nodeId, linkNodeId, WikiRelationship.Link, null);
            linkCounter.increment();
        } else {
            badLinkCount++;
        }
    }

    private Long findNodeId(String title) {
        return inMemoryIndex.get(title);
    }

}
