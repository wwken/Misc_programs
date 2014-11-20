/*
 * 
 * Copyright (c) 2014 Ken Wu
 * 
 */

package com.wwken.neo4jdataimport;

import java.util.Arrays;
import java.util.HashSet;
import java.util.Set;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

import javax.xml.stream.XMLStreamException;
import javax.xml.stream.XMLStreamWriter;

import com.wwken.neo4jdataimport.ProgressCounter;
import com.wwken.neo4jdataimport.engine.StaxExtractor;

public class LinkExtractor extends StaxExtractor {

    private static final Pattern LINK_PATTERN = Pattern.compile("\\[\\[(.+?)\\]\\]");

    private final XMLStreamWriter writer;
    private final ProgressCounter pageCounter = new ProgressCounter();

    private String title;
    private String text;

    public LinkExtractor(XMLStreamWriter writer) {
        super(Arrays.asList("page", "title", "text"));
        this.writer = writer;
    }

    public int getPageCount() {
        return pageCounter.getCount();
    }

    @Override
    protected void handleElement(String element, String value) {
        if ("page".equals(element)) {
            if (!title.contains(":")) {
                try {
                    writePage(title, text);
                } catch (XMLStreamException streamException) {
                    throw new RuntimeException(streamException);
                }
            }
            title = null;
            text = null;
        } else if ("title".equals(element)) {
            title = value;
        } else if ("text".equals(element)) {
            text = value;
        }
    }

    private void writePage(String title, String text) throws XMLStreamException {
        writer.writeStartElement("p");
        
        writer.writeStartElement("t");
        writer.writeCharacters(title);
        writer.writeEndElement();
        
        Set<String> links = parseLinks(text);
        links.remove(title);
        
        for (String link : links) {
            writer.writeStartElement("l");
            writer.writeCharacters(link);
            writer.writeEndElement();
        }
        
        writer.writeEndElement();

        pageCounter.increment();
    }

    private Set<String> parseLinks(String text) {
        Set<String> links = new HashSet<String>();
        if (text != null) {
            Matcher matcher = LINK_PATTERN.matcher(text);
            while (matcher.find()) {
                String link = matcher.group(1);
                if (!link.contains(":")) {
                    if (link.contains("|")) {
                        link = link.substring(link.lastIndexOf('|') + 1);
                    }
                    links.add(link);
                }
            }
        }
        return links;
    }

}
