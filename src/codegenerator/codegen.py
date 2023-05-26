from parser.ast_nodes import *

class Context(object):

    def __init__(self):
        self.global_pointers_ctx = {}
        self.functions_pointers_ctx = []
        self.global_values_ctx = {}
        self.functions_values_ctx = []
        self.function_params = []
        
    def set_param(self, name: str, ttype: str, reg: str) -> None:
        scope = self.function_params[0][1]
        scope[name] = ttype, reg

    def has_param_in_current_scope(self, name) -> bool:
        return name in self.function_params[0][1]

    def get_param(self, name: str) -> str:
        scope = self.function_params[0][1]
        if name in scope:
            return scope[name]

    def get_pointer(self, name: str) -> str:
        scope = self.functions_pointers_ctx[0][1]
        if name in scope:
            return scope[name]
            
    def get_pointer_global(self, name: str) -> str:
        if name in self.global_pointers_ctx:
            return self.global_pointers_ctx[name]
            
    def get_value(self, name: str) -> str:
        scope = self.functions_values_ctx[0][1]
        if name in scope:
            return scope[name]   
        
    def get_func_params(self, fname: str) -> str:
        for scope in self.function_params:
            if fname in scope[0]:
                return scope[1]
        
    def get_all_params(self) -> dict:
        return self.function_params[0][1]
            
    def get_value_global(self, name: str) -> str:
        if name in self.global_values_ctx:
            return self.global_values_ctx[name]
    
    def set_pointer_global(self, name: str, ttype: str, pointer: str) -> None:
        scope = self.global_pointers_ctx
        scope[name] = ttype, pointer

    def set_pointer(self, name: str, ttype: str, pointer: str) -> None:
        scope = self.functions_pointers_ctx[0][1]
        scope[name] = ttype, pointer
        
    def set_value(self, name: str, ttype: str) -> None:
        scope = self.functions_values_ctx[0][1]
        scope[name] = ttype
        
    def set_value_global(self, name: str, ttype: str) -> None:
        scope = self.global_values_ctx
        scope[name] = ttype

    def has_pointer_global(self, name: str) -> bool:
        if name in self.global_pointers_ctx:
            return True
        return False
    
    def has_pointer_in_current_scope(self, name: str) -> bool:
        return name in self.functions_pointers_ctx[0][1]
    
    def has_value_global(self, name: str) -> bool:
        if name in self.global_values_ctx:
            return True
        return False
    
    def has_value_in_current_scope(self, name: str) -> bool:
        return name in self.functions_values_ctx[0][1]

    def enter_function_scope(self, fname: str, expected_type: str) -> None:
        self.functions_pointers_ctx.insert(0, ((fname, expected_type) , {}))
        self.functions_values_ctx.insert(0, ((fname, expected_type) , {}))
        self.function_params.insert(0, ((fname, expected_type) , {}))
        
    def get_func_type(self, name: str) -> str:
        for (fname, expected_type), _ in self.function_params:
            if name == fname:
                return expected_type
        
    def get_context_function_signature(self) -> Tuple[str, str]:
        return self.functions_pointers_ctx[0][0]
    
    def exit_scope(self) -> None:
        self.functions_pointers_ctx.insert(-1, self.functions_pointers_ctx.pop(0))
        self.functions_values_ctx.insert(-1, self.functions_values_ctx.pop(0))
        self.function_params.insert(-1, self.function_params.pop(0))

class Emitter(object):
    
    def __init__(self):
        self.counter = 0
        self.counter2 = 0
        self.labels = 0
        self.lines = []
        self.heap = Context()

    def get_count(self):
        self.counter += 1
        return self.counter
    
    def get_count2(self):
        self.counter2 += 1
        return self.counter2
    
    def get_count3(self):
        self.labels += 1
        return self.labels
    
    def get_identifier(self):
        id = self.get_count()
        return f"cas_{id}"
    
    def __lshift__(self, v):
        self.lines.append(v)

    def get_code(self):
        return "\n".join(self.lines)
    
    def get_label(self):
        id = self.get_count3()
        return f"_label_{id}"
    
    def get_pointer_name(self):
        id = self.get_count2()
        return f"pont_{id}"

def compile(ast: ProgramNode) -> str:
    llvm = LLVMIRGenerator()
    return llvm.generate_code(ast)

