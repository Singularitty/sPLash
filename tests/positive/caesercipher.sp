(* Caesar cipher in sPLash *)

(* 
   Function to encrypt a character, assumes that type Char can be interpeted as a Int
   when performing arithmetic operations 
*)
encrypt_char: Char (c: Char, shift: Int where shift >= 0) {
  if "A" <= c && c <= "Z" {
    return (((c - "A") + shift) % 26) + "A";
  }
  if "a" <= c && c <= "z" {
    return (((c - "a") + shift) % 26) + "a";
  }
  return c;
}

(* Function to encrypt a string *)
encrypt_string: String (input: String, shift: Int where shift >= 0) {
  encrypted: String = "";
  i: Int = 0;
  while i < len(input) {
    encrypted = encrypted + encrypt_char(input[i], shift);
    i = i + 1;
  }
  return encrypted;
}

main: Int () {
  input: String = "Hello, World!";
  shift: Int where shift >= 0 = 3;

  encrypted: String = encrypt_string(input, shift);
  print("Original text: ", input);
  print("Encrypted text: ", encrypted);
  return 0;
}
