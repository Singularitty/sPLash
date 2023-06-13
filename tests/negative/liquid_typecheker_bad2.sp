a : Int where a < 0 = -1;
b : Int where b == a = a;
c : Int where c > b = b;

main : Int () {
    return 0;
}