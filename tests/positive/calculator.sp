(* Simple calculator in sPLash *)

string_compare: Int (str1: String, str2: String);
print: Void (str: String);
printf: Void (format: String, arg1: String, arg2: Double);
get_input: Int ();

(* Function to add two numbers *)
add: Double (a: Double, b: Double) {
  return a + b;
}

(* Function to subtract two numbers *)
subtract: Double (a: Double, b: Double) {
  return a - b;
}

(* Function to multiply two numbers *)
multiply: Double (a: Double, b: Double) {
  return a * b;
}

(* Function to divide two numbers *)
divide: Double (a: Double, b: Double where b != 0) {
  return a / b;
}

(* Function to perform the selected operation *)
calculate: Double (operation: String, a: Double, b: Double) {
  if string_compare(operation, "add") {
    return add(a, b);
  } if string_compare(operation, "subtract") {
    return subtract(a, b);
  } if string_compare(operation, "multiply") {
    return multiply(a, b);
  } if string_compare(operation, "divide") {
    return divide(a, b);
  } else {
    print("Invalid operation");
    return 0.;
  }
}

(* Function to display the menu *)
display_menu: Void () {
  print("Select an operation:");
  print("1. Add");
  print("2. Subtract");
  print("3. Multiply");
  print("4. Divide");
}

(* Function to get the operation from user input *)
get_operation: String (option: Int) {
  if option == 1 {
    return "add";
  } if option == 2 {
    return "subtract";
  } if option == 3 {
    return "multiply";
  } if option == 4 {
    return "divide";
  } else {
    return "invalid";
  }
}

main: Int () {

  while true {
    display_menu();
    print("Enter the option number (1-4): ");
    option: Int = get_input();
    operation: String = get_operation(option);

    if string_compare(operation, "invalid") {
      print("Invalid option. Exiting...");
      return 1;
    }

    print("Enter the first number: ");
    num1: Double = get_input();
    print("Enter the second number: ");
    num2: Double = get_input();

    result: Double = calculate(operation, num1, num2);
    printf("The result of the {s} operation is: {f}", operation, result);
  }
  return 0;
}
