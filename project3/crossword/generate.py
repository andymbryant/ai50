import sys
from copy import deepcopy
from queue import Queue
from itertools import chain
from crossword import *

CONSTRAINTS = []


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
        print crossword assignment to the terminal.
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
                        w, h = draw.textsize(letters[i][j], font=font)
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
        # Loop through all of the items in domain
        for var, value in self.domains.items():
            # Update the domains for each var to only include words that are equal to var.length
            self.domains[var] = [word for word in value if len(word) == var.length]

    def revise(self, x, y):
        """
        Make variable `x` arc consistent with variable `y`.
        To do so, remove values from `self.domains[x]` for which there is no
        possible corresponding value for `y` in `self.domains[y]`.

        Return True if a revision was made to the domain of `x`; return
        False if no revision was made.
        """
        revised = False
        x_domains = deepcopy(self.domains[x])
        y_domains = deepcopy(self.domains[y])

        # Get overlap coordinates for two variables
        try:
            i, j = self.crossword.overlaps[x, y]
        except:
            # If there is no overlap, then return revised (False)
            return revised

        # Loop through all words in x_domains
        for x_word in x_domains:
            # Make list of words in y_domain with value at j that is equal to value at i for x_word
            yj = [y_word for y_word in y_domains if y_word[j] == x_word[i]]
            # If there are no such words then remove x_word from domains
            if len(yj) == 0:
                self.domains[x].remove(x_word)
                # Update revised
                revised = True
        return revised

    def ac3(self, arcs=None):
        """
        Update `self.domains` such that each variable is arc consistent.
        If `arcs` is None, begin with initial list of all arcs in the problem.
        Otherwise, use `arcs` as the initial list of arcs to make consistent.

        Return True if arc consistency is enforced and no domains are empty;
        return False if one or more domains end up empty.
        """
        queue = Queue(maxsize=0)
        # If there are arcs add them all to queue
        if arcs is not None:
            for arc in arcs:
                queue.put(arc)
        else:
            # Get list of all variables in domains and all variables in the puzzle and make arcs between them
            for x in list(self.domains.keys()):
                for y in self.crossword.variables:
                    # Do not make arcs between the same variable
                    if str(x) != str(y):
                        new_arc = (x, y)
                        queue.put(new_arc)
        while not queue.empty():
            # Get first arc and unpack values
            x, y = queue.get()
            # Check if arc requires revisions
            if self.revise(x, y):
                # If domains is empty, return False
                if len(self.domains[x]) == 0:
                    return False
                # Add neighbors to queue, minus y
                for z in self.crossword.neighbors(x) - {y}:
                    queue.put((z,x))
        return True

    def assignment_complete(self, assignment):
        """
        Return True if `assignment` is complete (i.e., assigns a value to each
        crossword variable); return False otherwise.
        """
        # Loop through each variable and check if it has been assigned
        # If all have been assignment, then the assignment is complete
        for var in self.crossword.variables:
            if assignment.get(var) is None:
                return False
        return True

    def consistent(self, assignment):
        """
        Return True if `assignment` is consistent (i.e., words fit in crossword
        puzzle without conflicting characters); return False otherwise.
        """
        # Check if all values in the assignment are unique
        # Flatten list if multiple values
        assignment_values = [values for values in assignment.values()]
        assignment_values_flat = [item for sublist in assignment_values for item in sublist]
        if not self.are_values_unique(assignment_values):
            return False
        # Loop through the items in assignment
        for var, var_value in list(assignment.items()):
            # Check if length of var value is equal to var.length
            if var.length != len(var_value):
                return False
            # Check if there is a conflict within the var and its neighbors
            if self.is_conflict(var):
                return False
        return True

    def is_conflict(self, var):
        """
        Helper function for determining if there is a conflict within a var and its neighbors
        """
        # Copy the domains of the var
        var_domains = deepcopy(self.domains[var])
        # Get the neighbors of the var
        neighbors = self.crossword.neighbors(var)
        # Loop through neighbors
        for neighbor in neighbors:
            # Get the domains of the neighbors
            neighbor_domains = self.domains[neighbor]
            # Get overlap coordinates of var and neighbor
            i, j = self.crossword.overlaps[var, neighbor]
            # Loop through words in domains
            for var_word in var_domains:
                # Get all neighbor_words from neighbor_domain that have same char at j as var_word at i
                neighbor_words = [neighbor_word for neighbor_word in neighbor_domains if neighbor_word[j] == var_word[i]]
                # If there are no such words then there is a conflict
                if len(neighbor_words) == 0:
                    return True
        return False

    def are_values_unique(self, values):
        """
        Helper function for determining if incoming values are unique.
        """
        return len(values) == len(set(values))

    def order_domain_values(self, var, assignment):
        """
        Return a list of values in the domain of `var`, in order by
        the number of values they rule out for neighboring variables.
        The first value in the list, for example, should be the one
        that rules out the fewest values among the neighbors of `var`.
        """
        # domain_values = []
        # naive way is to return them all
        # least constraining values heuristic
        # choose the one that rules out the fewest possible options
        # 1:40:20
        # domain_values_sorted = sorted(domain_values.sort, key=lambda x: x.foo)

        domain_values = deepcopy(self.domains[var])


        return domain_values

    def select_unassigned_variable(self, assignment):
        """
        Return an unassigned variable not already part of `assignment`.
        Choose the variable with the minimum number of remaining values
        in its domain. If there is a tie, choose the variable with the highest
        degree. If there is a tie, any of the tied variables are acceptable
        return values.
        """
        # Get the total number of words in the puzzle
        total_num_words = len(self.crossword.words)
        # Initialize least_values list with one more number than total number of words
        least_values = [i for i in range(total_num_words + 1)]
        least_var = None
        # Loop through all variables in crossword
        for var in self.crossword.variables:
            # Check if var is not in assignment
            if var not in assignment:
                values = self.domains[var]
                # If the length of values is less than existing least_values then update least_var and least_values
                if len(values) < len(least_values):
                    least_values = values
                    least_var = var
                # If equal, compare the degree of current var and least_var
                elif len(values) == len(least_values):
                    if least_var is not None:
                        # Get the degree of least_var and the degree of current
                        least_var_degree = len(self.crossword.neighbors(least_var))
                        var_degree = len(self.crossword.neighbors(var))
                        # If degree of current is less than least_var, update values
                        if var_degree < least_var_degree:
                            least_values = values
                            least_var = var
                    else:
                        least_values = values
                        least_var = var
        return least_var

    def backtrack(self, assignment):
        """
        Using Backtracking Search, take as input a partial assignment for the
        crossword and return a complete assignment if possible to do so.

        `assignment` is a mapping from variables (keys) to words (values).

        If no assignment is possible, return None.
        """
        if self.assignment_complete(assignment):
            return assignment
        var = self.select_unassigned_variable(assignment)
        # for value in self.domains[var]:
        for value in self.order_domain_values(var, assignment):
            new_assignment = assignment.copy()
            new_assignment[var] = value
            if self.consistent(new_assignment):
                result = self.backtrack(new_assignment)
                if result is not None:
                    return result
                # del assignment[var]
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
    crossword = Crossword(sys.argv[1], sys.argv[2])
    creator = CrosswordCreator(crossword)
    assignment = creator.solve()

    # print result
    if assignment is None:
        print("No solution.")
    else:
        creator.print(assignment)
        if output:
            creator.save(assignment, output)

if __name__ == "__main__":
    main()
