(* Calculate the square root with the Babylonian method *)

print_double: Void (n: Double);
print_string: Void (string: String);


(* Function to calculate the absolute value of a number *)
abs: Double (x: Double) {
  result: Double = x;
  if x < 0 {
    result = result * -1;
  }
  return result;
}

(* Function to calculate the square root of a number using the Babylonian method *)
sqrt: Double (n: Double) {
  guess: Double = n / 2.0;
  epsilon: Double = 0.001;
  while abs(guess * guess - n) >= epsilon {
    guess = (guess + n / guess) / 2.0;
  }
  return guess;
}

main: Int () {
  number: Double = 25.0;
  sqrt_number: Double = sqrt(number);
  print_string("The square root of 25 is:");
  print_double(sqrt_number);
  return 0;
}
