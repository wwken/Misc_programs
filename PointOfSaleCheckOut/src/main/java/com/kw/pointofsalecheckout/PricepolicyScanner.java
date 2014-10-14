/**
 * 
 */
package com.kw.pointofsalecheckout;

import java.io.File;
import java.io.IOException;
import java.util.List;

import org.apache.commons.io.FileUtils;

/**
 * @author ken
 *
 */
public class PricepolicyScanner {
	 
	final PriceTerminal priceTerminal;
	public PricepolicyScanner(PriceTerminal priceTerminal) {
		this.priceTerminal = priceTerminal;
	}
	public void scanPolicy(String pricePolicyinputPath) throws IOException {
		File file = new File(pricePolicyinputPath);
		List<String> lines = FileUtils.readLines(file, "UTF-8");
		for (String line : lines) {
			String[] contents = line.split("\t");
			String item = contents[0];
			parsePriceSpec(item, contents[1]);
		}
	}
	
	/*
	 * priceString is of form, e.g.: 1-1.00,3-0.75,5-0.5
	 */
	private void parsePriceSpec(String item, String priceString) {
		String[] contents = priceString.split(",");
		for (String s : contents) {
			String[] unitAndPrice = s.split("-");
			int unit = Integer.parseInt(unitAndPrice[0]);
			double price = Double.parseDouble(unitAndPrice[1]);
			priceTerminal.setPricing(item, unit, price);
		}
	}
}
