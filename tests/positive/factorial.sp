(* Factorial in sPLash *)

print_string: Void (str: String);
print_int: Void (n : Int);

(* Function to calculate the factorial of a number *)
factorial: Int (n: Int where n >= 0) {
  result: Int where result >= 1 = 1;
  i: Int = 1;
  while i <= n {
    result = result * i;
    i = i + 1;
  }
  return result;
}

main: Int () {
  num: Int where num >= 0 = 5;
  fact: Int = factorial(num);
  print_string("Factorial of 5 is:");
  print_int(fact);
  return 0;
}