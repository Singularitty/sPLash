(* Fibonacci sequence in sPLash *)

alocate_array: [Int] (size: Int);
write_to_array: Void (array: [Int], index: Int, value: Int);
print_int: Void (value: Int);
print: Void (content: String);


(* Function to calculate the nth Fibonacci number *)
fibonacci: Int (n: Int where n >= 0) {
  if n == 0 {
    return 0;
  } if n == 1 {
    return 1;
  }
  return fibonacci(n - 1) + fibonacci(n - 2);
}

(* Function to fill an array with Fibonacci numbers *)
fill_fibonacci: Void (arr: [Int], index: Int, n: Int) {
  if index < n {
    write_to_array(arr, index, fibonacci(index));
    fill_fibonacci(arr, index + 1, n);
  }
}

(* Function to print an array of integers *)
print_array: Void (arr: [Int], index: Int, n: Int) {
  if index < n {
    print_int(arr[index]);
    print(" ");
    print_array(arr, index + 1, n);
  } else {
    print("\n");
  }
}

main: Int () {
  num_terms: Int = 10;
  fib_sequence: [Int] = alocate_array(num_terms);

  fill_fibonacci(fib_sequence, 0, num_terms);
  print("Fibonacci sequence:");
  print_array(fib_sequence, 0, num_terms);

  return 0;
}
