/* * Given an infinite number of quarters (25 cents), 
 * dimes (10 cents), nickels (5 cents)  * and pennies (1 cent), 
 * write code to calculate the number of ways of representing n cents. 
 *  
 *  
 *  Author: Ken Wu
 *  
 */


public class ChangeCoins {
	public static void main(String[] args) {
		int AMOUNT = 51;
		int[] changeArray = { 25, 10, 5, 1 };
		int time = goChange(AMOUNT, AMOUNT, changeArray, 0, 0, "");
		System.out.println("To change $" + AMOUNT + ", the number of ways is "
				+ time);

	}

	private static int goChange(int ORI_AMOUNT, int amount, int[] changeArray,
			int pos, int totalWays, String currentO) {

		if (pos == changeArray.length - 1) {
			int needed = amount / changeArray[pos];
			if (needed > 0)
				currentO = currentO + " " + needed + " * $" + changeArray[pos];
			System.out.println(currentO);
			return 1;
		}

		int currentWays = 0;

		int thisCurrentChangeCoin = changeArray[pos];
		if (thisCurrentChangeCoin <= amount) {
			int i = amount / thisCurrentChangeCoin;
			for (; i >= 0; i--) {
				if (i == 0) {
					currentWays = currentWays
							+ goChange(ORI_AMOUNT, amount - i
									* thisCurrentChangeCoin, changeArray,
									pos + 1, totalWays, currentO);
				} else {
					currentWays = currentWays
							+ goChange(ORI_AMOUNT, amount - i
									* thisCurrentChangeCoin, changeArray,
									pos + 1, totalWays, currentO + " " + i
											+ " * $" + thisCurrentChangeCoin
											+ " ");
				}
			}
		} else {
			currentWays = currentWays
					+ goChange(ORI_AMOUNT, amount, changeArray, pos + 1,
							totalWays, currentO);
		}

		return currentWays;
	}

}