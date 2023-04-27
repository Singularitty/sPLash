(* Invalid type in while condition *)

break: Void();

count_to:Int (num:Int) {
  i:Int = 0;
  while "end" {
    if i == num {
      break();
    }
    i = i + 1;
  }
  return i;
}


main: Int () {
    return 0;
}