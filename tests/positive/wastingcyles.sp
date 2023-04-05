(* Some random functions to demonstrate that all sPLash grammar is correctly defined *)


(* Declarations *)



(* This function never ends *)
f1 : Float (b: Float where b < -10 && b > -11) {
    if b > (* Comment in the middle of a binary operation *) -10 {
        b = b - 1;
        f1(b);
    } else {
        b = b + 1;
        f1(b);
    }
}

(* Friendly warning *)
warning : void () {
    print("You should never call f1.");
}

(* Safety off *)
safety : Bool = false;

(* I am out of ideas for programs, sorry *)
gibirish : string (n : Int where n % 1 == 0) {
    random_int = 1013;
    if random_int % 2 == 0 {
        return "whoa";
    } if random_int / 3 == 123 - 321 * 100 {
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

main : int () {
    (* Double not *)
    warning();
    if !!satety {
        gibirish(123123);
    } else {
        f1(-10);
    }
    return 0;
}

