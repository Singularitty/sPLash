(* Missing bracket on function definiton *)

factorial: Int (n: Int where n >= 0) {
  if n == 0 {
    return 1;
  } else {
    return n * factorial(n - 1);

main: Int () {
  num: Int = 5;
  fact: Int = factorial(num);
  print("Factorial: ", fact);
  return 0;
}
