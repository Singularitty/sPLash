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
@.str1 = private unnamed_addr constant [25 x i8] c"GCD and LCM of 15 and 25\00"

@.str2 = private unnamed_addr constant [5 x i8] c"GCD:\00"

@.str3 = private unnamed_addr constant [5 x i8] c"LCM:\00"

define i64 @gcd(i64 %a, i64 %b) {
	%pont_1 = alloca i64
	store i64 %a, i64* %pont_1
	%pont_2 = alloca i64
	store i64 %b, i64* %pont_2
	%result = alloca i64
	store i64 0, i64* %result
	%cas_1 = load i64, i64* %pont_2
	%cas_2 = icmp eq i64 %cas_1, 0
	br i1 %cas_2, label %if.then._label_1, label %if.else._label_2
if.then._label_1:
	%cas_3 = load i64, i64* %pont_1
	store i64 %cas_3, i64* %result
	br label %if.end._label_3
if.else._label_2:
	%cas_4 = load i64, i64* %pont_2
	%cas_5 = load i64, i64* %pont_1
	%cas_6 = load i64, i64* %pont_2
	%cas_7 = srem i64 %cas_5, %cas_6
	%cas_8 = call i64 @gcd(i64 %cas_4, i64 %cas_7)
	store i64 %cas_8, i64* %result
	br label %if.end._label_3
if.end._label_3:
	%cas_9 = load i64, i64* %result
	ret i64 %cas_9
}

define double @lcm(i64 %a, i64 %b) {
	%pont_3 = alloca i64
	store i64 %a, i64* %pont_3
	%pont_4 = alloca i64
	store i64 %b, i64* %pont_4
	%cas_10 = load i64, i64* %pont_3
	%cas_11 = load i64, i64* %pont_4
	%cas_12 = mul i64 %cas_10, %cas_11
	%cas_13 = load i64, i64* %pont_3
	%cas_14 = load i64, i64* %pont_4
	%cas_15 = call i64 @gcd(i64 %cas_13, i64 %cas_14)
	%cas_17 = sitofp i64 %cas_12 to double
	%cas_18 = sitofp i64 %cas_15 to double
	%cas_16 = fdiv double %cas_17, %cas_18
	ret double %cas_16
}

define i64 @main() {
	%num1 = alloca i64
	store i64 15, i64* %num1
	%num2 = alloca i64
	store i64 25, i64* %num2
	%cas_19 = load i64, i64* %num1
	%cas_20 = load i64, i64* %num2
	%cas_21 = call i64 @gcd(i64 %cas_19, i64 %cas_20)
	%result_gcd = alloca i64
	store i64 %cas_21, i64* %result_gcd
	%cas_22 = load i64, i64* %num1
	%cas_23 = load i64, i64* %num2
	%cas_24 = call double @lcm(i64 %cas_22, i64 %cas_23)
	%result_lcm = alloca double
	store double %cas_24, double* %result_lcm
	%pont_5 = getelementptr inbounds [25 x i8], [25 x i8]* @.str1, i64 0, i64 0
	call void @print_string(i8* %pont_5)
	%pont_6 = getelementptr inbounds [5 x i8], [5 x i8]* @.str2, i64 0, i64 0
	call void @print_string(i8* %pont_6)
	%cas_27 = load i64, i64* %result_gcd
	call void @print_int(i64 %cas_27)
	%pont_7 = getelementptr inbounds [5 x i8], [5 x i8]* @.str3, i64 0, i64 0
	call void @print_string(i8* %pont_7)
	%cas_30 = load double, double* %result_lcm
	call void @print_double(double %cas_30)
	ret i64 0
}
