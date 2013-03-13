import java.io.BufferedReader;
import java.io.File;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.IOException;
import java.io.InputStream;
import java.net.URISyntaxException;
import java.net.URL;
import java.util.ArrayList;
import java.util.List;
import java.util.regex.Pattern;

/**
 * 
 */

/**
 * @author ken wu
 *
 */
public class WordMutation {

	/**
	 * 
	 */
	
	private Dictionary dict = new Dictionary();
	
	public WordMutation(String dictionaryFileLocation) {

		InputStream is = getClass().getResourceAsStream(dictionaryFileLocation);
		
		java.util.Scanner s = new java.util.Scanner(is).useDelimiter(Pattern.compile("[\\r\\n;]+"));
		String readStr = null;
		while (s.hasNext()) {
			readStr = s.next();
			dict.add(readStr.toLowerCase());
		}
		
		
	}
	
	public List<String> mutate (String start, String end) {
		List<String> candidates = getAllCandidateWords(end);
		
		String pers = "";
		for(int i=0; i<start.length(); i++) {
			if(start.charAt(i) == end.charAt(i))
				continue;
			pers += i+"";
		}
		
		ArrayList<String> ps = Permutation.getPerms(pers);
		ArrayList<String> finalOutPut = new ArrayList<String>();
		/*
		System.out.println("There are total " + ps.size() + " items");
		for (String s : ps) {
			System.out.println(s);
		}
		*/
		for(String patternIndex: ps) {
			process(candidates, start, start, end, patternIndex, 0, start, finalOutPut);
		}
		
		return finalOutPut;
	}

	private void process(List<String> candidates, String currentString, String start, String end, String patternIndex, int currentPos, String soFar, List<String> finalOutPut) {
		
		if(currentPos == patternIndex.length()) {
			//No more to loop, now check if the current String is equal to the end string
			if(currentString.equals(end)) {
				finalOutPut.add(soFar);
			}
			return;
		}
		
		//System.out.println("Inside the process, patternIndex: " + patternIndex + ", i:" + i + ", c:" + c);
		
		List<String> all = getAllStringsExceptAt(candidates, currentString, patternIndex, currentPos);
		
		for(String s: all) {
			process(candidates, s, start, end, patternIndex, currentPos+1, soFar + " -> " + s, finalOutPut);
		}
	}
	
	private List<String> getAllStringsExceptAt(List<String> candidates, String inputString, String patternIndex, int currentPos) {

		int patternInd = Integer.parseInt(patternIndex.charAt(currentPos)+"");
		char c = inputString.charAt(patternInd);
		
		List<String> thisRoundStrings = new ArrayList<String>();
		for(String s: candidates) {
			boolean isItGood = true;
			for(int i=0; i<s.length(); i++) {
				if(i == patternInd) {
					if(s.charAt(i) == inputString.charAt(i)) {
						isItGood = false;
						break;
					} else {
						
					}
				} else {
					if(s.charAt(i) != inputString.charAt(i)) {
						isItGood = false;
						break;
					}
				}
			}
			if(isItGood) {
				//Now i am going to see if all of the previous chracters match too
				boolean isItStillGood = true;
				for(int k=0; k<currentPos; k++) {
					int pInd = Integer.parseInt(patternIndex.charAt(k)+"");
					if(s.charAt(pInd) != inputString.charAt(pInd))
						isItStillGood = false;
				}
				if(isItStillGood) {
					thisRoundStrings.add(s);
				}
			}
		}
		return thisRoundStrings;
	}

	private List<String> getAllCandidateWords(String end) {
		List<String> allWordsWithSpecifiedLengths = new ArrayList<String>();
		
		//Now i am going to filter out all of the dictionary with .length() != end.length()
		//For example, let say input string is "salt", "xayy" will be kept, "axyy" will be kept, "xxyy" will be out
		for(String s: dict) {
			if(s.length() == end.length()) {
				allWordsWithSpecifiedLengths.add(s);
			}
		}

		//Now i am going to filter out all the words that does not have any letter which matchs the input string's letter at the same position
		//For example, let say input string is "salt", "xayy" will be kept, "axyy" will be out
		List<String> allWordsWithSpecifiedLengthsAndAtLeastOneMatchedCharacter = new ArrayList<String>();
		for(String s: allWordsWithSpecifiedLengths) {
			for(int i=0; i<end.length(); i++) {
				Boolean isThisWordGood = false;
				if(s.contains(end.charAt(i)+"")) {
					for(int j=0; j<s.length(); j++) {
						if((s.charAt(j) == end.charAt(i)) && j == i) {
							allWordsWithSpecifiedLengthsAndAtLeastOneMatchedCharacter.add(s);
							isThisWordGood = true;
							break;
						}
					}
				}
				if(isThisWordGood)
					break;
			}
		}
		
		
		return allWordsWithSpecifiedLengthsAndAtLeastOneMatchedCharacter;
	}
	
	

}
