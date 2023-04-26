(* GCD and LCM in sPLash *)

get_input: Void ();

print: Void (str: String);

(* Function to calculate the GCD of two numbers *)
gcd: Int (a: Int where a > 0, b: Int where b > 0) {
  if b == 0 {
    return a;
  }
  return gcd(b, a % b);
}

(* Function to calculate the LCM of two numbers *)
lcm: Int (a: Int where a > 0, b: Int where b > 0) {
  return a * b / gcd(a, b);
}

(* Function to read an integer value from the user *)
read_int: Int (prompt: String) {
  print(prompt);
  value: Int = get_input();
  return value;
}

main: Int () {
  num1: Int = read_int("Enter the first number: ");
  num2: Int = read_int("Enter the second number: ");

  result_gcd: Int = gcd(num1, num2);
  result_lcm: Int = lcm(num1, num2);

  return 0;
}
