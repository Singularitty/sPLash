from parser.ast_nodes import *
from .types import *
from .liquidtypechecker import check_refinement

class Context(object):
    """
    Represents a context for type checking with a stack of scopes.
    """

    def __init__(self, errors):
        """
        Initializes a new Context with an empty stack.
        """
        self.stack = [{}]
        self.errors = errors

    def get_type(self, name: str, node) -> LiquidType:
        """
        Retrieves the type associated with the given name from the context's stack.
        Node parameter is just used for error messages
        """
        for scope in self.stack:
            if name in scope:
                return scope[name]
        raise TypeError(f"Line:{node.line}, Column:{node.column}, Identifier {name} is not in the context")

    def set_type(self, name: str, ttype: LiquidType) -> None:
        """
        Sets the type for the given name in the current scope.
        """
        scope = self.stack[0]
        scope[name] = ttype

    def has_identifier(self, name: str) -> bool:
        """
        Checks if the given name is in any scope of the context's stack.
        """
        for scope in self.stack:
            if name in scope:
                return True
        return False

    def has_identifier_in_current_scope(self, name: str) -> bool:
        """
        Checks if the given name is in the current scope of the context's stack.
        """
        return name in self.stack[0]

    def enter_scope(self) -> None:
        """
        Enters a new scope by adding an empty dictionary to the top of the stack.
        """
        self.stack.insert(0, {})

    def exit_scope(self) -> None:
        """
        Exits the current scope by removing the top dictionary from the stack.
        """
        self.stack.pop(0)

def subtype(type1 : LiquidType, type2 : LiquidType, Ctx: Context) -> bool:
    """Checks if type1 is a subtype of type2
    
    For primitive types, only Int is a subtype of Double:
        
        Int <: Double
        
    We then have the following subtyping relations:
    
        T <: T, forall T
    
        {x:T | p} <: T, forall T
        
    When both types are refined, we check the constraints.
    """
    
    if type1.is_refined() and not type2.is_refined():
        # {x:T | p} <: T, forall T
        if type1.ttype == type2.ttype:
            return True
        # {x:T | p} <: U, forall T <: U
        elif type1.ttype == TypeName.INT and type2.ttype == TypeName.DOUBLE:
            return True
        
    elif type1.is_refined() and type2.is_refined():
        if type1.ttype == type2.ttype:
            return check_refinement(type1, type2, Ctx)
        
        if type1.ttype == TypeName.INT and type2.ttype == TypeName.DOUBLE:
            return check_refinement(type1, type2, Ctx)
    
    else:
        # T <: T for all T
        if type1.ttype == type2.ttype:
            return True
        # Int <: Double
        elif type1.ttype == TypeName.INT and type2.ttype == TypeName.DOUBLE:
            return True
        
    return False

