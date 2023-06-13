from z3 import Solver, Int, Real, Not, sat
from parser.ast_nodes import *
from .types import LiquidType

def check_refinement(type1: LiquidType, type2: LiquidType, ctx):
    """
    Checks if the refinement of type1 is a subtype of the refinement of type2.

    Args:
        type1 (LiquidType): The first type.
        type2 (LiquidType): The second type.
        ctx (Context): The context for type checking.

    Returns:
        bool: True if the refinement of type1 is a subtype of the refinement of type2, False otherwise.
    """
    # Create a new Z3 solver
    solver = Solver()

    # Symbolic variables for the refinements
    symbolic_vars = {}

    # Add the refinements of the context to the solver
    for frame in ctx.stack:
        for name, ttype in frame.items():
            if isinstance(ttype, tuple):
                # This happens when we have a function signature
                # In this case we have (return_type, [arg1_type, arg2_type, ...])
                for t in ttype[1]:
                    if t.refinement is not None:
                        if t.ttype == TypeName.DOUBLE:
                            symbolic_vars[t.var] = Real(t.var)
                        elif t.ttype == TypeName.INT:
                            symbolic_vars[t.var] = Int(t.var)
                        else:
                            raise TypeError("Only Int and Double types can be refined.")
                        solver.add(eval(str(t.refinement), symbolic_vars))
            elif ttype.refinement is not None:
                if ttype.ttype == TypeName.DOUBLE:
                    symbolic_vars[name] = Real(name)
                elif ttype.ttype == TypeName.INT:
                    symbolic_vars[name] = Int(name)
                else:
                    raise TypeError("Only Int and Double types can be refined.")
                solver.add(eval(str(ttype.refinement), symbolic_vars))

    # Add the refinement of type1 to the solver
    if type1.var not in symbolic_vars:
        if type1.ttype == TypeName.DOUBLE:
            symbolic_vars[type1.var] = Real(type1.var)
        elif type1.ttype == TypeName.INT:
            symbolic_vars[type1.var] = Int(type1.var)
        else:
            raise TypeError("Only Int and Double types can be refined.")
    solver.add(eval(str(type1.refinement), symbolic_vars))

    # Replace the symbolic variables of type2 with the ones of type1
    symbolic_vars[type2.var] = symbolic_vars[type1.var]
    # Check if the negation of the refinement of type2 is satisfiable
    solver.push()
    solver.add(Not(eval(str(type2.refinement), symbolic_vars)))
    #print(solver)
    if solver.check() == sat:
        # If it is, then type1 is not a subtype of type2
        return False
    solver.pop()

    # If it is unsat, then type1 is a subtype of type2
    return True
