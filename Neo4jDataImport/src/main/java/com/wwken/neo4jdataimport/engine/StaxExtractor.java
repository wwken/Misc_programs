/*
 * 
 * Copyright (c) 2014 Ken Wu
 * 
 */

package com.wwken.neo4jdataimport.engine;

import java.io.FileInputStream;
import java.io.IOException;
import java.io.InputStream;
import java.util.LinkedList;
import java.util.List;

import javax.xml.stream.XMLInputFactory;
import javax.xml.stream.XMLStreamException;
import javax.xml.stream.XMLStreamReader;
import javax.xml.stream.events.XMLEvent;

import org.codehaus.stax2.XMLInputFactory2;

public abstract class StaxExtractor {

	private static final XMLInputFactory XML_INPUT_FACTORY = XMLInputFactory2
			.newInstance();

	private final List<String> interestingElements;

	public StaxExtractor(List<String> interestingElements) {
		this.interestingElements = interestingElements;
	}

	protected abstract void handleElement(String element, String value);

	public void parse() throws IOException, XMLStreamException {
		parse(System.in);
	}

	public void parse(String fileName) throws IOException, XMLStreamException {
		parse(new FileInputStream(fileName));
	}

	private void parse(InputStream inputStream) throws IOException,
			XMLStreamException {
		XMLStreamReader reader = XML_INPUT_FACTORY.createXMLStreamReader(
				inputStream, "UTF-8");
		try {
			parseElements(reader);
		} finally {
			reader.close();
			inputStream.close();
		}
	}

	private void parseElements(XMLStreamReader reader)
			throws XMLStreamException {
		LinkedList<String> elementStack = new LinkedList<String>();
		StringBuilder textBuffer = new StringBuilder();

		while (reader.hasNext()) {
			switch (reader.next()) {
			case XMLEvent.START_ELEMENT:
				elementStack.push(reader.getName().getLocalPart());
				textBuffer.setLength(0);
				break;
			case XMLEvent.END_ELEMENT:
				String element = elementStack.pop();
				if (isInteresting(element)) {
					handleElement(element, textBuffer.toString().trim());
				}
				break;
			case XMLEvent.CHARACTERS:
				if (isInteresting(elementStack.peek())) {
					textBuffer.append(reader.getText());
				}
				break;
			}
		}
	}

	private boolean isInteresting(String element) {
		return interestingElements.contains(element);
	}

}
