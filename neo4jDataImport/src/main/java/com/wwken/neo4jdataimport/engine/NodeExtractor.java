/*
 * 
 * Copyright (c) 2014 Ken Wu
 * 
 */

package com.wwken.neo4jdataimport.engine;

import java.util.Arrays;
import java.util.Map;

import com.wwken.neo4jdataimport.ProgressCounter;
import com.wwken.neo4jdataimport.domain.WikiLabel;

import org.neo4j.helpers.collection.MapUtil;
import org.neo4j.unsafe.batchinsert.BatchInserter;

public class NodeExtractor extends StaxExtractor {

    private final BatchInserter inserter;
    private final Map<String, Long> inMemoryIndex;

    private final ProgressCounter pageCounter = new ProgressCounter();

    public NodeExtractor(BatchInserter inserter, Map<String, Long> inMemoryIndex) {
        super(Arrays.asList("t"));
        this.inserter = inserter;
        this.inMemoryIndex = inMemoryIndex;
    }

    public int getPageCount() {
        return pageCounter.getCount();
    }

    @Override
    protected void handleElement(String element, String value) {
        if ("t".equals(element)) {
            createNode(value);
        }
    }

    private void createNode(String title) {
        Map<String, Object> properties = MapUtil.map("title", title);
        long nodeId = inserter.createNode(properties, WikiLabel.Page);
        inMemoryIndex.put(title, nodeId);
        pageCounter.increment();
    }

}
