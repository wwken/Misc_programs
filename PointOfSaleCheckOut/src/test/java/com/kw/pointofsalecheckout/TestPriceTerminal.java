/**
 * 
 */
package com.kw.pointofsalecheckout;

import static org.junit.Assert.*;

import org.junit.Before;
import org.junit.Test;

/**
 * @author ken
 *
 */
public class TestPriceTerminal {

	PriceTerminal priceTerminal;
	private final double DELTA = 1e-5;	//To the 5 decimals precise
	
	@Before
	public void setUp() throws Exception {
		String pointOfSaleFilePath = "input/pointofsale.txt";
		priceTerminal =  new PriceTerminal(pointOfSaleFilePath);
	}
	
	@Test
	public void test1() {
		priceTerminal.reset();
		priceTerminal.scan("A");
		priceTerminal.scan("B");
		priceTerminal.scan("C");
		priceTerminal.scan("D");
		priceTerminal.scan("A");
		priceTerminal.scan("B");
		priceTerminal.scan("A");
		priceTerminal.scan("A");
		double total = priceTerminal.getTotal();
		assertEquals(32.40, total, DELTA);
	}
	
	@Test
	public void test2() {
		priceTerminal.reset();
		priceTerminal.scan("C");
		priceTerminal.scan("C");
		priceTerminal.scan("C");
		priceTerminal.scan("C");
		priceTerminal.scan("C");
		priceTerminal.scan("C");
		priceTerminal.scan("C");
		double total = priceTerminal.getTotal();
		assertEquals(7.25, total, DELTA);
	}
	
	@Test
	public void test3() {
		priceTerminal.reset();
		priceTerminal.scan("A");
		priceTerminal.scan("B");
		priceTerminal.scan("C");
		priceTerminal.scan("D");
		double total = priceTerminal.getTotal();
		assertEquals(15.40, total, DELTA);
	}
	
	@Test
	public void test4() {
		priceTerminal.reset();
		priceTerminal.scan("D");
		priceTerminal.scan("C");
		priceTerminal.scan("C");
		priceTerminal.scan("B");
		priceTerminal.scan("B");
		priceTerminal.scan("C");
		priceTerminal.scan("A");
		double total = priceTerminal.getTotal();
		assertEquals(29.9, total, DELTA);
	}
	
	@Test
	public void test5() {
		priceTerminal.reset();
		priceTerminal.scan("B");
		priceTerminal.scan("B");
		priceTerminal.scan("B");
		priceTerminal.scan("B");
		priceTerminal.scan("B");
		priceTerminal.scan("C");
		priceTerminal.scan("A");
		priceTerminal.scan("A");
		priceTerminal.scan("D");
		priceTerminal.scan("B");
		priceTerminal.scan("C");
		priceTerminal.scan("D");
		priceTerminal.scan("D");
		priceTerminal.scan("A");
		double total = priceTerminal.getTotal();
		assertEquals(80.95, total, DELTA);
	}
	
	@Test
	public void testEmpty() {
		priceTerminal.reset();
		double total = priceTerminal.getTotal();
		assertEquals(0, total, DELTA);
	}
	
	@Test
	public void testNonExistingItem() {
		priceTerminal.reset();
		boolean sucess = priceTerminal.scan("ZZZ");
		assertFalse(sucess);
	}
	
}
