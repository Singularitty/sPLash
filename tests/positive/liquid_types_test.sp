(* Showcase of the capabilities of the liquid type checker *)

print_string: Void (str: String);
print_double: Void (n: Double);

(* We can use these refined types on function parameters to have some ensurance about the passed args *)
func: Double (r: Int where r >= 0, pi: Double where (pi / PI) - 1 >= -0.01) {
    return r*r*pi;
}

main: Int () {

    (* Defining an absolute error for a variable *)
    PI: Double where PI == 3.14159265359 = 3.14159265359;
    PI_3: Double where PI_3 == 3.14 = 3.14;
    (* Here we can define that the absolute error must be 0.01, if we decrease it to 0.000001 this will not type check *)
    PI_APROX: Double where (PI_APROX / PI) - 1 >= -0.01 = PI_3; 


    (* We can also set it so that variables are always positive *)
    a: Int where a >= 0 = 1;
    (* b + 1 > 0 <=> b > -1 <=> b >= 0, so this will type check *)
    b: Int where b + 1 > 0 = a;
    b2: Int where b2 > -1 = a;

    (* Simple expressions like the ones above are allowed, but we cannot use && or || to chain multiple conditions *)
    (* Type checkers to do not perform evaluation, therefore we do not check the result of a operation is a subtype of a refined type. This would have to be checked on runtime. *)
    c: Int where c > 0 = 0 + 1;

    (* We also do not check if a literal conforms to the refinement, as literals are not refined types. This would have to be checked on runtime. *)
    d: Int where d != 0 = 0;

    radius: Int where radius == 12 = 12;
    (* Here we can give a value of Pi that is within the allowed error *)
    area: Double = func(radius, PI_APROX);
    print_string("The area of a circle with radius ");
    print_double(radius);
    print_string("is");
    print_double(area);
    return 0;
}