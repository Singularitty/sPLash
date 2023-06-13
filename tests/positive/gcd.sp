(* GCD and LCM in sPLash *)

print_string: Void (str: String);
print_int: Void (n: Int);
print_double: Void (n: Double);

(* Function to calculate the GCD of two numbers *)
gcd: Int (a: Int where a > 0, b: Int where b > 0) {
  result: Int = 0;
  if b == 0 {
    result = a;
  } else {
    result = gcd(b, a % b);
  }
  return result;
}

(* Function to calculate the LCM of two numbers *)
lcm: Double (a: Int where a > 0, b: Int where b > 0) {
    return (a * b) / gcd(a, b);

}

main: Int () {
  num1: Int where num1 >= 15 = 15;
  num2: Int where num2 >= 25 = 25;

  result_gcd: Int = gcd(num1, num2);
  result_lcm: Double = lcm(num1, num2);

  print_string("GCD and LCM of 15 and 25");

  print_string("GCD:");
  print_int(result_gcd);
  print_string("LCM:");
  print_double(result_lcm);

  return 0;
}