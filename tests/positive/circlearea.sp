(* Calculate the area of a cirlce in sPLash *)

PI : Double = 3.14159265359;

Square : Double (n : Double) {
	return n*n;
}

CircleArea : Double (radius : Double where radius > 0.0) {
	return PI * Square(r);
}

main : Int () {
	r : Double where r > 0 = get_input();
	area : Double = CircleArea(r);
	print("Area of a cirle of radius ", r, " is ", area);
	return 0;
}
