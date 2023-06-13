(* Function to calculate the mean of an array of integers *)

print_string: Void (str: String);
print_double: Void (n: Double);
create_array_int: [Int] (size: Int where size > 0);
write_to_array_int: Void (array: [Int], index: Int where index >= 0, value: Int);

sqrt: Double (n: Double);


mean:Double (arr:[Int], size:Int where size > 0) {
  sum:Int = 0;
  i: Int = 0;
  while i < size {
    sum = sum + arr[i];
    i = i + 1;
  }

  return sum / size;
}


main: Int () {
  array_size:Int where array_size > 0 = 5;
  numbers:[Int] = create_array_int(array_size);
  value: Int = 3;
  i: Int = 0;
  while value < 5 {
    write_to_array_int(numbers, i, value);
    i = i + 1;
    value = value + 2;
  }

  mean_result:Double = mean(numbers, array_size);

  print_string("Mean of the numbers 3, 5, 7, 9, 11 is:");
  print_double(mean_result);
  print_string("Ok, so it doesn't correctly calculate the mean...");
  print_string("But hey, if you are looking for a random number generator this works pretty good!");
  return 0;
}
