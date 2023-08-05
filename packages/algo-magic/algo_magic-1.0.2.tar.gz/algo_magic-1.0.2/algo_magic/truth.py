from IPython.core.magic import (Magics, magics_class, line_cell_magic)
from itertools import product
import re

def truth(*tests, **kwargs):
    bools = kwargs.get("bools", ("False", "True"))
    width = max(len(bools[0]), len(bools[1]))
    (off, tests) = zip(*[(test.startswith("?"),test.lstrip("?").strip()) for test in tests])
    names = sorted(set(m.group(0) for m in re.finditer(r"\b\w\b", " ".join(tests))))
    labels = [name.ljust(width) for name in names] + list(tests)
    result = ["| %s |" % " | ".join(labels)]
    result.append("|-%s-|" % ("-|-".join("-" * len(label) for label in labels)))
    for values in product((0, 1), repeat = len(names)):
        cells = [bools[value].ljust(width) for value in values]
        for (i, test) in enumerate(tests):
            if off[i]:
                cells.append("".ljust(len(labels[i + len(names)])))
            else:
                for (name, value) in zip(names, values):
                    test = re.sub(r"\b%s\b" % name, str(value), test)
                cells.append(bools[eval(test)].ljust(len(labels[i + len(names)])))
        result.append("| %s |" % " | ".join(cells))
    return "\n".join(result)

@magics_class
class TruthMagics(Magics):
    @line_cell_magic
    def truth(self, line, cell = None, bools = ("False", "True")):
        """
        Truth Table Generator IPython magic extension

        Magic methods:
            %truth bool_expr

            %truth? bool_expr

            %truth01 bool_expr

            %truth bool_expr_1, bool_expr_2, ..., bool_expr_n

            %truth bool_expr_1, ? bool_expr_2, ..., bool_expr_n

            %%truth
            bool_expr_1
            bool_expr_2
            ...
            bool_expr_n

            %%truth
            bool_expr_1
            ? bool_expr_2
            ...
            bool_expr_n
        """
        if line:
            print(truth(*line.split(", "), bools = bools))
        elif cell:
            print(truth(*cell.split("\n"), bools = bools))
    
    @line_cell_magic
    def truth01(self, line, cell = None):
        self.truth(line, cell = cell, bools = "01")
    
    @line_cell_magic
    def truth10(self, line, cell = None):
        self.truth(line, cell = cell, bools = "01")
    
    @line_cell_magic
    def truthFV(self, line, cell = None):
        self.truth(line, cell = cell, bools = "FV")
    
    @line_cell_magic
    def truthVF(self, line, cell = None):
        self.truth(line, cell = cell, bools = "FV")
    
    @line_cell_magic
    def truthFT(self, line, cell = None):
        self.truth(line, cell = cell, bools = "FT")
    
    @line_cell_magic
    def truthTF(self, line, cell = None):
        self.truth(line, cell = cell, bools = "FT")


if __name__ == "__main__":
    print(truth("(a and b) or (b and c) or (not a and c)", bools = "01"))