import static org.junit.Assert.*;

import org.junit.Before;
import org.junit.Test;

import com.kw.cartesianproductinbashshell.CartesianProductParser;


public class testCartesianProductParser {

	@Before
	public void setUp() throws Exception {
	}

	
	@Test
	public void test1() {
		String input = "ab{p,q,r}yz";
		CartesianProductParser cpp = new CartesianProductParser(input);
		String result = cpp.parse();
		String expected = "abpyz abqyz abryz";
		assertTrue(expected.equals(result));
	}
	
	@Test
	public void test2() {
		String input = "a{b,c}d{x,y}";
		CartesianProductParser cpp = new CartesianProductParser(input);
		String result = cpp.parse();
		String expected = "abdx abdy acdx acdy";
		assertTrue(expected.equals(result));
	}
	
	@Test
	public void test3() {
		String input = "ab{c,d}{e,f,g}";
		CartesianProductParser cpp = new CartesianProductParser(input);
		String result = cpp.parse();
		String expected = "abce abcf abcg abde abdf abdg";
		assertTrue(expected.equals(result));
	}
	
	@Test
	public void test4() {
		String input = "a{b,c{d,e}}";
		CartesianProductParser cpp = new CartesianProductParser(input);
		String result = cpp.parse();
		String expected = "ab acd ace";
		assertTrue(expected.equals(result));
	}
	
	@Test
	public void test5() {
		String input = "a{b,c{d,e}g}";
		CartesianProductParser cpp = new CartesianProductParser(input);
		String result = cpp.parse();
		String expected = "ab acdg aceg";
		assertTrue(expected.equals(result));
	}
	
	@Test
	public void test6() {
		String input = "a{b,c{d,e}g,h}";
		CartesianProductParser cpp = new CartesianProductParser(input);
		String result = cpp.parse();
		String expected = "ab acdg aceg ah";
		assertTrue(expected.equals(result));
	}
	
	@Test
	public void test7() {
		String input = "a{b,c{d,e}g,h}ij";
		CartesianProductParser cpp = new CartesianProductParser(input);
		String result = cpp.parse();
		String expected = "abij acdgij acegij ahij";
		assertTrue(expected.equals(result));
	}
	
	
	@Test
	public void test8() {
		String input = "a{b,c}ij{k,l}";
		CartesianProductParser cpp = new CartesianProductParser(input);
		String result = cpp.parse();
		String expected = "abijk abijl acijk acijl";
		assertTrue(expected.equals(result));
	}
	
	
	@Test
	public void testSomethingCrazy() {
		String input = "a{b,c{d,e,f}g,h}ij{k,l}{p,q,r}";
		CartesianProductParser cpp = new CartesianProductParser(input);
		String result = cpp.parse();
		String expected = "abijkp abijkq abijkr abijlp abijlq abijlr acdgijkp acdgijkq acdgijkr acdgijlp acdgijlq acdgijlr acegijkp acegijkq acegijkr acegijlp acegijlq acegijlr acfgijkp acfgijkq acfgijkr acfgijlp acfgijlq acfgijlr ahijkp ahijkq ahijkr ahijlp ahijlq ahijlr";
		assertTrue(expected.equals(result));
	}
	
	@Test
	public void testfinalFromSpec() {
		String input = "a{b,c{d,e,f}g,h}ij{k,l}";
		CartesianProductParser cpp = new CartesianProductParser(input);
		String result = cpp.parse();
		String expected = "abijk abijl acdgijk acdgijl acegijk acegijl acfgijk acfgijl ahijk ahijl";
		assertTrue(expected.equals(result));
	}
	
	

}
