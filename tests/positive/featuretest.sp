(* Testing all the features of sPLash *)


(* Function declarations *)
len: Int (array: [Int]);
print: Void (value: Int);
RandomInt: Int();
write_to_array: Void (array: [Int], index: Int, Value: Int);
alocate_array: [Int] (size: Int);
string_compare: Int (str1: String, str2: String);
int: Int (n: Double);


function1 : Void ();
function2 : Int (a : String, b : Int, c : Double where c < -0.5);

(* Variable Declarations *)
global_1 : Int;
REFINEDGLOBAL : [Int] where len(REFINEDGLOBAL) > 1;


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

CriticalSection : Void (shared_memory : [Int], task : String) {
    (* Local Variable Declarations *)
    n : Int where n > 0 = len(shared_memory);
    i : Int where i > 0 = 0;
    (* If statement *)
    if string_compare(task, "read") {
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

	buffer : [Int] = alocate_array(100);

    while true {
        (* some binary operations *)
        b:Int = 1 + 2;
        c:Double = b / 3;
        d:Int = int(c) % int(4.0);
        f:Double = d - 0.5;
        (* Using the _ notation for an int *)
        h: Int = -1 + 2_232_2398_2_3;
        flag: Int = h < f;
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
