import java.util.ArrayList;

public class Permutation {

	public static void main(String[] args) {
		String input = "abcde";
		ArrayList<String> o = getPerms(input);
		printOut(o);
	}

	private static ArrayList<String> getPerms(String input) { // TODO
																// Auto-generated
																// method stub
		if (input == null)
			return null;
		else if (input.length() == 1) {
			ArrayList<String> a = new ArrayList<String>();
			a.add(input);
			return a;
		}

		else {
			char c = input.charAt(0);
			ArrayList<String> allPreviousPerms = getPerms(input.substring(1));
			ArrayList<String> thisRoundPerms = new ArrayList<String>();
			for (String str : allPreviousPerms) {
				for (int i = 0; i < str.length(); i++) {
					String newS = insertAt(c, str, i);
					thisRoundPerms.add(newS);
				}
				thisRoundPerms.add(insertAt(c, str, str.length())); // Insert to
																	// the end
			}
			return thisRoundPerms;
		}
	}

	private static String insertAt(char c, String str, int i) {
		String st = (new StringBuffer(str)).insert(i, c).toString();
		return st;
	}

	private static void printOut(ArrayList<String> o) {
		if (o != null) {
			System.out.println("There are total " + o.size() + " items");
			for (String s : o) {
				System.out.println(s);
			}
		}
	}
}