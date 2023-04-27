(* Function to calculate the mean of an array of integers *)

printf: Void (format: String, arg: Double);
alocate_array: [Int] (size: Int);
write_to_array: Void (array: [Int], index: Int, value: Int);

sqrt: Double (n: Double);


mean:Double (arr:[Int], size:Int) {
  sum:Int = 0;
  i: Int = 0;
  while i < size {
    sum = sum + arr[i];
    i = i + 1;
  }

  return sum / size;
}

(* Function to calculate the standard deviation of an array of integers *)
stddev:Double (arr:[Int], size:Int) {
  mean_val:Double = mean(arr, size);
  sum_squared_diff:Double = 0;

  i: Int = 0;
  diff: Double = 0;
  while i < size {
    diff = arr[i] - mean_val;
    sum_squared_diff = sum_squared_diff + (diff * diff);
    i = i + 1;
  }

  return sqrt(sum_squared_diff / size);
}


main: Int () {
  array_size:Int = 5;
  numbers:[Int] = alocate_array(array_size);
  value: Int = 3;
  i: Int = 0;
  while value < 11 {
    write_to_array(numbers, i, value);
    i = i + 1;
    value = value + 2;
  }

  mean_result:Double = mean(numbers, array_size);
  stddev_result:Double = stddev(numbers, array_size);

  printf("Mean: {f}", mean_result);
  printf("Standard Deviation: {f}", stddev_result);
}
