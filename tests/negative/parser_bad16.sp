(* Invalid function call syntax *)

multiply: Int (a: Int, b: Int) {
  return a * b;
}

main: Int () {
  a: Int = 5;
  b: Int = 10;
  result: Int = multiply a, b;
  print("Product: ", result);
  return 0;
}
