(* Some random functions *)

print: Void (content: String);
int: Int (n: Double);

(* This function never ends *)
f1 : Double (b: Double where b < -10 && b > -11) {
    if b > (* Comment in the middle of a binary operation *) -10 {
        b = b - 1;
        f1(b);
    } else {
        b = b + 1;
        f1(b);
    }
}

(* Friendly warning *)
warning : Void () {
    print("You should never call f1.");
}

(* Safety off *)
safety : Int = false;


gibirish : String (n : Int where n % 1 == 0) {
    random_int: Int = 1013;
    a: Int = 0;
    b: Int = 0;
    c: Int = 0;
    if random_int % 2 == 0 {
        return "whoa";
    } if int(random_int / 3) == 123 - 321 * 100 {
        return "there";
    } if random_int * 5 == 10 % 2 {
        return "hello";
    } else {
        (* Some binary operators *)
        b = true && false;
        a = b || true;
        c = a == b;
        if c {
            return "false";
        } else {
            return "true";
        }
    }
    return "?";
}

main : Int () {
    (* Double not *)
    warning();
    if !!safety {
        gibirish(123123);
    } else {
        f1(-10);
    }
    return 0;
}

