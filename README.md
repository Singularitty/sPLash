# sPLash Compiler

## Author: Luís Ferreirinha Nº51127

This repo contains a compiler for the sPLash programming language. This compiler was designed as a project for the course Técnicas de Compilação lectured in Faculdade de Ciências da Universidade de Lisboa during the 2nd Semester of 2022/23.

### Structure

This repository has a the following structure:  
```
├── README.md  
├── requirements.txt  			
├── setup.sh  					
├── splash  
├── src  
│   ├── compiler.py  
│   ├── parser  
│   │   ├── ast_nodes.py  
│   │   ├── ast_transformer.py  
│   │   └── sPLash.lark  
│   ├── typechecker  
│   │   ├── typechecker.py  
│   │   ├── liquidtypechecker.py  
│   │   └── types.py  
│   └── codegen  
│       └── codegen.py  
└── tests  
    ├── negative  
    └── positive  
```
  
Description of each item:  
- requirements.txt
- setup.sh: Bash script to install all dependencies
- splash: script to run the compiler
- src: Contains the source code for the compiler
	- compiler.py: Entry point for the compiler
	- parser: Contains the source code for the parser and the grammar file
		- ast_nodes.py:  Absract Syntax Tree Definition and JSON Representation
		- ast_transformer.py: Absract Syntax Tree Definition and Representation  
		- sPLash.lark: sPLash lark grammar file 
	- typechecker: Contains the source code for the typechecker and type definition classes
		- typechecker: Type Checker implementation
		- liquidtypechecker: Checks refinements of liquid types
		- types: Type Classes defined
	- codegen: Contains the source code for the LLVM IR code generator
- tests: Tests for the compiler
	- negative: Contains 20 programs with incorrect syntax and 20 programs with incorrect semantics. They are denoted by a prefix "parser" or "typechecker" depending on which error they contain.
	- positive: Interesting programs with correct syntax and semantics


### How to run

To run the compiler you first have to install all the dependencies.
In order to do this you can run the following setup script as root.

```bash
./setup.sh
```

After you've ran the setup script, you can use the compiler with the splash script.
To parse a file you can simply give the path of a sPLash source code file to the compiler:

```bash
./splash file_path
```
If the sPLash file had correct syntax the compiler will emit a file_path.ll file, which contains the LLVM IR code generated for that source file, but if it contains syntax errors, the parser will throw an error indicating where it failed to parse the file.
  
If you have a file with correct syntax, you can view a JSON representation of the Abstract Syntax Tree by including the flag --tree, before the file:

```bash
./splash --tree file_path
```

This will print a JSON representation of the AST generated for that program.

Additionally if the program contains incorrect semantics it will not type check, and the errors preventing it from type checking will be printing out.

After you've compiled the sPLash source code to LLVM, you can user the interpreter to execute the program.

```bash
lli file.ll
```

Or you can generate assembly and compile it with your favorite compiler

```bash
llc -relocation-model=pic tests/positive/file.ll
gcc tests/positive/file.s -o file
./file
```

Notes:  
Operations in arrays have some problems unfortunately.
