
func : Int (a : Int where a == 1) {
    return 1;
}

main : Int () {
    c : Int where c == 0 = 0;
    func(c);
    return 0;
}