class TypeChecker:
    """
    Represents a type checker for a given AST, which verifies the types and raises TypeErrors if any issues are found.
    """

    RETURN_CODE = "$ret"

    def __init__(self, ast: ProgramNode):
        """
        Initializes a new TypeChecker with the given AST and context.

        Args:
            ast (ProgramNode): The abstract syntax tree to check.
            ctx (Context): The context for type checking. Defaults to an empty Context.
        """
        self.ast = ast
        self.errors = []
        self.ctx = Context(self.errors)
        self.verify(self.ast)
        if len(self.errors) == 0:
            self.valid = True
        else:
            self.valid = False

    def verify(self, node: Node) -> TypeName | ArrayType:
        """
        Verifies the types for the given node and its children.

        Args:
            node (Node): The node to check.

        Returns:
            Type: The type of the node, if applicable.
        """
        match node:
            case ProgramNode():
                for n in node.program_body:
                    self.verify(n)
                self.verify(node.main)
            case DefinitionNode():
                self.__verify_definition(node)
            case BlockNode():
                for stmt in node.statements:
                    self.__verify_statement(stmt)
            case StmtNode():
                self.__verify_statement(node)
            case DeclarationNode():
                self.__verify_declaration(node)
            case ExprNode():
                expr_type = self.__verify_expression(node)
                return expr_type

    def __verify_definition(self, node: DefinitionNode):
        match node:
            case FunctionDefinitionNode():
                # Start by adding function signature to the context if it wasn't declared previously
                params = node.parameters
                fname = node.func_id.identifier
                return_type = LiquidType(fname, node.type_.ttype, node.type_.refinement)
                if not self.ctx.has_identifier(fname):
                    signature = (return_type, [LiquidType(x[0].identifier, x[1].ttype, x[1].refinement) for x in params])
                    self.ctx.set_type(node.func_id.identifier, signature)
                # Now begin typchecking function body
                self.ctx.enter_scope()
                # Use return code to typecheck the return statement when we get to it
                self.ctx.set_type(self.RETURN_CODE, return_type)
                for (id_node, type_node) in params:
                    p_type = LiquidType(id_node.identifier, type_node.ttype, type_node.refinement)
                    self.ctx.set_type(id_node.identifier, p_type)
                self.ctx.enter_scope()
                for statement in node.body.statements:
                    self.verify(statement)
                self.ctx.exit_scope()
                self.ctx.exit_scope()
            case ValueDefinitionNode():
                name = node.var_id.identifier
                expected_type = LiquidType(name, node.type_.ttype, node.type_.refinement)
                if self.ctx.has_identifier_in_current_scope(name):
                    self.errors.append(TypeError(
                        f"Line:{node.line}, Column:{node.column}: Variable {name} is already defined in the context"))
                returned_type = self.verify(node.expr)
                if not subtype(returned_type, expected_type, self.ctx):
                    self.errors.append(TypeError(
                        f"Line:{node.line}, Column:{node.column}: Expected a value of type {expected_type}, got {returned_type} instead"))
                self.ctx.set_type(name, expected_type)

    def __verify_statement(self, node: StmtNode):
        match node:
            case LocalVariableDeclarationNode():
                name = node.var_id.identifier
                if self.ctx.has_identifier_in_current_scope(name):
                    self.errors.append(TypeError(
                        f"Line:{node.line}, Column:{node.column}: Variable {name} is already in the context"))
                var_type = LiquidType(name, node.type_.ttype, node.type_.refinement)
                self.ctx.set_type(name, var_type)

            case VariableAssignmentStmtNode():
                name = node.var_id.identifier
                assigned_expr = node.expr
                if not self.ctx.has_identifier(name):
                    self.errors.append(TypeError(
                        f"Line:{node.line}, Column:{node.column}: Variable {name} is not defined in the cotnext"))
                expected_type = self.ctx.get_type(name, node)
                returned_type = self.verify(assigned_expr)
                # Allows the assignemnt of a Int to a Double variable, the Int is casted to a Double
                if not subtype(returned_type, expected_type, self.ctx):
                    self.errors.append(TypeError(
                        f"Line:{node.line}, Column:{node.column}: Expected assigned value to be of tpye {expected_type}, got {returned_type}"))

            case ExprStmtNode():
                self.verify(node.expr)

            case ReturnStmtNode():
                return_type = self.verify(node.return_expr)
                expected_return = self.ctx.get_type(self.RETURN_CODE, node)
                if not subtype(return_type, expected_return, self.ctx):
                    self.errors.append(TypeError(
                        f"Line:{node.line}, Column:{node.column}: Expected return expression of type {expected_return}, got {return_type} instead"))

            case IfStmtNode():
                cond_type = self.verify(node.conditional)
                if not subtype(cond_type, LiquidType(None, TypeName.INT, None), self.ctx):
                    self.errors.append(TypeError(
                        f"Line:{node.line}, Column:{node.column}: Condition on if statement must be of type Int and have value 0 or 1, got {cond_type} instead"))
                self.ctx.enter_scope()
                for st in node.then_block.statements:
                    self.verify(st)
                self.ctx.exit_scope()
                if node.else_block is not None:
                    self.ctx.enter_scope()
                    for st in node.else_block.statements:
                        self.verify(st)
                    self.ctx.exit_scope()

            case WhileStmtNode():
                guard = node.guard
                guard_type = self.verify(guard)
                if not subtype(guard_type, LiquidType(None, TypeName.INT, None), self.ctx):
                    self.errors.append(TypeError(
                        f"Line:{node.line}, Column:{node.column}: Guard on while statement must be of type Int and have value 0 or 1, go {guard_type} instead"))
                self.ctx.enter_scope()
                for st in node.do_block.statements:
                    self.verify(st)
                self.ctx.exit_scope()

            case LocalValueDefinitionNode():
                name = node.var_id.identifier
                expected_type = LiquidType(name, node.type_.ttype, node.type_.refinement)
                if self.ctx.has_identifier_in_current_scope(name):
                    self.errors.append(TypeError(
                        f"Line:{node.line}, Column:{node.column}: Variable {name} is already defined in the context"))
                returned_type = self.verify(node.expr)
                # Allows the assignemnt of a Int to a Double variable, the Int is casted to a Double
                if not subtype(returned_type, expected_type, self.ctx):
                        self.errors.append(TypeError(
                            f"Line:{node.line}, Column:{node.column}: Expected a value of type {expected_type}, got {returned_type} instead"))
                self.ctx.set_type(name, expected_type)

    def __verify_declaration(self, node: DeclarationNode):
        match node:
            case FunctionDeclarationNode():
                name = node.func_id.identifier
                if self.ctx.has_identifier(name):
                    self.errors.append(TypeError(
                        f"Line:{node.line}, Column:{node.column}: Function {name} was alread declared or defined in the context"))
                return_type = LiquidType(name, node.type_.ttype, node.type_.refinement)
                parameters_type = [LiquidType(x[0].identifier, x[1].ttype, x[1].refinement) for x in node.parameters]
                signature = (return_type, parameters_type)
                self.ctx.set_type(name, signature)
            case VariableDeclarationNode():
                name = node.var_id.identifier
                if self.ctx.has_identifier_in_current_scope(node.var_id):
                    self.errors.append(TypeError(
                        f"Line:{node.line}, Column:{node.column}: Variable {node.var_id} is already in the context"))
                var_type = LiquidType(name, node.type_.ttype, node.type_.refinement)
                self.ctx.set_type(name, var_type)

    def __verify_expression(self, node: ExprNode):
        match node:
            case IntLiteralExprNode():
                return LiquidType(None, TypeName.INT, None)
            case FloatLiteralExprNode():
                return LiquidType(None, TypeName.DOUBLE, None)
            case BoolLiteralExprNode():
                return LiquidType(None, TypeName.INT, None)
            case StrExprNode():
                return LiquidType(None, TypeName.STRING, None)

            case IdentifierExprNode():
                name = node.identifier
                if not self.ctx.has_identifier(name):
                    self.errors.append(TypeError(
                        f"Line:{node.line}, Column:{node.column}: Variable {name} is not defined in the context"))
                return self.ctx.get_type(name, node)

            case FuncReturnExprNode():
                fname = node.func_id.identifier
                args = node.arguments
                (expected_return, parameter_types) = self.ctx.get_type(fname, node)
                if len(args) != len(parameter_types):
                    self.errors.append(TypeError(
                        f"Line:{node.line}, Column:{node.column}: {fname} expected {len(parameter_types)} arguments, got {len(args)} instead"))
                for (i, (arg, par_type)) in enumerate(zip(args, parameter_types)):
                    arg_type = self.verify(arg)
                    if not subtype(arg_type, par_type, self.ctx):
                        index = i+1
                        self.errors.append(TypeError(
                            f"Line:{node.line}, Column:{node.column}: Expected {par_type} for argument #{index}, got {arg_type} instead."))
                return expected_return

            case BinaryExprNode():
                operator = node.operator
                match operator:
                    case BinaryOperator.PLUS | BinaryOperator.MINUS | BinaryOperator.MUL:
                        exp1_type = self.verify(node.expr1)
                        exp2_type = self.verify(node.expr2)
                        if not subtype(exp1_type, LiquidType(None, TypeName.DOUBLE, None), self.ctx):
                            self.errors.append(TypeError(
                                f"Line:{node.line}, Column:{node.column}: Expected type for the first operand should be either Int or Double, got {exp1_type}"))
                        if not subtype(exp2_type, LiquidType(None, TypeName.DOUBLE, None), self.ctx):
                            self.errors.append(TypeError(
                                f"Line:{node.line}, Column:{node.column}: Expected type for the second operand should be either Int or Double, got {exp2_type}"))
                        # Allows operations with Int and Double, but always returns Double
                        if exp1_type.ttype == TypeName.DOUBLE or exp2_type.ttype == TypeName.DOUBLE:
                            return LiquidType(None, TypeName.DOUBLE, None)
                        return LiquidType(None, TypeName.INT, None)
                    
                    case BinaryOperator.DIV:
                        exp1_type = self.verify(node.expr1)
                        exp2_type = self.verify(node.expr2)
                        if not subtype(exp1_type, LiquidType(None, TypeName.DOUBLE, None), self.ctx):
                            self.errors.append(TypeError(
                                f"Line:{node.line}, Column:{node.column}: Expected type for the first operand should be either Int or Double, got {exp1_type}"))
                        if not subtype(exp2_type, LiquidType(None, TypeName.DOUBLE, None), self.ctx):
                            self.errors.append(TypeError(
                                f"Line:{node.line}, Column:{node.column}: Expected type for the second operand should be either Int or Double, got {exp2_type}"))
                        return LiquidType(None, TypeName.DOUBLE, None)
                    
                    case BinaryOperator.EQ | BinaryOperator.NEQ | BinaryOperator.GE | BinaryOperator.GT | BinaryOperator.LE | BinaryOperator.LT:
                        exp1_type = self.verify(node.expr1)
                        exp2_type = self.verify(node.expr2)
                        if not subtype(exp1_type, LiquidType(None, TypeName.DOUBLE, None), self.ctx):
                            self.errors.append(TypeError(
                                f"Line:{node.line}, Column:{node.column}: Expected type for the first operand should be Int or Double, got {exp1_type}"))
                        if not subtype(exp2_type, LiquidType(None, TypeName.DOUBLE, None), self.ctx):
                            self.errors.append(TypeError(
                                f"Line:{node.line}, Column:{node.column}: Expected type for the second operand should be Int or Double, got {exp2_type}"))
                        return LiquidType(None, TypeName.INT, None)
                    
                    case BinaryOperator.AND | BinaryOperator.OR | BinaryOperator.MOD:
                        exp1_type = self.verify(node.expr1)
                        exp2_type = self.verify(node.expr2)
                        if not subtype(exp1_type, LiquidType(None, TypeName.INT, None), self.ctx):
                            self.errors.append(TypeError(
                                f"Line:{node.line}, Column:{node.column}: Expected type for the first operand should be Int, got {exp1_type}"))
                        if not subtype(exp2_type, LiquidType(None, TypeName.INT, None), self.ctx):
                            self.errors.append(TypeError(
                                f"Line:{node.line}, Column:{node.column}: Expected type for the second operand should be Int, got {exp2_type}"))
                        return LiquidType(None, TypeName.INT, None)

            case UnaryExprNode():
                operator = node.operator
                match operator:
                    case UnaryOperator.NOT:
                        expression_type = self.verify(node.expr)
                        if not subtype(expression_type, LiquidType(None, TypeName.INT, None), self.ctx):
                            self.errors.append(TypeError(
                                f"Line:{node.line}, Column:{node.column}: Expected type for operand should be Int, got {expression_type}"))
                        return LiquidType(None, TypeName.INT, None)

            case IndexAccessExprNode():
                expected_type = self.verify(node.array)
                index_type = self.verify(node.index)
                if not subtype(index_type, LiquidType(None, TypeName.INT, None), self.ctx):
                    self.errors.append(TypeError(
                        f"Line:{node.line}, Column:{node.column}: Expected Int type for array index got {index_type} instead"))
                return LiquidType(None, expected_type.ttype.element_type(), None)