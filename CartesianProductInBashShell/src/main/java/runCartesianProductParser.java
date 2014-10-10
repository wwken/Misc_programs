import java.util.ArrayList;
import java.util.HashSet;
import java.util.List;
import java.util.Set;

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
		//String input = "ab{p,q,r}yz";
		//String input = "c{d,e}g";
		//String input = "{d,e}g";
		String input = "a{b,c{d,e}g,h}";
		System.out.println("Trying to parse: " + input);
		CartesianProductParser cpp = new CartesianProductParser(input);
		String result = cpp.parse();
		System.out.println(result);
	}

}
