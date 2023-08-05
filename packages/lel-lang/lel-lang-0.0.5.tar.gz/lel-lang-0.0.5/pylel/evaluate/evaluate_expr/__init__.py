from pylel.token import Symbols, Token
from pylel.libraries import LIBRARIES
from .language_core import CORE
from .language_core.lel_call_function import lel_call_function
from .language_core.standard_language_functions import STANDARD
from .find_base_path import find_base_path

def find_in_scope(scope, name):
	if not scope:
		return None
	if name in scope.variables:
		return scope.variables[name]
	return find_in_scope(scope.upper_scope, name)

def _evaluate_list(scope, expr_list):
	return [evaluate_expr(scope, sub_expr) for sub_expr in expr_list]

def evaluate_expr(scope, expr):
	if isinstance(expr, list):
		# Evaluate empty block
		if not expr:
			return Token(Symbols.LIST, [])

		# List of expressions?
		# Evaluate a block in series
		if isinstance(expr[0], list):
			return _evaluate_list(scope, expr)[-1]

		# The rest of the expressions are based on identifiers
		identifier_token = expr[0]
		if identifier_token.type == Symbols.IDENTIFIER:
			# Core language functions
			if identifier_token.value in CORE:
				return CORE[identifier_token.value](evaluate_expr, scope, expr)

			# Standard languages functions that manipulate primitives
			if identifier_token.value in STANDARD:
				evaluated_expr = _evaluate_list(scope, expr[1:])
				return STANDARD[identifier_token.value](*evaluated_expr)

			# Libraries that are added to the runtime with use identifier
			if identifier_token.value in LIBRARIES:
				evaluated_expr = _evaluate_list(scope, expr[1:])
				return LIBRARIES[identifier_token.value](*evaluated_expr)

			# Run a scoped function if one is found
			scoped_function = find_in_scope(scope, identifier_token.value)
			if scoped_function and \
				scoped_function.type == Symbols.FUNCTION_REFERENCE:
				evaluated_expr = _evaluate_list(scope, expr[1:])
				return lel_call_function(evaluate_expr, scope, \
						evaluated_expr, scoped_function.value)

		# Try and evaluate them single expression
		return _evaluate_list(scope, expr)[-1]
	else:
		# Return the value of primitives directly in their tokenised form
		if expr.is_token and \
			( \
				expr.type == Symbols.RANGE \
				or expr.type == Symbols.STRING \
				or expr.type == Symbols.NUMBER \
				or expr.type == Symbols.BOOLEAN \
				or expr.type == Symbols.FUNCTION_REFERENCE \
				or expr.type == Symbols.LIST \
			):
			return expr

		# Identifiers will be a function reference or a variable
		if expr.type == Symbols.IDENTIFIER:
			identifier_type = expr.value

			# Pass back variable value. Explicitly check null instead of other
			# falsey values that might really be contained in the variable
			variable_in_scope = find_in_scope(scope, identifier_type)
			if variable_in_scope:
				return variable_in_scope

	raise Exception("Unrecognised expression: {}".format(expr))
