package com.kw.cartesianproductinbashshell.expression;

import java.util.Set;

import com.kw.cartesianproductinbashshell.CartesianProductParser;


public abstract class Expression {
		protected Expression nextExpression = null;
		protected CartesianProductParser cpParser=null;

		Expression(CartesianProductParser ccp) {
			this.cpParser = ccp;
		}
		
		public abstract String eval();

		abstract Set<StringBuffer> combineNext();

		boolean hasBeenEvalulated = false;

		boolean hasThisBeenEvalulated() {
			return this.hasBeenEvalulated;
		}

		public void setNext(Expression e) {
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

		public abstract void appendValue(String s);

		public abstract void createNewValue();

	}
