(* Too many arguments *)

break: Void();

bad:Int (num:Int, b: String) {
  return 0;
}


main: Int () {

    bad(2, "str", 2, 3, 5);

    return 0;
}