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
@.str1 = private unnamed_addr constant [26 x i8] c"The square root of 25 is:\00"

define double @abs(double %x) {
	%pont_1 = alloca double
	store double %x, double* %pont_1
	%cas_1 = load double, double* %pont_1
	%result = alloca double
	store double %cas_1, double* %result
	%cas_2 = load double, double* %pont_1
	%cas_3 = sitofp i64 0 to double
	%cas_4 = fcmp olt double %cas_2, %cas_3
	br i1 %cas_4, label %if.then._label_1, label %if.else._label_2
if.then._label_1:
	%cas_5 = load double, double* %result
	%cas_6 = sitofp i64 -1 to double
	%cas_7 = fmul double %cas_5, %cas_6
	store double %cas_7, double* %result
	br label %if.end._label_3
if.else._label_2:
	br label %if.end._label_3
if.end._label_3:
	%cas_8 = load double, double* %result
	ret double %cas_8
}

define double @sqrt(double %n) {
	%pont_2 = alloca double
	store double %n, double* %pont_2
	%cas_9 = load double, double* %pont_2
	%cas_10 = fdiv double %cas_9, 2.0
	%guess = alloca double
	store double %cas_10, double* %guess
	%epsilon = alloca double
	store double 0.001, double* %epsilon
	br label %while.guard._label_4
while.guard._label_4:
	%cas_11 = load double, double* %guess
	%cas_12 = load double, double* %pont_2
	%cas_13 = fsub double %cas_11, %cas_12
	%cas_14 = load double, double* %guess
	%cas_15 = fmul double %cas_14, %cas_13
	%cas_16 = call double @abs(double %cas_15)
	%cas_17 = load double, double* %epsilon
	%cas_18 = fcmp oge double %cas_16, %cas_17
	br i1 %cas_18, label %while.body._label_5, label %while.end._label_6
while.body._label_5:
	%cas_19 = load double, double* %guess
	%cas_20 = load double, double* %pont_2
	%cas_21 = fadd double %cas_19, %cas_20
	%cas_22 = load double, double* %guess
	%cas_23 = fdiv double %cas_21, %cas_22
	%cas_24 = fdiv double %cas_23, 2.0
	store double %cas_24, double* %guess
	br label %while.guard._label_4
while.end._label_6:
	%cas_25 = load double, double* %guess
	ret double %cas_25
}

define i64 @main() {
	%number = alloca double
	store double 25.0, double* %number
	%cas_26 = load double, double* %number
	%cas_27 = call double @sqrt(double %cas_26)
	%sqrt_number = alloca double
	store double %cas_27, double* %sqrt_number
	%pont_3 = getelementptr inbounds [26 x i8], [26 x i8]* @.str1, i64 0, i64 0
	call void @print_string(i8* %pont_3)
	%cas_29 = load double, double* %sqrt_number
	call void @print_double(double %cas_29)
	ret i64 0
}
