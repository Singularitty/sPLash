(* Sum of squares program in sPLash *)


printf: Void (format: String, arg1: Int, arg2: Int);

(* Function to calculate the square of a number *)
square: Int (n: Int) {
  return n * n;
}

(* Function to calculate the sum of squares of first n natural numbers *)
sum_of_squares: Int (n: Int where n >= 0, current_sum: Int) {
  if n == 0 {
    return current_sum;
  }
  return sum_of_squares(n - 1, current_sum + square(n));
}

main: Int () {
  num: Int = 5;
  result: Int = sum_of_squares(num, 0);
  printf("The sum of squares of first {n} natural numbers is: {n}", num, result);
  return 0;
}
