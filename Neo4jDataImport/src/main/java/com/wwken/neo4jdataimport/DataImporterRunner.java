/*
 * 
 * Copyright (c) 2014 Ken Wu
 * 
 */

package com.wwken.neo4jdataimport;

import java.io.FileOutputStream;
import java.io.IOException;

import javax.xml.stream.XMLOutputFactory;
import javax.xml.stream.XMLStreamException;
import javax.xml.stream.XMLStreamWriter;

import org.apache.log4j.Logger;
import org.codehaus.stax2.XMLOutputFactory2;

import com.wwken.neo4jdataimport.LinkExtractor;
import com.wwken.neo4jdataimport.engine.GraphImporter;

public class DataImporterRunner {
	private static Logger log = Logger.getLogger(DataImporterRunner.class);
	final private String outputFile;
	final private String dataDir;
    public DataImporterRunner(String o, String d) {
		this.outputFile=o;
		this.dataDir=d;
	}

	public static void main(String[] args) throws Exception {
        if (args.length < 2) {
        	log.error("USAGE: ExtractLinks <output-file> <data-dir>");
            System.exit(255);
        }
        DataImporterRunner self = new DataImporterRunner(args[0], args[1]);
        self.run();
    }

    private void run() throws Exception {
		extract();
		load();
	}

	private void extract() throws IOException, XMLStreamException {
		log.info("Parsing pages and extracting links...");
        
        long startTime = System.currentTimeMillis();
        XMLOutputFactory outputFactory = XMLOutputFactory2.newInstance();
        
        XMLStreamWriter writer = outputFactory.createXMLStreamWriter(new FileOutputStream(outputFile), "UTF-8");
        writer.writeStartDocument();
        writer.writeStartElement("d");
        
        LinkExtractor linkExtractor = new LinkExtractor(writer);
        linkExtractor.parse();

        writer.writeEndElement();
        writer.writeEndDocument();
        writer.close();
        
        long elapsedSeconds = (System.currentTimeMillis() - startTime) / 1000;
        System.out.printf("\n%d pages parsed in %d seconds.\n", linkExtractor.getPageCount(), elapsedSeconds);
    }
	
	private void load() throws Exception {
        GraphImporter importer = new GraphImporter(dataDir);
        importer.createNodes(outputFile);
        importer.createRelationships(outputFile);
        importer.finish();
	}

}
