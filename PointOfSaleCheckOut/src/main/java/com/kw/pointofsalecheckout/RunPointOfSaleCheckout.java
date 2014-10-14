package com.kw.pointofsalecheckout;

import java.io.IOException;
import java.util.Scanner;

public class RunPointOfSaleCheckout {

	public static void main(String[] args) throws IOException {
		String pointOfSaleFilePath = args[0];
		PriceTerminal priceTerminal = new PriceTerminal(pointOfSaleFilePath);

		@SuppressWarnings("resource")
		Scanner in = new Scanner(System.in);
		String s = " ";
		while (s.length() > 0) {
			System.out.println("Enter a item ( hit enter to finish) :");
			s = in.nextLine();
			priceTerminal.scan(s);
		}
		double totalPrices = priceTerminal.getTotal();
		System.out.println("Total Price is: " + totalPrices);
	}
}