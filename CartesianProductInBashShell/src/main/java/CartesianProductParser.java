import java.util.Iterator;
import java.util.LinkedHashSet;
import java.util.Set;
import java.util.Stack;
import java.util.logging.Level;

/**
 * 
 */

/**
 * Date: 2014-10-09
 * @author ken Wu
 * 
 *
 */
public class CartesianProductParser {

	final String input;
	int glevel = 0; // This represents the current level of the braces

	abstract class Expression {
		protected Expression nextExpression = null;

		abstract String eval();

		abstract Set<StringBuffer> combineNext();

		boolean hasBeenEvalulated = false;

		boolean hasThisBeenEvalulated() {
			return this.hasBeenEvalulated;
		}

		void setNext(Expression e) {
			if (this.nextExpression == null)
				this.nextExpression = e;
			else {
				Expression curExp = this.nextExpression;
				while (curExp.nextExpression != null) {
					curExp = curExp.nextExpression;
				}
				curExp.nextExpression = e;
			}
		}

		Expression getNext() {
			return nextExpression;
		}

		abstract void appendValue(String s);

		abstract void createNewValue();

	}

	class ValueExpression extends Expression {
		StringBuffer value = new StringBuffer();

		@Override
		String eval() {
			if (nextExpression == null)
				return value.toString() + " ";
			else {
				Set<StringBuffer> cValues = combineNext();
				StringBuffer sb = new StringBuffer();
				for (StringBuffer s : cValues) {
					sb.append(s.toString() + " ");
				}
				return sb.toString().trim();
			}
		}

		@Override
		// ValueExpression
		Set<StringBuffer> combineNext() {
			hasBeenEvalulated = true;
			if (nextExpression == null
					|| nextExpression.hasThisBeenEvalulated()) {
				Set<StringBuffer> cValues = new LinkedHashSet<StringBuffer>();
				cValues.add(new StringBuffer(this.value.toString()));
				return cValues;
			} else {
				Set<StringBuffer> cValues = nextExpression.combineNext();
				for (StringBuffer s : cValues) {
					String origS = s.toString();
					s.setLength(0);
					s.append(this.value + origS + "");
				}
				return cValues;
			}
		}

		@Override
		void appendValue(String s) {
			value.append(s);
		}

		@Override
		void createNewValue() {
			// Do nothing
		}

		@Override
		// ValueExpression
		public String toString() {
			StringBuffer sb = new StringBuffer(this.value.toString());
			if (this.nextExpression != null)
				sb.append(this.nextExpression.toString());
			return sb.toString();
		}

	} // end of ValueExpression

	class CompoundExpression extends Expression {
		Set<Expression> expressions = new LinkedHashSet<Expression>();
		Expression currentExpression = null; // This refers to the current
												// expression that it is working
												// on

		@Override
		String eval() {
			Set<StringBuffer> cValues = combineNext();
			if (nextExpression != null
					&& !nextExpression.hasThisBeenEvalulated()) {
				Set<StringBuffer> allOtherValues = nextExpression.combineNext();
				for (StringBuffer sb : cValues) {
					String oldV = sb.toString();
					sb.setLength(0);
					sb.append(oldV + " "
							+ flatternToString(allOtherValues, false));
				}
			}
			return flatternToString(cValues, true);
		}

		@Override
		Set<StringBuffer> combineNext() {
			hasBeenEvalulated = true;
			Set<StringBuffer> cValues = new LinkedHashSet<StringBuffer>();
			for (Expression e : expressions) {
				Set<StringBuffer> innerValues = e.combineNext();
				add(cValues, innerValues);
			}
			if (nextExpression != null
					&& !nextExpression.hasThisBeenEvalulated()) {
				Set<StringBuffer> nextCValues = nextExpression.combineNext();
				Set<StringBuffer> allCombinedValues = new LinkedHashSet<StringBuffer>();
				for (StringBuffer sb : cValues) {
					for (StringBuffer sbsb : nextCValues) {
						allCombinedValues.add(new StringBuffer(sb.toString()
								+ sbsb.toString()));
					}
				}
				return allCombinedValues;
			} else {
				return cValues;
			}
		}

		@Override
		void appendValue(String s) {
			if (currentExpression == null) {
				currentExpression = new ValueExpression();
				this.expressions.add(currentExpression);
			}
			currentExpression.appendValue(s);
		}

		@Override
		void createNewValue() {
			currentExpression = new ValueExpression();
			this.expressions.add(currentExpression);
		}

		@Override
		void setNext(Expression e) {
			if (glevel > 0) {
				if (currentExpression != null) {
					currentExpression.setNext(e);
				}
			} else {
				// To change
				this.nextExpression = e;
			}
		}

		@Override
		public String toString() {
			StringBuffer sb = new StringBuffer();
			sb.append("{");
			for (Expression e : expressions) {
				String s = e.toString();
				sb.append(s + " ");
			}
			sb = new StringBuffer(sb.toString().trim());
			sb.append("}");
			if (this.nextExpression != null)
				sb.append(this.nextExpression.toString());
			return sb.toString();
		}

	} // end of CompoundExpression

	/*
	 * Add all values from s2 to s1
	 */
	static Set<StringBuffer> add(Set<StringBuffer> s1, Set<StringBuffer> s2) {
		for (StringBuffer sb : s2) {
			s1.add(sb);
		}
		return s1;
	}

	static String flatternToString(Set<StringBuffer> cValues,
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

	CartesianProductParser(String in) {
		this.input = in;
	}

	public String parse() {
		int mode = 0; // 0 means value expression, 1 means compound expression
		int pos = 0;
		char prevC = ' ';
		// Now i am going to parse the whole input string
		currentExpr = new ValueExpression();
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
					Expression newE = new CompoundExpression();
					currentExpr.setNext(newE);
					exprStack.push(currentExpr); // Save the current one
					// into the stack
					currentExpr = newE;
				} else {

				}
			} else if (c == '}') {
				glevel--;
				if (prevC == '}') {

				} else {
					currentExpr = exprStack.pop();
				}
				mode = 2;
			} else if (c == ',') {
				//if (mode == 1) {
				if(currentExpr instanceof ValueExpression) {
					prevCurrentExpr.createNewValue();
					currentExpr = prevCurrentExpr; 
				} else {
					currentExpr.createNewValue();
				}
				//} else {
				//	System.out.println("ERROR 1 - should not happen");
				//}
			} else {
				if(mode==2) { //Right off from the compound expression
					ValueExpression newV = new ValueExpression();
					newV.appendValue(c+"");
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


}
