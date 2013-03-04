/* * 
 * Implement an algorithm to print all valid 
 * (e.g., properly opened and closed) combinations of n-pairs of parentheses.		
 * EXAMPLE:	input: 3 (e.g., 3 pairs of parentheses)	output: ()()(), ()(()), (())(), ((()))	 
 *
 **/

import java.util.LinkedList;
import java.util.Queue;
import java.util.Stack;
public class Parentheses 
{	
	public static void main(String[] args) {		
		int pairsOfParenthese = 5;		
		Queue<Queue<String>> results = new LinkedList<Queue<String>>();		
		loop(results, 0, pairsOfParenthese * 2);	
	}	
	
	private static void loop(Queue<Queue<String>> results, int pos, int limit) {		
		if(pos >= limit) {			
			printResult(results);			
			return;		
		}		
		if(results.size() == 0) {		 
			Queue<String> q = new LinkedList<String>();		
			q.add("(");			
			results.add(q);		
		} else {	
			Queue<Queue<String>> newResults =  new LinkedList<Queue<String>>(); 		
			for(Queue<String> q: results) {				
				int numOfLefts = numOfLefts(q);	
				int numOfRights = pos - numOfLefts; 		
				if( numOfLefts * 2 < limit ) {				
					//add left		
					Queue<String> newQ = new LinkedList<String> (q);			
					newQ.add("(");					newResults.add(newQ);	
				}							
				if ( (numOfRights * 2 < limit) && (numOfRights < numOfLefts)) {		
					//add right				
					Queue<String> newQ = new LinkedList<String> (q);		
					newQ.add(")");					
					newResults.add(newQ);	
				}		
			}			
			results = newResults;
		}		
		loop(results, pos+1, limit);
	}	
	
	private static int numOfLefts(Queue<String> q) {	
		int lefts = 0;		
		for(String s: q) {			
			if(s.equals("(")) {			 	
				lefts++;	
			}		
		}		
		return lefts;	
	}	
	
	private static void printResult(Queue<Queue<String>> results) {		
		for(Queue<String> q: results) {			
			for(String s: q) {	
				System.out.print(s + " ");			
			}		
			System.out.println();		
		}			
	}
}

	