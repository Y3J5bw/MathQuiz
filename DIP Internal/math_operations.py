"""This file deqls with the calculqtions as well as equations to be used in the quiz
    This is the only file that can be doc-tested or tested through other automated means due to its nature
    Each of these classes will have a __str__ decorator. This is purely preference as without the decorator, the same
    effect could be achieved by just calling the question gen function. My decision to use the __str__ decorator over
    just adding onto the question gen function is that it feels more pythonic, and better practice due to the fact that
    the main purpose of the __str__ decorator is to return a fancy string. THis method makes more sense to me
"""

import math
import cmath
import random


class Surds:
    """Perhaps the most complicated question here in terms of generation. There needs to be a check for all the square
        root numbers to be divisible by the same perfect square. The question is in the form of a+sqrt(b)... and the
        answer is in the same form except for when b is 1, which will then just return a.
    """
    def __init__(self, num_surds):
        self.num_surds = num_surds
        self.surd_nums = []
        self.reduced_forms = []
        self.sqrt_symbol = '\u221A'  # Needed as .join does not accept '\'

    def question_gen(self, index):
        surd_coefficient, surd_number = (random.randrange(1, 51) for _ in range(2))
        self.surd_nums.append([surd_coefficient, surd_number])
        closest_root = int(math.sqrt(surd_number))
        for factor_root in range(closest_root, 1, -1):
            factor = factor_root ** 2
            if surd_number % factor == 0:
                self.reduced_forms.append([surd_coefficient * factor_root, surd_number // factor])
                return
        self.surd_nums.pop(index)
        self.question_gen(index)

    def get_answer(self):
        if self.reduced_forms[0][1] == 1:
            return f'{sum(embed_list[0] for embed_list in self.reduced_forms)}'
        return f'{sum(embed_list[0] for embed_list in self.reduced_forms)}*sqrt({self.reduced_forms[0][1]})'

    def __str__(self):
        if self.surd_nums:
            return f"Simplify {' + '.join(self.sqrt_symbol.join(map(str, embed)) for embed in self.surd_nums)}"

        for i in range(self.num_surds):
            self.question_gen(i)
            while self.reduced_forms[i][1] != self.reduced_forms[i-1][1]:
                self.surd_nums.pop(i)
                self.reduced_forms.pop(i)
                self.question_gen(i)
        return f"Simplify {' + '.join(self.sqrt_symbol.join(map(str, embed)) for embed in self.surd_nums)}"


class ComplexNumbers:
    """The methods used in this class is made very simple with the use of the cmath library, which does most of my work
        for me. The class will choose between polar or rectangular form and produce the question and answer accordingly.
    """
    def __init__(self):
        self.forms = ('polar', 'rectangular')
        self.form = None
        self.convert_form = None
        self.equation = None

    def question_gen(self):
        self.form = random.choice(self.forms)
        if self.form == 'polar':
            self.equation = [random.randrange(1, 10), random.uniform(-cmath.pi, cmath.pi)]
            self.convert_form = self.forms[1]
            return f'{self.equation[0]:.2f}*cis({self.equation[1]:.2f})'

        else:
            self.equation = complex(random.uniform(-5, 5), random.uniform(-5, 5))
            self.convert_form = self.forms[0]
            return f'{self.equation.real:.2f} + {self.equation.imag:.2f}i'

    def get_answer(self):
        if self.form == 'polar':
            if cmath.rect(self.equation[0], self.equation[1]).imag > 0:
                return f'{cmath.rect(self.equation[0], self.equation[1]).real:.2f}+' \
                       f'{cmath.rect(self.equation[0], self.equation[1]).imag:.2f}i'
            else:
                return f'{cmath.rect(self.equation[0], self.equation[1]).real:.2f}' \
                       f'{cmath.rect(self.equation[0], self.equation[1]).imag:.2f}i'

        else:
            x, y = cmath.polar(self.equation)
            return f'{x:.2f}*cis({y:.2f})'

    def __str__(self):
        self.question_gen()
        return f'Convert {self.question_gen()} to {self.convert_form} form'


class Polynomials:
    """This class is about long division of polynomials. Due to the simplicity of the questions produced, indexing
        through a list is enough and implementation of a coefficient class or the SymPy module is unnecessary.
    """
    def __init__(self):
        self.divisor = [1]
        self.dividend = [0]
        self.quotient = []

    def question_gen(self):
        while self.dividend[0] <= self.divisor[0]:
            self.divisor, self.dividend = ([random.randrange(1, 10) for _ in range(i + 2)] for i in range(2))

    def get_answer(self):
        dividend = self.dividend[:]
        for _ in range(len(dividend)):
            if len(dividend) != len(self.divisor) - 1:
                division = dividend[0] / self.divisor[0]
                self.quotient.append(division)
                dividend.pop(0)

                dividend[0] -= self.divisor[1] * division

        return f'{self.quotient[0]:.2f}x+{self.quotient[1]:.2f}r{dividend[0]:.2f}'

    def __str__(self):
        self.question_gen()

        divisor, dividend = ([] for _ in range(2))

        for parse_list, original_list in zip([divisor, dividend], [self.divisor, self.dividend]):
            for index, constant in enumerate(original_list):
                power = len(original_list) - 1
                if power - index > 1:
                    parse_list.append(f'{constant}x^{power}')

                elif power - index == 1:
                    parse_list.append(f'{constant}x')

                else:
                    parse_list.append(f'{constant}')

        return f'What is ({" + ".join(divisor)}) \u27CC ({" + ".join(dividend)})'


class Differentiation:
    """Probably the most basic class, just filled with a lot of elif statements. This class makes basic use of the chain
        rule.
    """
    def __init__(self):
        self.diff_var_list = ['e^', 'ln', 'sin', 'cos', 'tan']
        self.diff_var = None
        self.a = None
        self.x = None

    def question_gen(self):
        self.diff_var = self.diff_var_list.index(random.choice(self.diff_var_list))
        self.a, self.x = [random.randrange(1, 9) for _ in range(2)]
        return f'{self.a}*{self.diff_var_list[self.diff_var]}({self.x}x)'

    def get_answer(self):
        if self.diff_var == 0:
            return f'{self.a * self.x}*{self.diff_var_list[self.diff_var]}({self.x}x)'

        elif self.diff_var == 1:
            return f'({self.a * self.x})/({self.diff_var_list[self.diff_var]}({self.x}x)'

        elif self.diff_var == 2:
            return f'{self.a * self.x}*cos({self.x}x)'

        elif self.diff_var == 3:
            return f'{- self.a * self.x}*sin({self.x}x)'

        else:
            return f'{self.a * self.x}*sec^(2)({self.x}x)'

    def __str__(self):
        return f'Differentiate {self.question_gen()}'


if __name__ == '__main__':
    a = Polynomials()
    print(a)
    print(a.get_answer())
