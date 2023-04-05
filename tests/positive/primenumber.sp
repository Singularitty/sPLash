(* Check if a number is prime in sPLash *)

(* Function to check if a number is prime *)
is_prime: Bool (num: Int) {
  if num <= 1 {
    return false;
  }
  if num <= 3 {
    return true;
  }
  if (num % 2 == 0) || (num % 3 == 0) {
    return false;
  }

  i: Int = 5;
  while (i * i) <= num {
    if (num % i == 0) || (num % (i + 2) == 0) {
      return false;
    }
    i = i + 6;
  }
  return true;
}

main: Int () {
  number: Int = 29;
  prime_check: Bool = is_prime(number);

  if prime_check {
    print(number, " is prime");
  } else {
    print(number, " is not prime");
  }
  return 0;
}
