/**
 * 
 */
package com.kw.pointofsalecheckout;

import java.io.IOException;
import java.util.HashMap;
import java.util.Iterator;
import java.util.LinkedHashMap;
import java.util.Map;
import java.util.NavigableMap;
import java.util.TreeMap;

/**
 * @author ken
 *
 */
public class PriceTerminal {

	final String pricePolicyinputPath;
	final Map<String, NavigableMap<Integer, Double>> allPriceSpecs = new HashMap<String, NavigableMap<Integer, Double>>();
	final private Map<String, Integer> itemQuantities = new LinkedHashMap<String, Integer>();

	public PriceTerminal(String pricePolicyinputPath) throws IOException {
		this.pricePolicyinputPath = pricePolicyinputPath;
		init();
	}

	private void init() throws IOException {
		PricepolicyScanner policyScanner = new PricepolicyScanner(this);
		policyScanner.scanPolicy(pricePolicyinputPath);
	}

	public void setPricing(String item, int unit, double price) {
		NavigableMap<Integer, Double> priceSpec = null;
		if (this.allPriceSpecs.containsKey(item)) {
			priceSpec = this.allPriceSpecs.get(item);
		} else {
			priceSpec = new TreeMap<Integer, Double>();
			this.allPriceSpecs.put(item, priceSpec);
		}
		priceSpec.put(unit, price);
	}

	public boolean scan(String item) {
		if (item != null && item.trim().length() > 0) {
			if(!allPriceSpecs.containsKey(item)) {	//If the item is not defined in our price policy..return false	
				return false;
			}
			item = item.trim();
			if (itemQuantities.containsKey(item)) {
				itemQuantities.put(item, itemQuantities.get(item) + 1);
			} else {
				itemQuantities.put(item, 1);
			}
			return true;
		}
		return false;
	}

	public double getTotal() {
		double total = 0.0;
		for(String item: itemQuantities.keySet()) {
			int totalQuantityForThisItem = itemQuantities.get(item);
			NavigableMap<Integer, Double> priceSpec = this.allPriceSpecs.get(item);
			Iterator<Integer> keys = priceSpec.descendingKeySet().iterator();
			while(totalQuantityForThisItem > 0) {
				int thisScannedQuantity = keys.next();
				if(totalQuantityForThisItem < thisScannedQuantity) {
					continue;	//Go to the next smaller quantity
				} else if (thisScannedQuantity==1) {
					total = total + (totalQuantityForThisItem * priceSpec.get(thisScannedQuantity));
				} else {
					total = total + priceSpec.get(thisScannedQuantity);
				}
				totalQuantityForThisItem = totalQuantityForThisItem - thisScannedQuantity;
				if(thisScannedQuantity==1) {
					break;
				}
			}
		}
		return total;
	}

	/*
	 * Reset the internal item vs quantity counts
	 */
	public void reset() {
		itemQuantities.clear();
	}

}
