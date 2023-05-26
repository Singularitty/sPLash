(* Maximum element program in sPLash *)

print_string: Void (str: String);
print_int: Void (n: Int);

create_array_int: [Int] (size: Int);
write_to_array_int: Void (array: [Int], index: Int, value: Int);

find_maximum: Int (array: [Int], size: Int) {
  max: Int = array[0];
  i: Int = 1;

  while i < size {
    if array[i] > max {
      max = array[i];
    }
    i = i + 1;
  }

  return max;
}

main: Int () {
  
  array_size:Int = 5;
  numbers:[Int] = create_array_int(array_size);
  value: Int = 3;
  i: Int = 0;
  while value < 5 {
    write_to_array_int(numbers, i, value);
    i = i + 1;
    value = value + 2;
  }

  max_number: Int = find_maximum(numbers, array_size);
  print_string("The maximum number in the array is: ");
  print_int(max_number);
  return 0;
}
