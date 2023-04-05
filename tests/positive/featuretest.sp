(* Testing all the features of sPLash *)

(* Variable Declarations *)
global_1 : Int;
REFINEDGLOBAL : [Int] where len(REFINEDGLOBAL) > 1;

(* Function Declarations *)
function1 : Void ();
function2 : Int (a : String, b : Char, c : Double where c < -0.5);

(* Value definition *)
global_value : Int = 10;
mutex : Int where (mutex == 0) || (mutex == 1) = 1;

(* Function definition *)
lock : Int () {
    if mutex == 0 {
        (* Lock not acquired *)
        return 0;
    } else {
        (* Lock acquired *)
        mutex = mutex - 1;
        return 1;
    }
}

unlock : Int () {
    if mutex == 0 {
        (* release lock *)
        mutex = mutex + 1;
        return 1;
    } else {
        (* No lock to release *)
        return 0;
    }
}

CriticalSection : Void (shared_memory : [Int], task : String where ((task == "read") || (task == "write"))) {
    (* Local Variable Declarations *)
    n : Int where n > 0 = len(shared_memory);
    i : Int where i > 0 = 0;
    (* If statement *)
    if task == "read" {
        (* While statement *)
        while i < n {
            print(shared_memory[i]);
            i = i + 1;
        }
    } else {
    	(* Nested while cycle  *)
        while i < n {
            j : Int = RandomInt();
            write_to_array(shared_memory, i, j);
        }
    }
}


main : Int () {

	buffer : [Int] = alocate_array(Int, 100);

    while true {
        (* some binary operations *)
        b = 1 + 2;
        c = b / 3;
        d = c % 4.0;
        f = d - 0.5;
        h = -1 + 2;
        flag = h < f;
        flag = flag || (f > c);
        flag = flag && (b <= d);
        flag = flag == (c >= d);
        flag = flag != !flag;
        lock();
        if flag {
        	CriticalSection(buffer, "read");
        } else {
        	CriticalSection(buffer, "write");
        }
        unlock();
        
    }


    return 0;
}
