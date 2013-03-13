
import java.io.BufferedReader;
import java.io.File;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.IOException;
import java.net.URISyntaxException;
import java.net.URL;
import java.util.List;
import java.util.Scanner;

/**
 * 
 */

/**
 * @author ken
 *
 */
public class RunMain {

	/**
	 * 
	 */
	public static void main(String[] args) {
		
		String from;
		String to;
		Scanner user_input = new Scanner( System.in );
		
		WordMutation wm = new WordMutation("allwords.txt");
		
		while(true) {
			System.out.println("Please enter a word you want to mutate from: ");
			from = user_input.next( );
			System.out.println("Please enter a word you want to mutate to: ");
			to = user_input.next( );
			
			if(to.length() != from.length()) {
				System.out.println("Sorry, the length of '"+from+"' is not same as '"+to+"'.  Please try again.");
				continue;
			}
			

			List<String> allMutations = wm.mutate(from, to);
			
			//Print out my findings
			if(allMutations.size() > 0) {
				System.out.println("To mutate the word from '"+from+"' to '"+to+"', there are " + allMutations.size() + " ways to do that as followed: ");
				print(allMutations);
			} else {
				System.out.println("Sorry, there is no way to mutate a word from '"+from+"' to '"+to+"'.  Please try again.");
			}
			
			System.out.println("");
			System.out.println("");
		}
		
	}

	private static void print(List<String> allMutations) {
		for(String s: allMutations) {
			System.out.println(s);
		}
	}

}
