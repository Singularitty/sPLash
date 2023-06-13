(* Maximum element program in sPLash *)

print_string: Void (str: String);
print_int: Void (n: Int);

create_array_int: [Int] (size: Int where size > 0);
write_to_array_int: Void (array: [Int], index: Int where index >= 0, value: Int);

find_maximum: Int (array: [Int], size: Int where size > 0) {
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
  
  array_size:Int where array_size == 5 = 5;
  numbers:[Int] = create_array_int(array_size);
  value: Int where value > 0 = 3;
  i: Int where i + 1 > 0 = 0;
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
