(* Return of non initialized var *)

break: Void();

bad:Int (num:Int) {
  while false {
    i: Int = 0;
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