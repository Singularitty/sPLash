(* Calculate the area of a cirlce in sPLash *)


print_string: Void (str: String);
print_double: Void (n : Double);

PI : Double = 3.14159265359;

Square : Double (n : Double) {
	return n*n;
}

CircleArea : Double (radius : Double where radius > 0) {
	return PI * Square(radius);
}

main : Int () {
	r : Double where r > 0 = 5;
	area : Double = CircleArea(r);
	print_string("The are of a circle with 5 radius is:");
	print_double(area);
	return 0;
}
