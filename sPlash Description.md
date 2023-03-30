# sPLash

sPLash is new a programming language, designed to teach programming. It's goal is to be simple, and modular.

## Language Description

- Comments in simPLe start with (* and end with *).
- sPLash is whitespace insensitive.
- A program is made of several declarations or definitions that precede the main body.
- A declaration includes the name of the function, its arguments and types and refinements, as well as the return type.

```
sample_normal:Double (mean:Double, stddev:Double where stddev != 0);
```

   - The refinement (where p(a)) is optional. The refinement can refer to the variable, and constrains possible values allowed as parameters.
   - The return type can also be refined:

```
abs:Int where abs > 0 (val:Int);
```
   - A definition is similar, but includes a block of code that defines the function, or a definition of the value.

```
max:Int (a:Int, b:Int) {
  if a > b {
    return a;
  }
  return b;
}
pi:Int = 3;
```
- Statements, declarations and definitions with values end with semicolon. Definitions of functions do not need semicolon, as the curly braces delimit the function.
     -    Blocks are enclosed with { and } and are comprised of 0 or more statements.
     - Expressions are statements: 1; or f(3);
     - If statements have a condition, a then block and optionally an else block, separated by the else keyword.
     - While statements are similar to if statements, without the else block.
     - Local variables statements are defined similarly to global ones (with a mandatory starting value)
     - Variable assignments can be statements.
- Expressions represent values. They can be:

    -  Binary operators, with a C-like precedence and parenthesis to force other precedences: `&&`, `||`, `==`, `!=`, `>=`, `>`, `<=`, `<`, `+`, `-`, `*`, `/`, `%` em que a divisão tem sempre a semântica da divisão de floats.

    -  The not unary operator (!true)

    -  Boolean literals (`true`, `false`)

    - Integer literals (`1`, `01`, `12312341341`, `1_000_000`) where underscores can be present in any position.

    - Float literals (`1.1`, `.5`, `1233123131231321`)

    - String literals (`""`, `"a"`, `"aa"`, `"qwertyuiop"`, `"qwerty\tuiop"`)

    - Variables, which start with a letter or understore and are followed by any number of letters, underscores or numbers.

    - index access, (`a[0]` or `get_array()[i+1]`)
