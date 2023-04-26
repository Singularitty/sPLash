(* Factorial in sPLash *)

printf: Void (format : String, arg: String);

toString: String (i: Int);

factorial: Int (n: Int where n >= 0) {
  if n == 0 {
    return 1;
  }
  return n * factorial(n - 1);
}

main: Int () {
  num: Int = 5;
  fact: Int = factorial(num);
  result: String = toString(fact);
  printf("Factorial of is", result);
  return 0;
}
