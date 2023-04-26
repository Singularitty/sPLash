(* Calculate the area of a cirlce in sPLash *)


printf: Void (format: String, arg1: Double, arg2: Double);

get_input: Int ();

PI : Double = 3.14159265359;

Square : Double (n : Double) {
	return n*n;
}

CircleArea : Double (radius : Double where radius > 0.0) {
	return PI * Square(radius);
}

main : Int () {
	r : Double where r > 0 = get_input();
	area : Double = CircleArea(r);
	printf("Area of a cirle of radius {f} is {f} ", r, area);
	return 0;
}
