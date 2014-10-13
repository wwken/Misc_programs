package com.kw.cartesianproductinbashshell;

import java.util.Set;
import java.util.Stack;
import com.kw.cartesianproductinbashshell.expression.CompoundExpression;
import com.kw.cartesianproductinbashshell.expression.Expression;
import com.kw.cartesianproductinbashshell.expression.ValueExpression;

/**
 * 
 */

/**
 * Date: 2014-10-09
 * 
 * @author ken Wu
 * 
 *
 */
public class CartesianProductParser {

	final String input;
	private int glevel = 0; // This represents the current level of the braces
	
	
	/*
	 * Add all values from s2 to s1
	 */
	public static Set<StringBuffer> add(Set<StringBuffer> s1, Set<StringBuffer> s2) {
		for (StringBuffer sb : s2) {
			s1.add(sb);
		}
		return s1;
	}

	public static String flatternToString(Set<StringBuffer> cValues,
			boolean putSpacesInBetween) {
		StringBuffer result = new StringBuffer();
		for (StringBuffer sb : cValues) {
			result.append(sb.toString());
			if (putSpacesInBetween)
				result.append(" ");
		}
		return result.toString().trim();
	}

	Expression prevCurrentExpr = null;
	Expression currentExpr = null;
	Expression firstExpr = null;
	Stack<Expression> exprStack = new Stack<>();

	public CartesianProductParser(String in) {
		this.input = in;
	}

	public String parse() {
		int mode = 0; // 0 means value expression, 1 means compound expression
		int pos = 0;
		char prevC = ' ';
		// Now i am going to parse the whole input string
		currentExpr = new ValueExpression(this);
		while (pos < input.length()) {
			char c = input.charAt(pos++);
			if (c == '{') {
				glevel++;
				if (prevC == ',') {
					mode = 0;
				} else {
					mode = 1;
				}
				if (mode == 1) {
					Expression newE = new CompoundExpression(this);
					currentExpr.setNext(newE);
					exprStack.push(currentExpr); // Save the current one into the stack
					currentExpr = newE;
				}
			} else if (c == '}') {
				glevel--;
				if (prevC != '}') {
					currentExpr = exprStack.pop();
				}
				mode = 2;
			} else if (c == ',') {
				if (currentExpr instanceof ValueExpression) {
					prevCurrentExpr.createNewValue();
					currentExpr = prevCurrentExpr;
				} else {
					currentExpr.createNewValue();
				}
			} else {
				if (mode == 2) { // Right off from the compound expression
					ValueExpression newV = new ValueExpression(this);
					newV.appendValue(c + "");
					currentExpr.setNext(newV);
					prevCurrentExpr = currentExpr;
					currentExpr = newV;
				} else {
					currentExpr.appendValue(c + "");
				}
				if (firstExpr == null)
					firstExpr = currentExpr;
				mode = 0;
			}
			prevC = c;
		}

		return firstExpr.eval();

	}
	

	public int getLevel() {
		return this.glevel;
	}

}
