package com.kw.cartesianproductinbashshell.expression;

import java.util.LinkedHashSet;
import java.util.Set;

import com.kw.cartesianproductinbashshell.CartesianProductParser;

public class CompoundExpression extends Expression {

	public CompoundExpression(CartesianProductParser ccp) {
		super(ccp);

	}

	Set<Expression> expressions = new LinkedHashSet<Expression>();
	Expression currentExpression = null; // This refers to the current
											// expression that it is working
											// on

	@Override
	public
	String eval() {
		Set<StringBuffer> cValues = combineNext();
		if (nextExpression != null && !nextExpression.hasThisBeenEvalulated()) {
			Set<StringBuffer> allOtherValues = nextExpression.combineNext();
			for (StringBuffer sb : cValues) {
				String oldV = sb.toString();
				sb.setLength(0);
				sb.append(oldV
						+ " "
						+ CartesianProductParser.flatternToString(
								allOtherValues, false));
			}
		}
		return CartesianProductParser.flatternToString(cValues, true);
	}

	@Override
	Set<StringBuffer> combineNext() {
		hasBeenEvalulated = true;
		Set<StringBuffer> cValues = new LinkedHashSet<StringBuffer>();
		for (Expression e : expressions) {
			Set<StringBuffer> innerValues = e.combineNext();
			CartesianProductParser.add(cValues, innerValues);
		}
		if (nextExpression != null && !nextExpression.hasThisBeenEvalulated()) {
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
	public
	void appendValue(String s) {
		if (currentExpression == null) {
			currentExpression = new ValueExpression(this.cpParser);
			this.expressions.add(currentExpression);
		}
		currentExpression.appendValue(s);
	}

	@Override
	public
	void createNewValue() {
		currentExpression = new ValueExpression(this.cpParser);
		this.expressions.add(currentExpression);
	}

	@Override
	public
	void setNext(Expression e) {
		if (this.cpParser.getLevel() > 0) {
			if (currentExpression != null) {
				currentExpression.setNext(e);
			}
		} else {
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
