(* Incorrect type for index access *)

arr: [Int] ();

incorrect_index_access:Void () {
  a : [Int] = arr();
  index:String = "0";
  value:Int = a[index];
}

main: Int () {
    return 0;
}