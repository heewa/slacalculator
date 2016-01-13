from __future__ import division

import re
import math
from inspect import isroutine


MathConstants = {
    symbol: value
    for symbol, value in math.__dict__.iteritems()
    if isinstance(value, (float, int))
}
MathFunctions = {
    symbol: value
    for symbol, value in math.__dict__.iteritems()
    if symbol[:1] != '_' and isroutine(value)
}
MathContext = dict(MathConstants.items() + MathFunctions.items())


FunctionPattern = r'(?:(?:' + '|'.join(MathFunctions.keys()) + r')\s*\(\s*)'
NumberPattern = r'-?[0-9]*\.?[0-9]+'
OperatorPattern = r'(?:(?:[-+*%/\\]|\*\*|//)\s*)'
SymbolPattern = (
    r'(?:'  # the whole group
    r'(?:(?:\(+\s*)*' + FunctionPattern + r')*'
    r'(?:\(+\s*)*'  # if it starts with paren, spaces are allowed
    r'(?:'  # the number group, inside parens
    + NumberPattern +
    r'|' + '|'.join(MathConstants.keys()) + # math constants
    r')'  # end of number group
    r'(?:\)*\s*)*'  # ending parens and spaces, in any combination
    r')'  # end of whole group
)
ExpressionPattern = r'(?:' + SymbolPattern + OperatorPattern + ')+' + SymbolPattern
FormulaPattern = (
    ExpressionPattern + r'|' +
    FunctionPattern + NumberPattern + r'(?:\)*\s*)*'
)
FormulaRe = re.compile(FormulaPattern)


def find_and_calc(text):
    """Given a string, returns array of:
        (math expression, result of evaluating it)
    """
    maths = []

    for match in FormulaRe.finditer(text):
        formula = match.group(0)
        try:
            code = compile(formula, '<string>', 'eval', division.compiler_flag)

            result = eval(code, MathContext)

            if isinstance(result, float):
                result = '%.4f' % result
            elif isinstance(result, (int, long)) and result > 10**10:
                exp = int(math.log10(result))
                result = '%.4fe+%d' % (result / 10**exp, exp)

            maths.append((formula, result))
        except SyntaxError:
            pass
        except ZeroDivisionError:
            maths.append((formula, '<div by zero>'))

    return maths
