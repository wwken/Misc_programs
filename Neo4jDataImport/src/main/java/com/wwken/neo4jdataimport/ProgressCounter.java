/*
 * 
 * Copyright (c) 2014 Ken Wu
 * 
 */

package com.wwken.neo4jdataimport;

import com.wwken.neo4jdataimport.DataImporterRunner;

import org.apache.log4j.Logger;

public class ProgressCounter {
	private static Logger log = Logger.getLogger(ProgressCounter.class);
	
    private static final int THOUSAND = 1000;
    private static final int SMALL_STEP = 1 * THOUSAND;
    private static final int BIG_STEP = 50 * THOUSAND;

    private int count = 0;

    public int getCount() {
        return count;
    }

    public void increment() {
        count++;
        if (count % BIG_STEP == 0) {
        	log.debug(". "+ count / THOUSAND +"k");
        } else if (count % SMALL_STEP == 0) {
        	log.debug(".");
        }
    }

}
