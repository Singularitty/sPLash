(* Fibonacci again but without arrays and segfaults *)

print_string: Void (content: String);
print_int: Void (value: Int);

(* Function to calculate the nth Fibonacci number *)
fibonacci: Int (n: Int where n >= 0) {
  a: Int = 0;
  b: Int = 1;
  temp: Int = 0;
  i: Int = 0;
  
  while i < n {
    print_int(a);
    temp = a + b;
    a = b;
    b = temp;
    i = i + 1;
  }
  return a;
}

main: Int () {
  num_terms: Int where num_terms > 0 = 25;
  print_string("Fibonacci sequence:");
  fibonacci(num_terms);
  return 0;
}
