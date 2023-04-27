(* Missing : in type of function definition *)

square Int (n: Int) {
  return n * n;
}

main: Int () {
  a: Int = 5;
  result: Int = square(a);
  print("Square: ", result);
  return 0;
}
