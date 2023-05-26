(* Sum of squares program in sPLash *)


print_int: Void (n: Int);
print_string: Void (string: String);

(* Function to calculate the square of a number *)
square: Int (n: Int) {
  return n * n;
}

(* Function to calculate the sum of squares of first n natural numbers *)
sum_of_squares: Int (n: Int where n >= 0, current_sum: Int) {
  result: Int = 0;
  if n == 0 {
    result = current_sum;
  } else {
    result =sum_of_squares(n - 1, current_sum + square(n));
  }
  return result;
}

main: Int () {
  num: Int = 5;
  result: Int = sum_of_squares(num, 0);
  print_string("The sum of the squares of the first 5 natural numbers is");
  print_int(result);
  return 0;
}
