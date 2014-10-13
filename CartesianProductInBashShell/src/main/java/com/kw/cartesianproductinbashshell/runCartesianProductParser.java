package com.kw.cartesianproductinbashshell;

/**
 * 
 */

/**
 * @author ken
 *
 */
public class runCartesianProductParser {

		
	/**
	 * @param args
	 */
	public static void main(String[] args) {
		String input = args[0];
		System.out.println("Trying to parse: " + input);
		CartesianProductParser cpp = new CartesianProductParser(input);
		String result = cpp.parse();
		System.out.println(result);
	}

}
