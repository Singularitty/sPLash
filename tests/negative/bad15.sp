(* definition inside definition *)


f1 : Int () {
	f2 : Double () {
		return 0;
	}
	return 1;
}

main : Int () {
	return 0;
}
