package com.kw.cartesianproductinbashshell.expression;

import java.util.LinkedHashSet;
import java.util.Set;

import com.kw.cartesianproductinbashshell.CartesianProductParser;

public class ValueExpression extends Expression {

	StringBuffer value = new StringBuffer();

	public ValueExpression(CartesianProductParser ccp) {
		super(ccp);
	}
	
	@Override
	public
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
		if (nextExpression == null || nextExpression.hasThisBeenEvalulated()) {
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
	public
	void appendValue(String s) {
		value.append(s);
	}

	@Override
	public
	void createNewValue() {
		// Do nothing here
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
