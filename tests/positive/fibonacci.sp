(* Fibonacci sequence in sPLash *)

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
    print(arr[index], " ");
    print_array(arr, index + 1, n);
  } else {
    print("\n");
  }
}

main: Int () {
  num_terms: Int = 10;
  fib_sequence: [Int] = alocate_array(Int, num_terms);

  fill_fibonacci(fib_sequence, 0, num_terms);
  print("Fibonacci sequence with ", num_terms, " terms: ");
  print_array(fib_sequence, 0, num_terms);

  return 0;
}