class LLVMIRGenerator:


    module_functions = ["print_int", "print_string", "print_double",
                        "create_array_int", "create_array_double",
                        "write_to_array_int", "write_to_array_double",
                        "freeInt", "freeDouble"]

    def __init__(self):
        self.module = Emitter()
        self.__initiate_module()
        self.emitter = Emitter()
        self.ctx = Context()
        
    def convert_type(self, ttype) -> str:
        
        if isinstance(ttype, ArrayType):
            nest_level = ttype.nest_level
            match ttype.type_name:
                case "Double":
                    return "double" + "*"*nest_level
                case "Int":
                    return "i64" + "*"*nest_level
        else:
            match ttype:
                case "Double":
                    return "double"
                case "Int":
                    return "i64"
                case "String":
                    return "i8*"
                case "Void":
                    return "void"
            
    def cast_llvm_type(self, reg: str, desired_type: str) -> str:
            
            converted_reg = self.emitter.get_identifier()
            if desired_type == "i64":
                self.ctx.set_value(converted_reg, "i64")
                self.emitter << f"\t%{converted_reg} = fptosi double %{reg} to i64"
                return converted_reg
            else:
                self.ctx.set_value(converted_reg, "double")
                self.emitter << f"\t%{converted_reg} = sitofp i64 %{reg} to double"
                return converted_reg
            
    def cast_bool_int(self, reg: str, desired_type: str) -> str:
            
            converted_reg = self.emitter.get_identifier()
            if desired_type == "i1":
                self.ctx.set_value(converted_reg, "i64")
                self.emitter << f"\t%{converted_reg} = trunc i64 %{reg} to i1"
            else:
                self.ctx.set_value(converted_reg, "i1")
                self.emitter << f"\t%{converted_reg} = zext i1 %{reg} to i64"
            return converted_reg
        
            
    def cast_type(self, value: str, typename: str) -> str:
        
        match typename:
            case "double":
                return str(float(value))
            case "i64":
                return str(int(value))
            
    def __initiate_module(self):
        self.module << "; Module functions declarations and definitions\n"
        
        self.module << "; Declare C functions that will do the actual heavy work"
        self.module << "declare i32 @printf(i8*, ...)"
        self.module << "declare i8* @malloc(i64)\n"
        self.module << "declare void @free(i8*)"
        
        self.module << "; Print functions"
        self.module << """define void @print_int(i64 %i) { 
        %format = getelementptr inbounds [4 x i8], [4 x i8]* @int_format, i64 0, i64 0
        call i32 (i8*, ...) @printf(i8* %format, i64 %i) 
        ret void 
        }"""

        self.module << """define void @print_double(double %d) {
            %format = getelementptr inbounds [4 x i8], [4 x i8]* @double_format, i64 0, i64 0
            call i32 (i8*, ...) @printf(i8* %format, double %d)
            ret void
            }"""
            
        self.module << """define void @print_string(i8* %s) {
            %format = getelementptr inbounds [4 x i8], [4 x i8]* @string_format, i64 0, i64 0
            call i32 (i8*, ...) @printf(i8* %format, i8* %s)
            ret void
            }"""
        self.module << '@int_format = private unnamed_addr constant [4 x i8] c"%d\n\00"'
        self.module << '@double_format = private unnamed_addr constant [4 x i8] c"%f\n\00"'
        self.module << '@string_format = private unnamed_addr constant [4 x i8] c"%s\n\\00"'


        self.module << "\n; Array allocation"
        self.module << """define i64* @create_array_int(i64 %size) {
            %bytes = mul i64 %size, 4
            %mem = call i8* @malloc(i64 %bytes)
            %arr = bitcast i8* %mem to i64*
            ret i64* %arr
            }"""

        self.module << """define double* @create_array_double(i64 %size) {
            %bytes = mul i64 %size, 8
            %mem = call i8* @malloc(i64 %bytes)
            %arr = bitcast i8* %mem to double*
            ret double* %arr
            }"""

        self.module << """define void @write_to_array_int(i64* %arr, i64 %index, i64 %value) {
            %ptr = getelementptr inbounds i64, i64* %arr, i64 %index
            store i64 %value, i64* %ptr
            ret void
            }"""

        self.module << """define void @write_to_array_double(double* %arr, i64 %index, double %value) {
            %ptr = getelementptr inbounds double, double* %arr, i64 %index
            store double %value, double* %ptr
            ret void
            }"""
            
        self.module << """define void @freeInt(i64* %array) {
            %array_cast = bitcast i64* %array to i8*
            call void @free(i8* %array_cast)
            ret void
            }"""
            
        self.module << """define void @freeDouble(double* %array) {
            %array_cast = bitcast double* %array to i8*
            call void @free(i8* %array_cast)
            ret void
            }"""

        self.module << "\n; Start of program"

    def generate_code(self, node: Node):
        
        match node:
            case ProgramNode():
                # Include a prelude
                for n in node.program_body:
                    self.generate_code(n)
                self.generate_code(node.main)
                # Return the final code
                return self.module.get_code() + "\n" + self.emitter.get_code()
            case DefinitionNode():
                self.__defnition(node)
            case BlockNode():
                for stmt in node.statements:
                    self.__statement(stmt)
            case StmtNode():
                self.__statement(node)
            case DeclarationNode():
                self.__declaration(node)
            case ExprNode():
                self.__expression(node)
            
    def __defnition(self, node: DefinitionNode):
        
        match node:
            case FunctionDefinitionNode():
                
                fname = node.func_id.identifier
                ftype = self.convert_type(node.type_.ttype)
                params = node.parameters
                body = node.body
                    
                # Function signature
                fsignature = f"define {ftype} @{fname}("
                
                # Function params
                for i, (identifier, ttype) in enumerate(params):
                    param_type = self.convert_type(ttype.ttype)
                    param_name = identifier.identifier
                    if i == len(params) - 1:
                        fsignature += f"{param_type} %{param_name}"
                    else:
                        fsignature += f"{param_type} %{param_name}, " 
                    
                fsignature += ") {"
                
                self.emitter << fsignature
                
                # Alocate registers for the function params
                self.ctx.enter_function_scope(fname, ftype)
                for i, (id, ttype) in enumerate(params):
                    reg = self.emitter.get_pointer_name()
                    param_type = self.convert_type(ttype.ttype)
                    param_name = id.identifier
                    self.emitter << f"\t%{reg} = alloca {param_type}"
                    self.emitter << f"\tstore {param_type} %{param_name}, {param_type}* %{reg}"
                    self.ctx.set_param(param_name, param_type, reg)
                
                # Function body
                self.generate_code(body)
                
                self.ctx.exit_scope()
                
                if ftype == "void":
                    self.emitter << "\tret void"
                
                self.emitter << "}\n"
            case ValueDefinitionNode():
                
                var_name = node.var_id.identifier
                var_type = self.convert_type(node.type_.ttype)
                
                if isinstance(node.expr, IdentifierExprNode):
                    value = f"{var_type}* @{node.expr.identifier}"
                    self.ctx.set_pointer_global(var_name, var_type + "*", node.expr.identifier)
                else:
                    value = f"{var_type} {self.__expression(node.expr)}"
                    self.ctx.set_value_global(var_name, var_type)
                
                self.emitter << f"@{var_name} = global {value}\n"
            
    def __statement(self, node: StmtNode):
        
        match node:
            
            case ExprStmtNode():
                self.generate_code(node.expr)
            
            case LocalVariableDeclarationNode():
                # these nodes don't exist in the language???
                # I don't know why they were defined in the first place
                var_name = node.var_id.identifier
                var_type = self.convert_type(node.type_.ttype)
                
                self.emitter << f"\t%{var_name} = alloca {var_type}"
                
            case VariableAssignmentStmtNode():
                
                var_name = node.var_id.identifier
                
                val1 = self.__expression(node.expr)
                ttype, _ = self.ctx.get_pointer(var_name)
            
                if self.ctx.has_pointer_global(val1):
                    val1_type, _ = self.ctx.get_pointer_global(val1)
                    load_reg = self.emitter.get_identifier()
                    self.ctx.set_pointer(load_reg, val1_type, val1)
                    self.emitter << f"\t%{load_reg} = load {val1_type}, {val1_type}* @{val1}"
                    val1 = "%" + load_reg
                elif self.ctx.has_value_global(val1):
                    val1_type = self.ctx.get_value_global(val1)
                    load_reg = self.emitter.get_identifier()
                    self.ctx.set_pointer(load_reg, val1_type, val1)
                    self.emitter << f"\t%{load_reg} = load {val1_type}, {val1_type}* @{val1}"
                    val1 = "%" + load_reg
                elif self.ctx.has_param_in_current_scope(val1):
                    val1_type, reg1 = self.ctx.get_param(val1)
                    load_reg = self.emitter.get_identifier()
                    self.ctx.set_pointer(load_reg, val1_type, reg1)
                    self.emitter << f"\t%{load_reg} = load {val1_type}, {val1_type}* %{reg1}"
                    val1 = "%" + load_reg
                elif self.ctx.has_pointer_in_current_scope(val1):
                    val1_type, _ = self.ctx.get_pointer(val1)
                    load_reg = self.emitter.get_identifier()
                    self.ctx.set_pointer(load_reg, val1_type, val1)
                    self.emitter << f"\t%{load_reg} = load {val1_type}, {val1_type}* %{val1}"
                    val1 = "%" + load_reg
                elif self.ctx.has_value_in_current_scope(val1):
                    val1_type = self.ctx.get_value(val1)
                    val1 = "%" + val1
                elif isinstance(node.expr, IntLiteralExprNode):
                    val1_type = "i64"
                    if ttype != val1_type:
                        val1 = self.cast_type(val1, ttype)
                elif isinstance(node.expr, FloatLiteralExprNode):
                    val1_type = "double"
                    if ttype != val1_type:
                        val1 = self.cast_type(val1, ttype)
                elif isinstance(node.expr, StrExprNode):
                    val1_type = "i8*"
                    if ttype != val1_type:
                        val1 = self.cast_type(val1, ttype)
                    
                self.emitter << f"\tstore {ttype} {val1}, {ttype}* %{var_name}"
            
            
            case ExprStmtNode():
                self.__expression(node) # Call expression handlers, but do nothing with returned register
            case ReturnStmtNode():
                value = self.__expression(node.return_expr)
                _, ftype = self.ctx.get_context_function_signature()
                
                if self.ctx.has_value_global(value) or self.ctx.has_pointer_global(value):
                    return_reg = self.emitter.get_identifier()
                    self.ctx.set_value(return_reg, ftype)
                    self.emitter << f"\t%{return_reg} = load {ftype}, {ftype}* @{value}"
                    self.emitter << f"\tret {ftype} %{return_reg}"
                elif self.ctx.has_param_in_current_scope(value):
                    ptype, reg = self.ctx.get_param(value)
                    return_reg = self.emitter.get_identifier()
                    self.ctx.set_value(return_reg, ftype)
                    self.emitter << f"\t%{return_reg} = load {ftype}, {ptype}* %{reg}"
                    self.emitter << f"\tret {ftype} %{return_reg}"
                elif self.ctx.has_pointer_in_current_scope(value):
                    return_reg = self.emitter.get_identifier()
                    self.ctx.set_value(return_reg, ftype)
                    self.emitter << f"\t%{return_reg} = load {ftype}, {ftype}* %{value}"
                    self.emitter << f"\tret {ftype} %{return_reg}"
                elif self.ctx.has_value_in_current_scope(value):
                    self.emitter << f"\tret {ftype} %{value}"
                else:
                    self.emitter << f"\tret {ftype} {value}"
                    
            case IfStmtNode():
                
                condition_reg = self.__expression(node.conditional)
                
                then_label = f"if.then.{self.emitter.get_label()}"
                else_label = f"if.else.{self.emitter.get_label()}"
                end_label = f"if.end.{self.emitter.get_label()}"
                
                
                self.emitter << f"\tbr i1 %{condition_reg}, label %{then_label}, label %{else_label}"    
            
                # Then block
                self.emitter << f"{then_label}:"
                self.generate_code(node.then_block)
                self.emitter << f"\tbr label %{end_label}"
                
                # Else block
                self.emitter << f"{else_label}:"
                if node.else_block is not None:
                    self.generate_code(node.else_block)
                self.emitter << f"\tbr label %{end_label}"
               
                # End block
                self.emitter << f"{end_label}:"
            
            
            case WhileStmtNode():
                
                
                guard_label = f"while.guard.{self.emitter.get_label()}"
                body_label = f"while.body.{self.emitter.get_label()}"
                end_label = f"while.end.{self.emitter.get_label()}"
                
                self.emitter << f"\tbr label %{guard_label}"
                
                # Guard
                self.emitter << f"{guard_label}:"
                guard_reg = self.__expression(node.guard)
                self.emitter << f"\tbr i1 %{guard_reg}, label %{body_label}, label %{end_label}"
                
                # loop body
                self.emitter << f"{body_label}:"
                self.generate_code(node.do_block)
                self.emitter << f"\tbr label %{guard_label}"
                
                # end
                self.emitter << f"{end_label}:"
            
            case LocalValueDefinitionNode():
                
                var_name = node.var_id.identifier
                var_type = self.convert_type(node.type_.ttype)
                
                
                
                match node.expr:
                    case IdentifierExprNode():
                        reg = node.expr.identifier
                        if self.ctx.has_pointer_global(reg): 
                            ttype, _ = self.ctx.get_pointer_global(reg)
                            load_reg = self.emitter.get_identifier()
                            self.emitter << f"\t%{load_reg} = load {var_type}, {ttype}* %{reg}"
                            self.ctx.set_value(load_reg, ttype)
                            self.emitter << f"\t%{var_name} = alloca {var_type}"
                            self.emitter << f"\tstore {ttype} %{load_reg}, {var_type}* %{var_name}"
                            self.ctx.set_pointer(var_name, var_type, load_reg)
                        elif self.ctx.has_value_global(reg):                            
                            ttype, _ = self.ctx.get_value_global(reg)
                            load_reg = self.emitter.get_identifier()
                            self.emitter << f"\t%{load_reg} = load {var_type}, {ttype}* %{reg}"
                            self.ctx.set_value(load_reg, ttype)
                            self.emitter << f"\t%{var_name} = alloca {var_type}"
                            self.emitter << f"\tstore {ttype} %{load_reg}, {var_type}* %{var_name}"
                            self.ctx.set_pointer(var_name, var_type, load_reg)
                        elif self.ctx.has_param_in_current_scope(reg):
                            ttype, reg = self.ctx.get_param(reg)
                            load_reg = self.emitter.get_identifier()
                            self.emitter << f"\t%{load_reg} = load {var_type}, {ttype}* %{reg}"
                            self.ctx.set_value(load_reg, ttype)
                            self.emitter << f"\t%{var_name} = alloca {var_type}"
                            self.emitter << f"\tstore {ttype} %{load_reg}, {var_type}* %{var_name}"
                            self.ctx.set_pointer(var_name, var_type, load_reg)
                        elif self.ctx.has_value_in_current_scope(reg):
                            ttype = self.ctx.get_value(reg)
                            load_reg = self.emitter.get_identifier()
                            self.emitter << f"\t%{load_reg} = load {var_type}, {ttype}* %{reg}"
                            self.ctx.set_value(load_reg, ttype)
                            self.emitter << f"\t%{var_name} = alloca {var_type}"
                            self.emitter << f"\tstore {ttype} %{load_reg}, {var_type}* %{var_name}"
                            self.ctx.set_pointer(var_name, var_type, load_reg)
                        elif self.ctx.has_pointer_in_current_scope(reg):
                            ttype, _ = self.ctx.get_pointer(reg)
                            load_reg = self.emitter.get_identifier()
                            self.emitter << f"\t%{load_reg} = load {var_type}, {ttype}* %{reg}"
                            self.ctx.set_value(load_reg, ttype)
                            self.emitter << f"\t%{var_name} = alloca {var_type}"
                            self.emitter << f"\tstore {ttype} %{load_reg}, {var_type}* %{var_name}"
                            self.ctx.set_pointer(var_name, var_type, load_reg)
                        else:
                            self.emitter << f"\t%{var_name} = alloca {var_type}"
                            self.ctx.set_pointer(var_name, var_type, node.expr.identifier)
                            self.emitter << f"\tstore {var_type} %{node.expr.identifier}, {var_type}* %{var_name}"
                    case IntLiteralExprNode() | FloatLiteralExprNode() | BoolLiteralExprNode():
                        self.emitter << f"\t%{var_name} = alloca {var_type}"
                        value = self.cast_type(self.__expression(node.expr), var_type)
                        self.ctx.set_pointer(var_name, var_type, value)
                        self.emitter << f"\tstore {var_type} {value}, {var_type}* %{var_name}"
                    case StrExprNode():
                        str_pointer = self.__expression(node.expr)
                        self.ctx.set_pointer(var_name, "i8*", str_pointer)
                        self.emitter << f"\t%{var_name} = {str_pointer}"
                        
                    case _:
                        value = self.__expression(node.expr)
                        
                        if self.ctx.has_pointer_in_current_scope(value):
                            ttype, _ = self.ctx.get_pointer(value)
                            if ttype == "i1":
                                value = self.cast_bool_int(value, "i64")
                            elif ttype != var_type:
                                value = self.cast_llvm_type(value, var_type)
                        else:
                            ttype = self.ctx.get_value(value)
                            if ttype == "i1":
                                value = self.cast_bool_int(value, "i64")
                            elif ttype != var_type:
                                value = self.cast_llvm_type(value, var_type)            
                            
                        self.emitter << f"\t%{var_name} = alloca {var_type}"
                        self.ctx.set_pointer(var_name, var_type, value)
                        self.emitter << f"\tstore {var_type} %{value}, {var_type}* %{var_name}"
                        
                    
                
                
            
    def __declaration(self, node: DeclarationNode):
        
        match node:
            case FunctionDeclarationNode():
                
                fname = node.func_id.identifier
                ftype = self.convert_type(node.type_.ttype)
                params = node.parameters
                # Function signature
                fsignature = f"declare {ftype} @{fname}("
                # Function params
                for i, (_, ttype) in enumerate(params):
                    param_type = self.convert_type(ttype.ttype)
                    if i == len(params) - 1:
                        fsignature += f"{param_type}"
                    else:
                        fsignature += f"{param_type}, "
                fsignature += f")\n"

                if fname not in self.module_functions:
                    self.emitter << fsignature
                    
                # Enter and exit so that we have the func declaration saved in the context
                self.ctx.enter_function_scope(fname, ftype)
                for i, (id, ttype) in enumerate(params):
                    param_type = self.convert_type(ttype.ttype)
                    param_name = id.identifier
                    self.ctx.set_param(param_name, param_type, None)
                self.ctx.exit_scope()
                
            case VariableDeclarationNode():
                
                var_name = node.var_id.identifier
                var_type = self.convert_type(node.type_.ttype)
                
                self.emitter << f"@{var_name} = external global {var_type}\n"
                
            
    def __expression(self, node: ExprNode):
        
        match node:
            case IntLiteralExprNode():
                return f"{node.value}"
            case FloatLiteralExprNode():
                return f"{node.value}"
            case BoolLiteralExprNode():
                return "1" if node.value else "0"
            case StrExprNode():
                global_string_name = f"@.str{self.module.get_count()}"
                # Add string to the module, which comes before emitter
                string = node.value.strip("\"")
                self.module << f'{global_string_name} = private unnamed_addr constant [{len(string) + 1} x i8] c"{string}\\00"\n'
                # return pointer
                return f'getelementptr inbounds [{len(string) + 1} x i8], [{len(string) + 1} x i8]* {global_string_name}, i64 0, i64 0'
                
            case IdentifierExprNode():
                return node.identifier
            case FuncReturnExprNode():
                arguments = "("
                
                fname = node.func_id.identifier
                # params : {pname : (ttype, reg)}
                params = self.ctx.get_func_params(fname)
                
                
                for  (ptype, _), (i, expr) in zip(params.values(), enumerate(node.arguments)):
                    
                    val1 = self.__expression(expr)
                    
                    if self.ctx.has_pointer_global(val1):
                        val1_type, _ = self.ctx.get_pointer_global(val1)
                        load_reg = self.emitter.get_identifier()
                        self.ctx.set_pointer(load_reg, val1_type, val1)
                        self.emitter << f"\t%{load_reg} = load {val1_type}, {val1_type}* @{val1}"
                        if ptype != val1_type:
                            load_reg = self.cast_llvm_type(load_reg, ptype)
                        val1 = "%" + load_reg
                    elif self.ctx.has_value_global(val1):
                        val1_type = self.ctx.get_value_global(val1)
                        load_reg = self.emitter.get_identifier()
                        self.ctx.set_pointer(load_reg, val1_type, val1)
                        self.emitter << f"\t%{load_reg} = load {val1_type}, {val1_type}* @{val1}"
                        if ptype != val1_type:
                            load_reg = self.cast_llvm_type(load_reg, ptype)
                        val1 = "%" + load_reg
                    elif self.ctx.has_param_in_current_scope(val1):
                        val1_type, reg1 = self.ctx.get_param(val1)
                        load_reg = self.emitter.get_identifier()
                        self.ctx.set_pointer(load_reg, val1_type, reg1)
                        self.emitter << f"\t%{load_reg} = load {val1_type}, {val1_type}* %{reg1}"
                        if ptype != val1_type:
                            load_reg = self.cast_llvm_type(load_reg, ptype)
                        val1 = "%" + load_reg
                    elif self.ctx.has_pointer_in_current_scope(val1):
                        val1_type, _ = self.ctx.get_pointer(val1)
                        load_reg = self.emitter.get_identifier()
                        self.ctx.set_pointer(load_reg, val1_type, val1)
                        self.emitter << f"\t%{load_reg} = load {val1_type}, {val1_type}* %{val1}"
                        if ptype != val1_type:
                            load_reg = self.cast_llvm_type(load_reg, ptype)
                        val1 = "%" + load_reg
                    elif self.ctx.has_value_in_current_scope(val1):
                        val1_type = self.ctx.get_value(val1)
                        if ptype != val1_type:
                            val1 = self.cast_llvm_type(val1, ptype)
                        val1 = "%" + val1
                    elif isinstance(expr, IntLiteralExprNode):
                        val1_type = "i64"
                        if ptype != val1_type:
                            val1 = self.cast_type(val1, ptype)
                    elif isinstance(expr, FloatLiteralExprNode):
                        val1_type = "double"
                        if ptype != val1_type:
                            val1 = self.cast_type(val1, ptype)
                    elif isinstance(expr, StrExprNode):
                        val1_type = "i8*"
                        str_p = self.emitter.get_pointer_name()
                        self.emitter << f"\t%{str_p} = {val1}"
                        self.ctx.set_pointer(str_p, "i8*", val1)
                        val1 = "%" + str_p
                       
                       
                    if i == len(node.arguments) -1: 
                        arguments += f"{ptype} {val1}"
                    else:
                        arguments += f"{ptype} {val1}, "
            
                arguments += ")"
                
                fname = node.func_id.identifier
                ftype = self.ctx.get_func_type(fname)
                
                result_reg = self.emitter.get_identifier()
                self.ctx.set_value(result_reg, ftype)
                
                if ftype == "void":
                    self.emitter << f"\tcall {ftype} @{fname}{arguments}"
                else:
                    self.emitter << f"\t%{result_reg} = call {ftype} @{fname}{arguments}"
                
                return result_reg
        
        
            case BinaryExprNode():
                
                val1 = self.__expression(node.expr1)
                val2 = self.__expression(node.expr2)
                
                
                if self.ctx.has_pointer_global(val1):
                    val1_type, _ = self.ctx.get_pointer_global(val1)
                    load_reg = self.emitter.get_identifier()
                    self.ctx.set_pointer(load_reg, val1_type, val1)
                    self.emitter << f"\t%{load_reg} = load {val1_type}, {val1_type}* @{val1}"
                    val1 = "%" + load_reg
                elif self.ctx.has_value_global(val1):
                    val1_type = self.ctx.get_value_global(val1)
                    load_reg = self.emitter.get_identifier()
                    self.ctx.set_pointer(load_reg, val1_type, val1)
                    self.emitter << f"\t%{load_reg} = load {val1_type}, {val1_type}* @{val1}"
                    val1 = "%" + load_reg
                elif self.ctx.has_param_in_current_scope(val1):
                    val1_type, reg1 = self.ctx.get_param(val1)
                    load_reg = self.emitter.get_identifier()
                    self.ctx.set_pointer(load_reg, val1_type, reg1)
                    self.emitter << f"\t%{load_reg} = load {val1_type}, {val1_type}* %{reg1}"
                    val1 = "%" + load_reg
                elif self.ctx.has_pointer_in_current_scope(val1):
                    val1_type, _ = self.ctx.get_pointer(val1)
                    load_reg = self.emitter.get_identifier()
                    self.ctx.set_pointer(load_reg, val1_type, val1)
                    self.emitter << f"\t%{load_reg} = load {val1_type}, {val1_type}* %{val1}"
                    val1 = "%" + load_reg
                elif self.ctx.has_value_in_current_scope(val1):
                    val1_type = self.ctx.get_value(val1)
                    val1 = "%" + val1
                elif isinstance(node.expr1, IntLiteralExprNode):
                    val1_type = "i64"
                elif isinstance(node.expr1, FloatLiteralExprNode):
                    val1_type = "double"
                
                if self.ctx.has_pointer_global(val2):
                    val2_type, _ = self.ctx.get_pointer_global(val2)
                    load_reg = self.emitter.get_identifier()
                    self.ctx.set_pointer(load_reg, val2_type, val2)
                    self.emitter << f"\t%{load_reg} = load {val2_type}, {val2_type}* @{val2}"
                    val2 = "%" + load_reg
                elif self.ctx.has_value_global(val2):
                    val2_type = self.ctx.get_value_global(val2)
                    load_reg = self.emitter.get_identifier()
                    self.ctx.set_pointer(load_reg, val1_type, val2)
                    self.emitter << f"\t%{load_reg} = load {val2_type}, {val2_type}* @{val2}"
                    val2 = "%" + load_reg
                elif self.ctx.has_param_in_current_scope(val2):
                    val2_type, reg2 = self.ctx.get_param(val2)
                    load_reg = self.emitter.get_identifier()
                    self.ctx.set_pointer(load_reg, val2_type, reg2)
                    self.emitter << f"\t%{load_reg} = load {val2_type}, {val2_type}* %{reg2}"
                    val2 = "%" + load_reg
                elif self.ctx.has_pointer_in_current_scope(val2):
                    val2_type, _ = self.ctx.get_pointer(val2)
                    load_reg = self.emitter.get_identifier()
                    self.ctx.set_pointer(load_reg, val1_type, val2)
                    self.emitter << f"\t%{load_reg} = load {val2_type}, {val2_type}* %{val2}"
                    val2 = "%" + load_reg
                elif self.ctx.has_value_in_current_scope(val2):
                    val2_type = self.ctx.get_value(val2)
                    val2 = "%" + val2
                elif isinstance(node.expr2, IntLiteralExprNode):
                    val2_type = "i64"
                elif isinstance(node.expr2, FloatLiteralExprNode):
                    val2_type = "double"
                
                
                result_reg = None
                
                # TODO: Refactor this (I don't have time :( )
                match node.operator:
                    case BinaryOperator.PLUS:
                        if val1_type == "double" and val2_type == "i64":
                            # Convert integer to float
                            int_to_float_reg = self.emitter.get_identifier()
                            self.ctx.set_value(int_to_float_reg, "double")
                            self.emitter << f"\t%{int_to_float_reg} = sitofp i64 {val2} to double"
                            val2 = int_to_float_reg
                            result_reg = self.emitter.get_identifier()
                            self.ctx.set_value(result_reg, "double")
                            self.emitter << f"\t%{result_reg} = fadd double {val1}, %{val2}"
                        elif val1_type == "i64" and val2_type == "double":
                            # Convert integer to float
                            int_to_float_reg = self.emitter.get_identifier()
                            self.ctx.set_value(int_to_float_reg, "double")
                            self.emitter << f"\t%{int_to_float_reg} = sitofp i64 {val1} to double"
                            val1 = int_to_float_reg
                            result_reg = self.emitter.get_identifier()
                            self.ctx.set_value(result_reg, "double")
                            self.emitter << f"\t%{result_reg} = fadd double %{val1}, {val2}"
                        else:
                            # Both operands are of the same type
                            result_reg = self.emitter.get_identifier()
                            if val1_type == "i64":
                                self.ctx.set_value(result_reg, "i64")
                                self.emitter << f"\t%{result_reg} = add i64 {val1}, {val2}"
                            else:
                                self.ctx.set_value(result_reg, "double")
                                self.emitter << f"\t%{result_reg} = fadd double {val1}, {val2}"
                    case BinaryOperator.DIV:
                        if val1_type == "double" and val2_type == "i64":
                            # Convert integer to float
                            int_to_float_reg = self.emitter.get_identifier()
                            self.ctx.set_value(int_to_float_reg, "double")
                            self.emitter << f"\t%{int_to_float_reg} = sitofp i64 {val2} to double"
                            val2 = int_to_float_reg
                            result_reg = self.emitter.get_identifier()
                            self.ctx.set_value(result_reg, "double")
                            self.emitter << f"\t%{result_reg} = fdiv double {val1}, %{val2}"
                        elif val1_type == "i64" and val2_type == "double":
                            # Convert integer to float
                            int_to_float_reg = self.emitter.get_identifier()
                            self.ctx.set_value(int_to_float_reg, "double")
                            self.emitter << f"\t%{int_to_float_reg} = sitofp i64 {val1} to double"
                            val1 = int_to_float_reg
                            result_reg = self.emitter.get_identifier()
                            self.ctx.set_value(result_reg, "double")
                            self.emitter << f"\t%{result_reg} = fdiv double %{val1}, {val2}"
                        else:
                            # Both operands are of the same type
                            result_reg = self.emitter.get_identifier()
                            if val1_type == "i64":
                                # Convert val1 to float
                                int_to_float_reg = self.emitter.get_identifier()
                                self.ctx.set_value(int_to_float_reg, "double")
                                self.emitter << f"\t%{int_to_float_reg} = sitofp i64 {val1} to double"
                                val1 = "%" + int_to_float_reg
                                # Convert val2 to float
                                int_to_float_reg = self.emitter.get_identifier()
                                self.ctx.set_value(int_to_float_reg, "double")
                                self.emitter << f"\t%{int_to_float_reg} = sitofp i64 {val2} to double"
                                val2 = "%" + int_to_float_reg
                            self.ctx.set_value(result_reg, "double")
                            self.emitter << f"\t%{result_reg} = fdiv double {val1}, {val2}"
                    case BinaryOperator.MUL:
                        if val1_type == "double" and val2_type == "i64":
                            # Convert integer to float
                            int_to_float_reg = self.emitter.get_identifier()
                            self.ctx.set_value(int_to_float_reg, "double")
                            self.emitter << f"\t%{int_to_float_reg} = sitofp i64 {val2} to double"
                            val2 = int_to_float_reg
                            result_reg = self.emitter.get_identifier()
                            self.ctx.set_value(result_reg, "double")
                            self.emitter << f"\t%{result_reg} = fmul double {val1}, %{val2}"
                        elif val1_type == "i64" and val2_type == "double":
                            # Convert integer to float
                            int_to_float_reg = self.emitter.get_identifier()
                            self.ctx.set_value(int_to_float_reg, "double")
                            self.emitter << f"\t%{int_to_float_reg} = sitofp i64 {val1} to double"
                            val1 = int_to_float_reg
                            result_reg = self.emitter.get_identifier()
                            self.ctx.set_value(result_reg, "double")
                            self.emitter << f"\t%{result_reg} = fmul double %{val1}, {val2}"
                        else:
                            # Both operands are of the same type
                            result_reg = self.emitter.get_identifier()
                            if val1_type == "i64":
                                self.ctx.set_value(result_reg, "i64")
                                self.emitter << f"\t%{result_reg} = mul i64 {val1}, {val2}"
                            else:
                                self.ctx.set_value(result_reg, "double")
                                self.emitter << f"\t%{result_reg} = fmul double {val1}, {val2}"
                    case BinaryOperator.MINUS:
                        if val1_type == "double" and val2_type == "i64":
                            # Convert integer to float
                            int_to_float_reg = self.emitter.get_identifier()
                            self.ctx.set_value(int_to_float_reg, "double")
                            self.emitter << f"\t%{int_to_float_reg} = sitofp i64 {val2} to double"
                            val2 = int_to_float_reg
                            result_reg = self.emitter.get_identifier()
                            self.ctx.set_value(result_reg, "double")
                            self.emitter << f"\t%{result_reg} = fsub double {val1}, %{val2}"
                        elif val1_type == "i64" and val2_type == "double":
                            # Convert integer to float
                            int_to_float_reg = self.emitter.get_identifier()
                            self.ctx.set_value(int_to_float_reg, "double")
                            self.emitter << f"\t%{int_to_float_reg} = sitofp i64 {val1} to double"
                            val1 = int_to_float_reg
                            result_reg = self.emitter.get_identifier()
                            self.ctx.set_value(result_reg, "double")
                            self.emitter << f"\t%{result_reg} = fsub double %{val1}, {val2}"
                        else:
                            # Both operands are of the same type
                            result_reg = self.emitter.get_identifier()
                            if val1_type == "i64":
                                self.ctx.set_value(result_reg, "i64")
                                self.emitter << f"\t%{result_reg} = sub i64 {val1}, {val2}"
                            else:
                                self.ctx.set_value(result_reg, "double")
                                self.emitter << f"\t%{result_reg} = fsub double {val1}, {val2}"
                    case BinaryOperator.MOD:
                        result_reg = self.emitter.get_identifier()
                        self.ctx.set_value(result_reg, "i64")
                        self.emitter << f"\t%{result_reg} = srem i64 {val1}, {val2}"
                    case BinaryOperator.EQ:
                        if val1_type == "double" and val2_type == "i64":
                            # Convert integer to float
                            int_to_float_reg = self.emitter.get_identifier()
                            self.ctx.set_value(int_to_float_reg, "double")
                            self.emitter << f"\t%{int_to_float_reg} = sitofp i64 {val2} to double"
                            val2 = int_to_float_reg
                            result_reg = self.emitter.get_identifier()
                            self.ctx.set_value(result_reg, "i1")
                            self.emitter << f"\t%{result_reg} = fcmp oeq double {val1}, %{val2}"
                        elif val1_type == "i64" and val2_type == "double":
                            # Convert integer to float
                            int_to_float_reg = self.emitter.get_identifier()
                            self.ctx.set_value(int_to_float_reg, "double")
                            self.emitter << f"\t%{int_to_float_reg} = sitofp i64 {val1} to double"
                            val1 = int_to_float_reg
                            result_reg = self.emitter.get_identifier()
                            self.ctx.set_value(result_reg, "i1")
                            self.emitter << f"\t%{result_reg} = fcmp oeq double %{val1}, {val2}"
                        else:
                            # Both operands are of the same type
                            result_reg = self.emitter.get_identifier()
                            if val1_type == "i64":
                                self.ctx.set_value(result_reg, "i1")
                                self.emitter << f"\t%{result_reg} = icmp eq i64 {val1}, {val2}"
                            else:
                                self.ctx.set_value(result_reg, "i1")
                                self.emitter << f"\t%{result_reg} = fcmp oeq double {val1}, {val2}"
                    case BinaryOperator.NEQ:
                        if val1_type == "double" and val2_type == "i64":
                            # Convert integer to float
                            int_to_float_reg = self.emitter.get_identifier()
                            self.ctx.set_value(int_to_float_reg, "double")
                            self.emitter << f"\t%{int_to_float_reg} = sitofp i64 {val2} to double"
                            val2 = int_to_float_reg
                            result_reg = self.emitter.get_identifier()
                            self.ctx.set_value(result_reg, "i1")
                            self.emitter << f"\t%{result_reg} = fcmp one double {val1}, %{val2}"
                        elif val1_type == "i64" and val2_type == "double":
                            # Convert integer to float
                            int_to_float_reg = self.emitter.get_identifier()
                            self.ctx.set_value(int_to_float_reg, "double")
                            self.emitter << f"\t%{int_to_float_reg} = sitofp i64 {val1} to double"
                            val1 = int_to_float_reg
                            result_reg = self.emitter.get_identifier()
                            self.ctx.set_value(result_reg, "i1")
                            self.emitter << f"\t%{result_reg} = fcmp one double %{val1}, {val2}"
                        else:
                            # Both operands are of the same type
                            result_reg = self.emitter.get_identifier()
                            if val1_type == "i64":
                                self.ctx.set_value(result_reg, "i1")
                                self.emitter << f"\t%{result_reg} = icmp ne i64 {val1}, {val2}"
                            else:
                                self.ctx.set_value(result_reg, "i1")
                                self.emitter << f"\t%{result_reg} = fcmp one double {val1}, {val2}"
                    case BinaryOperator.GE:
                        if val1_type == "double" and val2_type == "i64":
                            # Convert integer to float
                            int_to_float_reg = self.emitter.get_identifier()
                            self.ctx.set_value(int_to_float_reg, "double")
                            self.emitter << f"\t%{int_to_float_reg} = sitofp i64 {val2} to double"
                            val2 = int_to_float_reg
                            result_reg = self.emitter.get_identifier()
                            self.ctx.set_value(result_reg, "i1")
                            self.emitter << f"\t%{result_reg} = fcmp oge double {val1}, %{val2}"
                        elif val1_type == "i64" and val2_type == "double":
                            # Convert integer to float
                            int_to_float_reg = self.emitter.get_identifier()
                            self.ctx.set_value(int_to_float_reg, "double")
                            self.emitter << f"\t%{int_to_float_reg} = sitofp i64 {val1} to double"
                            val1 = int_to_float_reg
                            result_reg = self.emitter.get_identifier()
                            self.ctx.set_value(result_reg, "i1")
                            self.emitter << f"\t%{result_reg} = fcmp oge double %{val1}, {val2}"
                        else:
                            # Both operands are of the same type
                            result_reg = self.emitter.get_identifier()
                            if val1_type == "i64":
                                self.ctx.set_value(result_reg, "i1")
                                self.emitter << f"\t%{result_reg} = icmp sge i64 {val1}, {val2}"
                            else:
                                self.ctx.set_value(result_reg, "i1")
                                self.emitter << f"\t%{result_reg} = fcmp oge double {val1}, {val2}"
                    case BinaryOperator.GT:
                        if val1_type == "double" and val2_type == "i64":
                            # Convert integer to float
                            int_to_float_reg = self.emitter.get_identifier()
                            self.ctx.set_value(int_to_float_reg, "double")
                            self.emitter << f"\t%{int_to_float_reg} = sitofp i64 {val2} to double"
                            val2 = int_to_float_reg
                            result_reg = self.emitter.get_identifier()
                            self.ctx.set_value(result_reg, "i1")
                            self.emitter << f"\t%{result_reg} = fcmp ogt double {val1}, %{val2}"
                        elif val1_type == "i64" and val2_type == "double":
                            # Convert integer to float
                            int_to_float_reg = self.emitter.get_identifier()
                            self.ctx.set_value(int_to_float_reg, "double")
                            self.emitter << f"\t%{int_to_float_reg} = sitofp i64 {val1} to double"
                            val1 = int_to_float_reg
                            result_reg = self.emitter.get_identifier()
                            self.ctx.set_value(result_reg, "i1")
                            self.emitter << f"\t%{result_reg} = fcmp ogt double %{val1}, {val2}"
                        else:
                            # Both operands are of the same type
                            result_reg = self.emitter.get_identifier()
                            if val1_type == "i64":
                                self.ctx.set_value(result_reg, "i1")
                                self.emitter << f"\t%{result_reg} = icmp sgt i64 {val1}, {val2}"
                            else:
                                self.ctx.set_value(result_reg, "i1")
                                self.emitter << f"\t%{result_reg} = fcmp ogt double {val1}, {val2}"
                    case BinaryOperator.LE:
                        if val1_type == "double" and val2_type == "i64":
                            # Convert integer to float
                            int_to_float_reg = self.emitter.get_identifier()
                            self.ctx.set_value(int_to_float_reg, "double")
                            self.emitter << f"\t%{int_to_float_reg} = sitofp i64 {val2} to double"
                            val2 = int_to_float_reg
                            result_reg = self.emitter.get_identifier()
                            self.ctx.set_value(result_reg, "i1")
                            self.emitter << f"\t%{result_reg} = fcmp ole double {val1}, %{val2}"
                        elif val1_type == "i64" and val2_type == "double":
                            # Convert integer to float
                            int_to_float_reg = self.emitter.get_identifier()
                            self.ctx.set_value(int_to_float_reg, "double")
                            self.emitter << f"\t%{int_to_float_reg} = sitofp i64 {val1} to double"
                            val1 = int_to_float_reg
                            result_reg = self.emitter.get_identifier()
                            self.ctx.set_value(result_reg, "i1")
                            self.emitter << f"\t%{result_reg} = fcmp ole double %{val1}, {val2}"
                        else:
                            # Both operands are of the same type
                            result_reg = self.emitter.get_identifier()
                            if val1_type == "i64":
                                self.ctx.set_value(result_reg, "i1")
                                self.emitter << f"\t%{result_reg} = icmp sle i64 {val1}, {val2}"
                            else:
                                self.ctx.set_value(result_reg, "i1")
                                self.emitter << f"\t%{result_reg} = fcmp ole double {val1}, {val2}"
                    case BinaryOperator.LT:
                        if val1_type == "double" and val2_type == "i64":
                            # Convert integer to float
                            int_to_float_reg = self.emitter.get_identifier()
                            self.ctx.set_value(int_to_float_reg, "double")
                            self.emitter << f"\t%{int_to_float_reg} = sitofp i64 {val2} to double"
                            val2 = int_to_float_reg
                            result_reg = self.emitter.get_identifier()
                            self.ctx.set_value(result_reg, "i1")
                            self.emitter << f"\t%{result_reg} = fcmp olt double {val1}, %{val2}"
                        elif val1_type == "i64" and val2_type == "double":
                            # Convert integer to float
                            int_to_float_reg = self.emitter.get_identifier()
                            self.ctx.set_value(int_to_float_reg, "double")
                            self.emitter << f"\t%{int_to_float_reg} = sitofp i64 {val1} to double"
                            val1 = int_to_float_reg
                            result_reg = self.emitter.get_identifier()
                            self.ctx.set_value(result_reg, "i1")
                            self.emitter << f"\t%{result_reg} = fcmp olt double %{val1}, {val2}"
                        else:
                            # Both operands are of the same type
                            result_reg = self.emitter.get_identifier()
                            if val1_type == "i64":
                                self.ctx.set_value(result_reg, "i1")
                                self.emitter << f"\t%{result_reg} = icmp slt i64 {val1}, {val2}"
                            else:
                                self.ctx.set_value(result_reg, "i1")
                                self.emitter << f"\t%{result_reg} = fcmp olt double {val1}, {val2}"
                    case BinaryOperator.AND:
                        result_reg = self.emitter.get_identifier()
                        self.ctx.set_value(result_reg, "i64")
                        self.emitter << f"\t%{result_reg} = and i64 {val1}, {val2}"
                    case BinaryOperator.OR:
                        result_reg = self.emitter.get_identifier()
                        self.ctx.set_value(result_reg, "i64")
                        self.emitter << f"\t%{result_reg} = or i64 {val1}, {val2}"
                    
                assert result_reg is not None
                return result_reg
                    
            case UnaryExprNode():
                
                val1 = self.__expression(node.expr)
                
                if self.ctx.has_pointer_global(val1):
                    val1_type, _ = self.ctx.get_pointer_global(val1)
                    load_reg = self.emitter.get_identifier()
                    self.ctx.set_pointer(load_reg, val1_type, val1)
                    self.emitter << f"\t%{load_reg} = load {val1_type}, {val1_type}* @{val1}"
                    val1 = "%" + load_reg
                elif self.ctx.has_value_global(val1):
                    val1_type = self.ctx.get_value_global(val1)
                    load_reg = self.emitter.get_identifier()
                    self.ctx.set_pointer(load_reg, val1_type, val1)
                    self.emitter << f"\t%{load_reg} = load {val1_type}, {val1_type}* @{val1}"
                    val1 = "%" + load_reg
                elif self.ctx.has_param_in_current_scope(val1):
                    val1_type, reg1 = self.ctx.get_param(val1)
                    load_reg = self.emitter.get_identifier()
                    self.ctx.set_pointer(load_reg, val1_type, reg1)
                    self.emitter << f"\t%{load_reg} = load {val1_type}, {val1_type}* %{reg1}"
                    val1 = "%" + load_reg
                elif self.ctx.has_pointer_in_current_scope(val1):
                    val1_type, _ = self.ctx.get_pointer(val1)
                    load_reg = self.emitter.get_identifier()
                    self.ctx.set_pointer(load_reg, val1_type, val1)
                    self.emitter << f"\t%{load_reg} = load {val1_type}, {val1_type}* %{val1}"
                    val1 = "%" + load_reg
                elif self.ctx.has_value_in_current_scope(val1):
                    val1_type = self.ctx.get_value(val1)
                    val1 = "%" + val1
                else:
                    val1_type = "i64"
                
                result_reg = None
                
                match node.operator:
                    case UnaryOperator.NOT:
                        result_reg = self.emitter.get_identifier()
                        self.ctx.set_value(result_reg, "i64")
                        self.emitter << f"\t%{result_reg} = xor i64 {val1}, -1"
                        
                assert result_reg is not None
                return result_reg
                
            case IndexAccessExprNode():
                
                array = self.__expression(node.array)
                
                val1 = self.__expression(node.index)
                
                if self.ctx.has_pointer_global(val1):
                    val1_type, _ = self.ctx.get_pointer_global(val1)
                    load_reg = self.emitter.get_identifier()
                    self.ctx.set_pointer(load_reg, val1_type, val1)
                    self.emitter << f"\t%{load_reg} = load {val1_type}, {val1_type}* @{val1}"
                    val1 = "%" + load_reg
                elif self.ctx.has_value_global(val1):
                    val1_type = self.ctx.get_value_global(val1)
                    load_reg = self.emitter.get_identifier()
                    self.ctx.set_pointer(load_reg, val1_type, val1)
                    self.emitter << f"\t%{load_reg} = load {val1_type}, {val1_type}* @{val1}"
                    val1 = "%" + load_reg
                elif self.ctx.has_param_in_current_scope(val1):
                    val1_type, reg1 = self.ctx.get_param(val1)
                    load_reg = self.emitter.get_identifier()
                    self.ctx.set_pointer(load_reg, val1_type, reg1)
                    self.emitter << f"\t%{load_reg} = load {val1_type}, {val1_type}* %{reg1}"
                    val1 = "%" + load_reg
                elif self.ctx.has_pointer_in_current_scope(val1):
                    val1_type, _ = self.ctx.get_pointer(val1)
                    load_reg = self.emitter.get_identifier()
                    self.ctx.set_pointer(load_reg, val1_type, val1)
                    self.emitter << f"\t%{load_reg} = load {val1_type}, {val1_type}* %{val1}"
                    val1 = "%" + load_reg
                elif self.ctx.has_value_in_current_scope(val1):
                    val1_type = self.ctx.get_value(val1)
                    val1 = "%" + val1
                else:
                    val1_type = "i64"
                
                if self.ctx.has_pointer_global(array):
                    array_type, _ = self.ctx.get_pointer_global(array)
                elif self.ctx.has_value_global(array):
                    array_type = self.ctx.get_value_global(array)
                elif self.ctx.has_param_in_current_scope(array):
                    array_type, reg1 = self.ctx.get_param(array)
                elif self.ctx.has_pointer_in_current_scope(array):
                    array_type, _ = self.ctx.get_pointer(array)
                elif self.ctx.has_value_in_current_scope(array):
                    array_type = self.ctx.get_value(array)
                
                arr_p = self.emitter.get_pointer_name()
                value = self.emitter.get_identifier()
                
                
                if array_type == "i64*":
                    self.emitter << f"\t%{arr_p} = getelementptr inbounds i64, i64* %{array}, i64 {val1}"
                    self.emitter << f"\t%{value} = load i64, i64* %{arr_p}"
                    self.ctx.set_value(value, "i64")
                elif array_type == "double*":
                    self.emitter << f"\t%{arr_p} = getelementptr inbounds double, double* %{array}, i64 {val1}"
                    self.emitter << f"\t%{value} = load double, double* %{arr_p}"
                    self.ctx.set_value(value, "double")
                    
                    
                return value
            
