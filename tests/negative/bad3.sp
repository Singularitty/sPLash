(* Missing parentheses on function value return *)

f : Int (b : Int) {
    return b + 1;
}

main: Int () {
  a: Int = 5;
  b: Int = 3;
  result: Int = a + b;
  f(result;
  return 0;
}
