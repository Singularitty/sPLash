; Module functions declarations and definitions

; Declare C functions that will do the actual heavy work
declare i32 @printf(i8*, ...)
declare i8* @malloc(i64)

declare void @free(i8*)
; Print functions
define void @print_int(i64 %i) { 
        %format = getelementptr inbounds [4 x i8], [4 x i8]* @int_format, i64 0, i64 0
        call i32 (i8*, ...) @printf(i8* %format, i64 %i) 
        ret void 
        }
define void @print_double(double %d) {
            %format = getelementptr inbounds [4 x i8], [4 x i8]* @double_format, i64 0, i64 0
            call i32 (i8*, ...) @printf(i8* %format, double %d)
            ret void
            }
define void @print_string(i8* %s) {
            %format = getelementptr inbounds [4 x i8], [4 x i8]* @string_format, i64 0, i64 0
            call i32 (i8*, ...) @printf(i8* %format, i8* %s)
            ret void
            }
@int_format = private unnamed_addr constant [4 x i8] c"%d
 "
@double_format = private unnamed_addr constant [4 x i8] c"%f
 "
@string_format = private unnamed_addr constant [4 x i8] c"%s
\00"

; Array allocation
define i64* @create_array_int(i64 %size) {
            %bytes = mul i64 %size, 4
            %mem = call i8* @malloc(i64 %bytes)
            %arr = bitcast i8* %mem to i64*
            ret i64* %arr
            }
define double* @create_array_double(i64 %size) {
            %bytes = mul i64 %size, 8
            %mem = call i8* @malloc(i64 %bytes)
            %arr = bitcast i8* %mem to double*
            ret double* %arr
            }
define void @write_to_array_int(i64* %arr, i64 %index, i64 %value) {
            %ptr = getelementptr inbounds i64, i64* %arr, i64 %index
            store i64 %value, i64* %ptr
            ret void
            }
define void @write_to_array_double(double* %arr, i64 %index, double %value) {
            %ptr = getelementptr inbounds double, double* %arr, i64 %index
            store double %value, double* %ptr
            ret void
            }
define void @freeInt(i64* %array) {
            %array_cast = bitcast i64* %array to i8*
            call void @free(i8* %array_cast)
            ret void
            }
define void @freeDouble(double* %array) {
            %array_cast = bitcast double* %array to i8*
            call void @free(i8* %array_cast)
            ret void
            }

; Start of program
@.str1 = private unnamed_addr constant [39 x i8] c"Fibonacci sequence until 10th element:\00"

define i64 @fibonacci(i64 %n) {
	%pont_1 = alloca i64
	store i64 %n, i64* %pont_1
	%a = alloca i64
	store i64 0, i64* %a
	%b = alloca i64
	store i64 1, i64* %b
	%i = alloca i64
	store i64 0, i64* %i
	%cas_1 = load i64, i64* %a
	%temp = alloca i64
	store i64 %cas_1, i64* %temp
	br label %while.guard._label_1
while.guard._label_1:
	%cas_2 = load i64, i64* %i
	%cas_3 = load i64, i64* %pont_1
	%cas_4 = icmp slt i64 %cas_2, %cas_3
	br i1 %cas_4, label %while.body._label_2, label %while.end._label_3
while.body._label_2:
	%cas_5 = load i64, i64* %a
	store i64 %cas_5, i64* %temp
	%cas_6 = load i64, i64* %b
	store i64 %cas_6, i64* %a
	%cas_7 = load i64, i64* %temp
	%cas_8 = load i64, i64* %b
	%cas_9 = add i64 %cas_7, %cas_8
	store i64 %cas_9, i64* %b
	%cas_10 = load i64, i64* %i
	%cas_11 = add i64 %cas_10, 1
	store i64 %cas_11, i64* %i
	br label %while.guard._label_1
while.end._label_3:
	%cas_12 = load i64, i64* %a
	ret i64 %cas_12
}

define void @fill_fibonacci(i64* %arr, i64 %n) {
	%pont_2 = alloca i64*
	store i64* %arr, i64** %pont_2
	%pont_3 = alloca i64
	store i64 %n, i64* %pont_3
	%i = alloca i64
	store i64 0, i64* %i
	br label %while.guard._label_4
while.guard._label_4:
	%cas_13 = load i64, i64* %i
	%cas_14 = load i64, i64* %pont_3
	%cas_15 = icmp slt i64 %cas_13, %cas_14
	br i1 %cas_15, label %while.body._label_5, label %while.end._label_6
while.body._label_5:
	%cas_16 = load i64*, i64** %pont_2
	%cas_17 = load i64, i64* %i
	%cas_18 = load i64, i64* %i
	%cas_19 = call i64 @fibonacci(i64 %cas_18)
	call void @write_to_array_int(i64* %cas_16, i64 %cas_17, i64 %cas_19)
	%cas_21 = load i64, i64* %i
	%cas_22 = add i64 %cas_21, 1
	store i64 %cas_22, i64* %i
	br label %while.guard._label_4
while.end._label_6:
	ret void
}

define void @print_array(i64* %arr, i64 %n) {
	%pont_4 = alloca i64*
	store i64* %arr, i64** %pont_4
	%pont_5 = alloca i64
	store i64 %n, i64* %pont_5
	%i = alloca i64
	store i64 0, i64* %i
	br label %while.guard._label_7
while.guard._label_7:
	%cas_23 = load i64, i64* %i
	%cas_24 = load i64, i64* %pont_5
	%cas_25 = icmp slt i64 %cas_23, %cas_24
	br i1 %cas_25, label %while.body._label_8, label %while.end._label_9
while.body._label_8:
	%cas_26 = load i64, i64* %i
	%pont_6 = getelementptr inbounds i64, i64* %arr, i64 %cas_26
	%cas_27 = load i64, i64* %pont_6
	call void @print_int(i64 %cas_27)
	%cas_29 = load i64, i64* %i
	%cas_30 = add i64 %cas_29, 1
	store i64 %cas_30, i64* %i
	br label %while.guard._label_7
while.end._label_9:
	ret void
}

define i64 @main() {
	%num_terms = alloca i64
	store i64 11, i64* %num_terms
	%cas_31 = load i64, i64* %num_terms
	%cas_32 = call i64* @create_array_int(i64 %cas_31)
	%fib_sequence = alloca i64*
	store i64* %cas_32, i64** %fib_sequence
	%cas_33 = load i64*, i64** %fib_sequence
	%cas_34 = load i64, i64* %num_terms
	call void @fill_fibonacci(i64* %cas_33, i64 %cas_34)
	%pont_7 = getelementptr inbounds [39 x i8], [39 x i8]* @.str1, i64 0, i64 0
	call void @print_string(i8* %pont_7)
	%cas_37 = load i64*, i64** %fib_sequence
	%cas_38 = load i64, i64* %num_terms
	call void @print_array(i64* %cas_37, i64 %cas_38)
	%cas_40 = load i64*, i64** %fib_sequence
	call void @freeInt(i64* %cas_40)
	ret i64 0
}
