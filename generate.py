import sys

from crossword import *


class CrosswordCreator():

    def __init__(self, crossword):
        """
        Create new CSP crossword generate.
        """
        self.crossword = crossword
        self.domains = {
            var: self.crossword.words.copy()
            for var in self.crossword.variables
        }

    def letter_grid(self, assignment):
        """
        Return 2D array representing a given assignment.
        """
        letters = [
            [None for _ in range(self.crossword.width)]
            for _ in range(self.crossword.height)
        ]
        for variable, word in assignment.items():
            direction = variable.direction
            for k in range(len(word)):
                i = variable.i + (k if direction == Variable.DOWN else 0)
                j = variable.j + (k if direction == Variable.ACROSS else 0)
                letters[i][j] = word[k]
        return letters

    def print(self, assignment):
        """
        Print crossword assignment to the terminal.
        """
        letters = self.letter_grid(assignment)
        for i in range(self.crossword.height):
            for j in range(self.crossword.width):
                if self.crossword.structure[i][j]:
                    print(letters[i][j] or " ", end="")
                else:
                    print("█", end="")
            print()

    def save(self, assignment, filename):
        """
        Save crossword assignment to an image file.
        """
        from PIL import Image, ImageDraw, ImageFont
        cell_size = 100
        cell_border = 2
        interior_size = cell_size - 2 * cell_border
        letters = self.letter_grid(assignment)

        # Create a blank canvas
        img = Image.new(
            "RGBA",
            (self.crossword.width * cell_size,
             self.crossword.height * cell_size),
            "black"
        )
        font = ImageFont.truetype("assets/fonts/OpenSans-Regular.ttf", 80)
        draw = ImageDraw.Draw(img)

        for i in range(self.crossword.height):
            for j in range(self.crossword.width):

                rect = [
                    (j * cell_size + cell_border,
                     i * cell_size + cell_border),
                    ((j + 1) * cell_size - cell_border,
                     (i + 1) * cell_size - cell_border)
                ]
                if self.crossword.structure[i][j]:
                    draw.rectangle(rect, fill="white")
                    if letters[i][j]:
                        _, _, w, h = draw.textbbox((0, 0), letters[i][j], font=font)
                        draw.text(
                            (rect[0][0] + ((interior_size - w) / 2),
                             rect[0][1] + ((interior_size - h) / 2) - 10),
                            letters[i][j], fill="black", font=font
                        )

        img.save(filename)

    def solve(self):
        """
        Enforce node and arc consistency, and then solve the CSP.
        """
        self.enforce_node_consistency()
        self.ac3()
        return self.backtrack(dict())

    def enforce_node_consistency(self):
        """
        Update `self.domains` such that each variable is node-consistent.
        (Remove any values that are inconsistent with a variable's unary
         constraints; in this case, the length of the word.)
        """
        conjunto_variaveis = self.crossword.variables

        for variable in conjunto_variaveis:
            conjunto_palavras = self.domains[variable].copy()
            for word in conjunto_palavras:
                if len(word) != variable.length:
                    self.domains[variable].remove(word)

    def revise(self, x, y):
        """
        Make variable `x` arc consistent with variable `y`.
        To do so, remove values from `self.domains[x]` for which there is no
        possible corresponding value for `y` in `self.domains[y]`.

        Return True if a revision was made to the domain of `x`; return
        False if no revision was made.
        """
        index_xy = self.crossword.overlaps[x, y]
        x_domains_copy = self.domains[x].copy()
        bool_return_variable = False

        if index_xy is None:
            return bool_return_variable

        # Pegando todas as letras do y que cruza com x (apenas as letras)
        index_y_words = [word[index_xy[1]] for word in self.domains[y]]

        for word_x in x_domains_copy:
            # Analisando se as letras do x que cruza com y esta na lista index_y_words
            if word_x[index_xy[0]] not in index_y_words:
                self.domains[x].remove(word_x)
                bool_return_variable = True
        return bool_return_variable

    def ac3(self, arcs=None):
        """
        Update `self.domains` such that each variable is arc consistent.
        If `arcs` is None, begin with initial list of all arcs in the problem.
        Otherwise, use `arcs` as the initial list of arcs to make consistent.

        Return True if arc consistency is enforced and no domains are empty;
        return False if one or more domains end up empty.
        """
        queue = []

        if arcs is not None:
            queue = arcs.copy()
        else:
            for variable in self.crossword.variables:
                for neighbor in self.crossword.neighbors(variable):
                    queue.append((variable, neighbor))

        while len(queue) != 0:
            x, y = queue.pop()
            result = self.revise(x, y)

            if result == True:
                if len(self.domains[x]) == 0:
                    return False
                for neighbor in self.crossword.neighbors(x):
                    if neighbor != y: 
                        queue.append((neighbor, x))
        return True

    def assignment_complete(self, assignment):
        """
        Return True if `assignment` is complete (i.e., assigns a value to each
        crossword variable); return False otherwise.
        """
        for variable in self.crossword.variables:
            if variable not in assignment:
                return False
        return True

    def consistent(self, assignment):
        """
        Return True if `assignment` is consistent (i.e., words fit in crossword
        puzzle without conflicting characters); return False otherwise.
        """
        # Verificação para saber se alguma palavra foi usada mais de uma vez
        # O set() da uma polida na lista e remove os resultados duplicados
        assignment_set = set(assignment.values())
        if len(assignment_set) != len(assignment.values()):
            return False

        # Verificando se todas as palavras cabem nos espaços da crossword
        for variable in assignment:
            if len(assignment[variable]) != variable.length:
                return False

        # Verificando os cruzamentos entre palavras
        for variable in assignment:
            for neighbor in self.crossword.neighbors(variable):
                if neighbor in assignment:
                    index_x, index_y = self.crossword.overlaps[variable, neighbor]
                    if assignment[variable][index_x] != assignment[neighbor][index_y]:
                        return False
        return True

    def order_domain_values(self, var, assignment):
        """
        Return a list of values in the domain of `var`, in order by
        the number of values they rule out for neighboring variables.
        The first value in the list, for example, should be the one
        that rules out the fewest values among the neighbors of `var`.
        """
        palavras_var = {
            # Pegando todos os possiveis domains de var e colocando em uma dict
            domain_var: 0 for domain_var in self.domains[var]}
        # Pegando os espaços vizinhos e colocando na lista
        neighbors_var = self.crossword.neighbors(var)

        for palavra in palavras_var:
            for neighbor_variable in neighbors_var:
                if neighbor_variable not in assignment:
                    overlaps_x, overlaps_y = self.crossword.overlaps[var, neighbor_variable]
                    for neighbor in self.domains[neighbor_variable]:
                        if palavra[overlaps_x] != neighbor[overlaps_y] or palavra == neighbor:
                            palavras_var[palavra] += 1
        return sorted(palavras_var, key=palavras_var.get)

    def select_unassigned_variable(self, assignment):
        """
        Return an unassigned variable not already part of `assignment`.
        Choose the variable with the minimum number of remaining values
        in its domain. If there is a tie, choose the variable with the highest
        degree. If there is a tie, any of the tied variables are acceptable
        return values.
        """
        # Criando dicionario com listas das contagem de var e definindo suas variaveis, que serão o numero de palavras por dominio e quantidade de vizinhos
        dict_var = {
            var: [
                len(self.domains[var]),
                len(self.crossword.neighbors(var))
            ]
            for var in self.crossword.variables
            if var not in assignment
        } 

        # Caso todas as variaveis ja estejam no assignment, apenas retorna none para nao dar erro
        if not dict_var: 
            return None

        # Retornar a variavel escolhida usando min(), passando os criterios de menor palavras por dominio e maior numero de vizinhos
        return min(
            dict_var,  # Dict para o min()
            key=lambda var: (dict_var[var][0], -dict_var[var][1])  # Criterios de seleção
        )
        
    def backtrack(self, assignment):  # Função recursiva que integra a Backtracking Search
        """
        Using Backtracking Search, take as input a partial assignment for the
        crossword and return a complete assignment if possible to do so.

        `assignment` is a mapping from variables (keys) to words (values).

        If no assignment is possible, return None.
        """
        if self.assignment_complete(assignment):  # Checando se assigment esta completo, caso esteja, retorne-o
            return assignment

        var = self.select_unassigned_variable(assignment)  # Variavel
        order_var = self.order_domain_values(var, assignment)  # Palavras candidatas de var

        # Parte recursiva para ver se palavra funciona na variavel, caso funcione chama a função novamente, se a achar solução retorna a solução 
        # se nao tem solução, deleta a atribuição de var e tenta noavamente para a mesma variavel. A proxima variavel é escolhida dentro da chamada recursiva
        for palavra in order_var:
            assignment[var] = palavra
            if self.consistent(assignment):
                solution = self.backtrack(assignment)
                if solution is not None:
                    return solution
            del assignment[var]
        return None
    

def main():

    # Check usage
    if len(sys.argv) not in [3, 4]:
        sys.exit("Usage: python generate.py structure words [output]")

    # Parse command-line arguments
    structure = sys.argv[1]
    words = sys.argv[2]
    output = sys.argv[3] if len(sys.argv) == 4 else None

    # Generate crossword
    crossword = Crossword(structure, words)
    creator = CrosswordCreator(crossword)
    assignment = creator.solve()

    # Print result
    if assignment is None:
        print("No solution.")
    else:
        creator.print(assignment)
        if output:
            creator.save(assignment, output)


if __name__ == "__main__":
    main()
