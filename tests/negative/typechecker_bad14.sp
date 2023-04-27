(* Wrong arg type *)

break: Void();

bad:Int (num:Int, b: String) {
  return 0;
}


main: Int () {

    bad("str", 2);

    return 0;
}