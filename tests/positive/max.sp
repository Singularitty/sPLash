(* Maximum number program in sPLash *)

print_int: Void (n: Int);
print_string: Void (string: String);

find_maximum: Int (a: Int, b: Int, c: Int) {
  max: Int = a;

  if b > max {
    max = b;
  }

  if c > max {
    max = c;
  }

  return max;
}

main: Int () {
  num1: Int = 5;
  num2: Int = -9;
  num3: Int = 3;

  max_number: Int = find_maximum(num1, num2, num3);
  print_string("The maximum number is: ");
  print_int(max_number);
  return 0;
}
