from parser.ast_nodes import *
from .types import *



class Context(object):
    
    def __init__(self):
        self.stack = [{}]

    def get_type(self, name):
        for scope in self.stack:
            if name in scope:
                return scope[name]
        raise TypeError(f"Identifier {name} is not in the context")

    def set_type(self, name, value):
        scope = self.stack[0]
        scope[name] = value

    def has_identifier(self, name):
        for scope in self.stack:
            if name in scope:
                return True
        return False

    def has_identifier_in_current_scope(self, name):
        return name in self.stack[0]

    def enter_scope(self):
        self.stack.insert(0, {})

    def exit_scope(self):
        self.stack.pop()


class TypeChecker:

    RETURN_CODE = "$ret"

    def __init__(self, ast: ProgramNode, ctx: Context = Context()):
        self.ast = ast
        self.ctx = ctx
        self.errors = []

    def verify(self, node: Node):
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
                self.ctx.enter_scope()
                return_type = node.type_
                params = node.parameters
                self.ctx.set_type(self.RETURN_CODE, return_type)
                for (id_node, type_node) in params:
                    self.ctx.set_type(id_node.identifier, type_node.ttype)
                self.ctx.enter_scope()
                for statement in node.body:
                    self.verify(statement)
                self.ctx.exit_scope()
                self.ctx.exit_scope()
            case ValueDefinitionNode():
                name = node.var_id
                expected_type = node.type_
                if self.ctx.has_identifier_in_current_scope(name):
                    raise TypeError(f"Variable {name} is already defined in the context")
                self.ctx.set_type(name, ttype)
                returned_type = self.verify(node.expr)
                if returned_type != expected_type:
                    raise TypeError(f"Expected a value of type {expected_type}, got {returned_type} instead")

    def __verify_statement(self, node: StmtNode):
        match node:
            case LocalVariableDeclarationNode():
                name = node.var_idopen new window in neovim
                if self.ctx.has_identifier_in_current_scope(node.var_id):
                    raise TypeError(f"Variable {node.var_id} is already in the context")
                ttype = node.type_.ttype
                self.ctx.set_type(name, ttype)
            case VariableAssignmentStmtNode():
                name = node.var_id
                assigned_expr = node.expr
                if not self.ctx.has_identifier(name):
                    raise TypeError(f"Variable {name} is not defined in the cotnext")
                expected_type = self.ctx.get_type(name)
                returned_type = self.verify(assigned_expr)
                if returned_type != expected_type:
                    raise TypeError(f"Expected assigned value to be of tpye {expected_type}, got {returned_type}")
            case ExprStmtNode():
                self.verify(node.expr)
            case ReturnStmtNode():
                return_type = self.verify(node.return_expr)
                expected_return = self.ctx.get_type(self.RETURN_CODE)
                if returned_type != expected_return:
                    raise TypeError(f"Expected return expression of type {expected_return}, got {return_type} instead")
            case IfStmtNode():
                cond = node.conditional
                cond_type = self.verify(cond)
                if self.verify(cond) != TypeName.INT:
                    raise TypeError(f"Condition on if statement must be of type Int and have value 0 or 1, got {cond_type} instead")
                self.ctx.enter_scope()
                for st in node.then_block:
                    self.verify(st)
                self.ctx.exit_scope()
                if node.else_block is not None:
                    self.ctx.enter_scope()
                    for st in node.else_block:
                        self.verify(st)
                    self.ctx.exit_scope()    
            case WhileStmtNode():
                guard = node.guard
                guard_type = self.verify(guard)
                if guard_type != TypeName.INT:
                    raise TypeError(f"Guard on while statement must be of type Int and have value 0 or 1, go {guard_type} instead")
                self.ctx.enter_scope()
                for st in node.do_block:
                    self.verify(st)
                self.ctx.exit_scope()
            case LocalValueDefinitionNode():
                name = node.var_id
                expected_type = node.type_
                if self.ctx.has_identifier_in_current_scope(name):
                    raise TypeError(f"Variable {name} is already defined in the context")
                self.ctx.set_type(name, ttype)
                returned_type = self.verify(node.expr)
                if returned_type != expected_type:
                    raise TypeError(f"Expected a value of type {expected_type}, got {returned_type} instead")


    def __verify_declaration(self, node: DeclarationNode):
        match node:
            case FunctionDeclarationNode():
                name = node.func_id
                if self.ctx.has_var(name):
                    raise TypeError(f"Function {node.func_id} was alread declared or defined in the context")
                f_type = node.type_.ttype
                parameters_type = []
                for (_, type_node) in node.parameters:
                    parameters_type.append(type_node.ttype)
                signature = (f_type, parameters_type)
                self.ctx.set_type(name, signature)
            case VariableDeclarationNode():
                name = node.var_idopen new window in neovim
                if self.ctx.has_identifier_in_current_scope(node.var_id):
                    raise TypeError(f"Variable {node.var_id} is already in the context")
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
                    raise TypeError(f"Variable {name} is not defined in the context")
                return self.ctx.get_type(name)
            
            case FuncReturnExprNode():
                fname = node.func_name
                args = node.arguments
                (expected_return, parameter_types) = self.ctx.get_type(fname)
                for (i, (arg, par_type)) in enumerate(zip(args, parameter_types)):
                    arg_type = self.verify(arg)
                    if arg_type != par_type:
                        index = i+1
                        raise TypeError(f"Expected {par_type} for argument #{index}, got {arg_type} instead.")
                return expected_return
            
            case BinaryExprNode():
                operator = node.operator
                match operator:
                    case BinaryOperator.PLUS, BinaryOperator.MINUS, BinaryOperator.MUL:
                        expected_type = [TypeName.INT, TypeName.DOUBLE]
                        exp1_type = self.verify(node.expr1)
                        exp2_type = self.verify(node.expr2)
                        if exp1_type not in expected_type:
                            raise TypeError(f"Expected type for the first operand should be either int or double, got {exp1_type}")
                        if exp2_type not in expected_type:
                            raise TypeError(f"Expected type for the second operand should be either int or double, got {exp2_type}")
                        if exp1_type == TypeName.DOUBLE or exp2_type == TypeName.DOUBLE:
                            return TypeName.DOUBLE
                        return TypeName.INT
                    case BinaryOperator.DIV:
                        expected_type = [TypeName.INT, TypeName.DOUBLE]
                        exp1_type = self.verify(node.expr1)
                        exp2_type = self.verify(node.expr2)
                        if exp1_type not in expected_type:
                            raise TypeError(f"Expected type for the first operand should be either int or double, got {exp1_type}")
                        if exp2_type not in expected_type:
                            raise TypeError(f"Expected type for the second operand should be either int or double, got {exp2_type}")
                        return TypeName.DOUBLE
                    case BinaryOperator.EQ, BinaryOperator.NEQ, BinaryOperator.GE, BinaryOperator.GT, BinaryOperator.LE, BinaryOperator.LT:
                        expected_type = [TypeName.INT, TypeName.DOUBLE]
                        exp1_type = self.verify(node.expr1)
                        exp2_type = self.verify(node.expr2)
                        if exp1_type not in expected_type:
                            raise TypeError(f"Expected type for the first operand should be either int or double, got {exp1_type}")
                        if exp2_type not in expected_type:
                            raise TypeError(f"Expected type for the second operand should be either int or double, got {exp2_type}")
                        return TypeName.INT
                    case BinaryOperator.AND, BinaryOperator.OR, BinaryOperator.MOD:
                        expected_type = TypeName.INT
                        exp1_type = self.verify(node.expr1)
                        exp2_type = self.verify(node.expr2)
                        if exp1_type != expected_type:
                            raise TypeError(f"Expected type for the first operand should be either int or double, got {exp1_type}")
                        if exp2_type != expected_type:
                            raise TypeError(f"Expected type for the second operand should be either int or double, got {exp2_type}")
                        return TypeName.INT

            case UnaryExprNode():
                operator = node.operator
                match operator:
                    case UnaryOperator.NOT:
                        expected_type = TypeName.INT
                        exp_type = self.verify(node.eopen new window in neovimxpr)
                        if self.verify(node.expr) != expected_type:
                            raise TypeError(f"Expected type for operand should be either int, got {exp_type}")
                        return TypeName.INT
            
            case IndexAccessExprNode():
                expected_type = self.verify(node.array)
                index_type = self.verify(node.index)
                if index_type != TypeName.INT:
                    raise TypeError(f"Expected Int type for array index got {index_type} instead")
                return expected_type
