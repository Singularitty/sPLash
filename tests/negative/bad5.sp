(* Missing semicolon on local variable definition *)

main: Int () {
  a: Int = 5
  b: Int = 10;
  sum: Int = a + b;
  return 0;
}
