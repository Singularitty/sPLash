from parser.ast_nodes import *
from .types import *


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

    def get_type(self, name: str) -> TypeName | ArrayType:
        """
        Retrieves the type associated with the given name from the context's stack.
        """
        for scope in self.stack:
            if name in scope:
                return scope[name]
        self.errors.append(
            TypeError(f"Identifier {name} is not in the context"))

    def set_type(self, name: str, value: TypeName | ArrayType) -> None:
        """
        Sets the type for the given name in the current scope.
        """
        scope = self.stack[0]
        scope[name] = value

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
                # Start by adding function signature to the context if it's not present
                return_type = node.type_.ttype
                params = node.parameters
                fname = node.func_id.identifier
                if not self.ctx.has_identifier(fname):
                    signature = (return_type, [x[1].ttype for x in params])
                    self.ctx.set_type(node.func_id.identifier, signature)

                self.ctx.enter_scope()
                self.ctx.set_type(self.RETURN_CODE, return_type)
                for (id_node, type_node) in params:
                    self.ctx.set_type(id_node.identifier, type_node.ttype)
                self.ctx.enter_scope()
                for statement in node.body.statements:
                    self.verify(statement)
                self.ctx.exit_scope()
                self.ctx.exit_scope()
            case ValueDefinitionNode():
                name = node.var_id.identifier
                expected_type = node.type_.ttype
                if self.ctx.has_identifier_in_current_scope(name):
                    self.errors.append(TypeError(
                        f"Line:{node.line}, Column:{node.column}: Variable {name} is already defined in the context"))
                self.ctx.set_type(name, expected_type)
                returned_type = self.verify(node.expr)
                if not (expected_type == TypeName.DOUBLE and returned_type == TypeName.INT):
                    if returned_type != expected_type:
                        self.errors.append(TypeError(
                            f"Line:{node.line}, Column:{node.column}: Expected a value of type {expected_type}, got {returned_type} instead"))

    def __verify_statement(self, node: StmtNode):
        match node:
            case LocalVariableDeclarationNode():
                name = node.var_id.identifier
                if self.ctx.has_identifier_in_current_scope(name):
                    self.errors.append(TypeError(
                        f"Line:{node.line}, Column:{node.column}: Variable {name} is already in the context"))
                ttype = node.type_.ttype
                self.ctx.set_type(name, ttype)

            case VariableAssignmentStmtNode():
                name = node.var_id.identifier
                assigned_expr = node.expr
                if not self.ctx.has_identifier(name):
                    self.errors.append(TypeError(
                        f"Line:{node.line}, Column:{node.column}: Variable {name} is not defined in the cotnext"))
                expected_type = self.ctx.get_type(name)
                returned_type = self.verify(assigned_expr)
                if not (expected_type == TypeName.DOUBLE and returned_type == TypeName.INT):
                    if returned_type != expected_type:
                        self.errors.append(TypeError(
                            f"Line:{node.line}, Column:{node.column}: Expected assigned value to be of tpye {expected_type}, got {returned_type}"))

            case ExprStmtNode():
                self.verify(node.expr)

            case ReturnStmtNode():
                return_type = self.verify(node.return_expr)
                expected_return = self.ctx.get_type(self.RETURN_CODE)
                if return_type != expected_return:
                    self.errors.append(TypeError(
                        f"Line:{node.line}, Column:{node.column}: Expected return expression of type {expected_return}, got {return_type} instead"))

            case IfStmtNode():
                cond_type = self.verify(node.conditional)
                if cond_type != TypeName.INT:
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
                if guard_type != TypeName.INT:
                    self.errors.append(TypeError(
                        f"Line:{node.line}, Column:{node.column}: Guard on while statement must be of type Int and have value 0 or 1, go {guard_type} instead"))
                self.ctx.enter_scope()
                for st in node.do_block.statements:
                    self.verify(st)
                self.ctx.exit_scope()

            case LocalValueDefinitionNode():
                name = node.var_id.identifier
                expected_type = node.type_.ttype
                if self.ctx.has_identifier_in_current_scope(name):
                    self.errors.append(TypeError(
                        f"Line:{node.line}, Column:{node.column}: Variable {name} is already defined in the context"))
                self.ctx.set_type(name, expected_type)
                returned_type = self.verify(node.expr)
                if not (expected_type == TypeName.DOUBLE and returned_type == TypeName.INT):
                    if returned_type != expected_type:
                        self.errors.append(TypeError(
                            f"Line:{node.line}, Column:{node.column}: Expected a value of type {expected_type}, got {returned_type} instead"))

    def __verify_declaration(self, node: DeclarationNode):
        match node:
            case FunctionDeclarationNode():
                name = node.func_id.identifier
                if self.ctx.has_identifier(name):
                    self.errors.append(TypeError(
                        f"Line:{node.line}, Column:{node.column}: Function {name} was alread declared or defined in the context"))
                f_type = node.type_.ttype
                parameters_type = []
                for (_, type_node) in node.parameters:
                    parameters_type.append(type_node.ttype)
                signature = (f_type, parameters_type)
                self.ctx.set_type(name, signature)
            case VariableDeclarationNode():
                name = node.var_id.identifier
                if self.ctx.has_identifier_in_current_scope(node.var_id):
                    self.errors.append(TypeError(
                        f"Line:{node.line}, Column:{node.column}: Variable {node.var_id} is already in the context"))
                ttype = node.type_.ttype
                self.ctx.set_type(name, ttype)

    def __verify_expression(self, node: ExprNode):
        match node:
            case IntLiteralExprNode():
                return TypeName.INT
            case FloatLiteralExprNode():
                return TypeName.DOUBLE
            case BoolLiteralExprNode():
                return TypeName.INT
            case StrExprNode():
                return TypeName.STRING

            case IdentifierExprNode():
                name = node.identifier
                if not self.ctx.has_identifier(name):
                    self.errors.append(TypeError(
                        f"Line:{node.line}, Column:{node.column}: Variable {name} is not defined in the context"))
                return self.ctx.get_type(name)

            case FuncReturnExprNode():
                fname = node.func_id.identifier
                args = node.arguments
                (expected_return, parameter_types) = self.ctx.get_type(fname)
                if len(args) != len(parameter_types):
                    self.errors.append(TypeError(
                        f"Line:{node.line}, Column:{node.column}: {fname} expected {len(parameter_types)} arguments, got {len(args)} instead"))
                for (i, (arg, par_type)) in enumerate(zip(args, parameter_types)):
                    arg_type = self.verify(arg)
                    if arg_type != par_type:
                        index = i+1
                        self.errors.append(TypeError(
                            f"Line:{node.line}, Column:{node.column}: Expected {par_type} for argument #{index}, got {arg_type} instead."))
                return expected_return

            case BinaryExprNode():
                operator = node.operator
                match operator:
                    case BinaryOperator.PLUS | BinaryOperator.MINUS | BinaryOperator.MUL:
                        expected_type = [TypeName.INT, TypeName.DOUBLE]
                        exp1_type = self.verify(node.expr1)
                        exp2_type = self.verify(node.expr2)
                        if exp1_type not in expected_type:
                            self.errors.append(TypeError(
                                f"Line:{node.line}, Column:{node.column}: Expected type for the first operand should be either int or double, got {exp1_type}"))
                        if exp2_type not in expected_type:
                            self.errors.append(TypeError(
                                f"Line:{node.line}, Column:{node.column}: Expected type for the second operand should be either int or double, got {exp2_type}"))
                        if exp1_type == TypeName.DOUBLE or exp2_type == TypeName.DOUBLE:
                            return TypeName.DOUBLE
                        return TypeName.INT
                    case BinaryOperator.DIV:
                        expected_type = [TypeName.INT, TypeName.DOUBLE]
                        exp1_type = self.verify(node.expr1)
                        exp2_type = self.verify(node.expr2)
                        if exp1_type not in expected_type:
                            self.errors.append(TypeError(
                                f"Line:{node.line}, Column:{node.column}: Expected type for the first operand should be either int or double, got {exp1_type}"))
                        if exp2_type not in expected_type:
                            self.errors.append(TypeError(
                                f"Line:{node.line}, Column:{node.column}: Expected type for the second operand should be either int or double, got {exp2_type}"))
                        return TypeName.DOUBLE
                    case BinaryOperator.EQ | BinaryOperator.NEQ | BinaryOperator.GE | BinaryOperator.GT | BinaryOperator.LE | BinaryOperator.LT:
                        expected_type = [TypeName.INT, TypeName.DOUBLE]
                        exp1_type = self.verify(node.expr1)
                        exp2_type = self.verify(node.expr2)
                        if exp1_type not in expected_type:
                            self.errors.append(TypeError(
                                f"Line:{node.line}, Column:{node.column}: Expected type for the first operand should be either int or double, got {exp1_type}"))
                        if exp2_type not in expected_type:
                            self.errors.append(TypeError(
                                f"Line:{node.line}, Column:{node.column}: Expected type for the second operand should be either int or double, got {exp2_type}"))
                        return TypeName.INT
                    case BinaryOperator.AND | BinaryOperator.OR | BinaryOperator.MOD:
                        expected_type = TypeName.INT
                        exp1_type = self.verify(node.expr1)
                        exp2_type = self.verify(node.expr2)
                        if exp1_type != expected_type:
                            self.errors.append(TypeError(
                                f"Line:{node.line}, Column:{node.column}: Expected type for the first operand should be either int or double, got {exp1_type}"))
                        if exp2_type != expected_type:
                            self.errors.append(TypeError(
                                f"Line:{node.line}, Column:{node.column}: Expected type for the second operand should be either int or double, got {exp2_type}"))
                        return TypeName.INT

            case UnaryExprNode():
                operator = node.operator
                match operator:
                    case UnaryOperator.NOT:
                        expected_type = TypeName.INT
                        expression_type = self.verify(node.expr)
                        if expression_type != expected_type:
                            self.errors.append(TypeError(
                                f"Line:{node.line}, Column:{node.column}: Expected type for operand should be either int, got {expression_type}"))
                        return TypeName.INT

            case IndexAccessExprNode():
                expected_type = self.verify(node.array)
                index_type = self.verify(node.index)
                if index_type != TypeName.INT:
                    self.errors.append(TypeError(
                        f"Line:{node.line}, Column:{node.column}: Expected Int type for array index got {index_type} instead"))
                return expected_type.element_type()
