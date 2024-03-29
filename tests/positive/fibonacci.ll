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
@.str1 = private unnamed_addr constant [20 x i8] c"Fibonacci sequence:\00"

define i64 @fibonacci(i64 %n) {
	%pont_1 = alloca i64
	store i64 %n, i64* %pont_1
	%a = alloca i64
	store i64 0, i64* %a
	%b = alloca i64
	store i64 1, i64* %b
	%temp = alloca i64
	store i64 0, i64* %temp
	%i = alloca i64
	store i64 0, i64* %i
	br label %while.guard._label_1
while.guard._label_1:
	%cas_1 = load i64, i64* %i
	%cas_2 = load i64, i64* %pont_1
	%cas_3 = icmp slt i64 %cas_1, %cas_2
	br i1 %cas_3, label %while.body._label_2, label %while.end._label_3
while.body._label_2:
	%cas_4 = load i64, i64* %a
	call void @print_int(i64 %cas_4)
	%cas_6 = load i64, i64* %a
	%cas_7 = load i64, i64* %b
	%cas_8 = add i64 %cas_6, %cas_7
	store i64 %cas_8, i64* %temp
	%cas_9 = load i64, i64* %b
	store i64 %cas_9, i64* %a
	%cas_10 = load i64, i64* %temp
	store i64 %cas_10, i64* %b
	%cas_11 = load i64, i64* %i
	%cas_12 = add i64 %cas_11, 1
	store i64 %cas_12, i64* %i
	br label %while.guard._label_1
while.end._label_3:
	%cas_13 = load i64, i64* %a
	ret i64 %cas_13
}

define i64 @main() {
	%num_terms = alloca i64
	store i64 25, i64* %num_terms
	%pont_2 = getelementptr inbounds [20 x i8], [20 x i8]* @.str1, i64 0, i64 0
	call void @print_string(i8* %pont_2)
	%cas_15 = load i64, i64* %num_terms
	%cas_16 = call i64 @fibonacci(i64 %cas_15)
	ret i64 0
}
