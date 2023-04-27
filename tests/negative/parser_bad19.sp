(* Missing type on main definition *)

factorial: Int (n: Int where n >= 0) {
  if n == 0 {
    return 1;
  } else {
    return n * factorial(n - 1);
  }
}

main () {asd;}
