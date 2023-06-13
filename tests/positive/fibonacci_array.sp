(* Fibonacci sequence in sPLash *)

create_array_int: [Int] (size: Int);
write_to_array_int: Void (array: [Int], index: Int, value: Int);
print_int: Void (value: Int);
print_string: Void (content: String);
freeInt: Void (arr: [Int]);

(* Function to calculate the nth Fibonacci number *)
fibonacci: Int (n: Int where n >= 0) {
  a: Int = 0;
  b: Int = 1;
  i: Int = 0;
  temp: Int = a;
  while i < n {
    temp = a;
    a = b;
    b = temp + b;
    i = i + 1;
  }
  return a;
}

(* Function to fill an array with Fibonacci numbers *)
fill_fibonacci: Void (arr: [Int], n: Int where n >= 1) {
  i: Int = 0;
  while i < n {
    write_to_array_int(arr, i, fibonacci(i));
    i = i + 1;
  }
}

(* Function to print an array of integers *)
print_array: Void (arr: [Int], n: Int where n >= 0) {
  i: Int = 0;
  while i < n {
    print_int(arr[i]);
    i = i + 1;
  }
}

main: Int () {
  num_terms: Int where num_terms > 0 = 11;
  fib_sequence: [Int] = create_array_int(num_terms);

  fill_fibonacci(fib_sequence, num_terms);
  print_string("Fibonacci sequence until 10th element:");
  print_array(fib_sequence, num_terms);

  (* Free doesn't fix the segfault, don't know how to fix it :( *)
  freeInt(fib_sequence);

  return 0;
}
