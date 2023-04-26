(* Simple calculator in sPLash *)


print: Void (str: String);
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
  if operation == "add" {
    return add(a, b);
  } if operation == "subtract" {
    return subtract(a, b);
  } if operation == "multiply" {
    return multiply(a, b);
  } if operation == "divide" {
    return divide(a, b);
  } else {
    print("Invalid operation");
    return 0;
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
    option: Int = get_input("Enter the option number (1-4): ");
    operation: String = get_operation(option);

    if operation == "invalid" {
      print("Invalid option. Exiting...");
      return 1;
    }

    num1: Double = get_input("Enter the first number: ");
    num2: Double = get_input("Enter the second number: ");

    result: Double = calculate(operation, num1, num2);
    print("The result of the ", operation, " operation is: ", result);
  }
  return 0;
}
