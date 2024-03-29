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
@.str1 = private unnamed_addr constant [38 x i8] c"The are of a circle with 5 radius is:\00"

@PI = global double 3.14159265359

define double @Square(double %n) {
	%pont_1 = alloca double
	store double %n, double* %pont_1
	%cas_1 = load double, double* %pont_1
	%cas_2 = load double, double* %pont_1
	%cas_3 = fmul double %cas_1, %cas_2
	ret double %cas_3
}

define double @CircleArea(double %radius) {
	%pont_2 = alloca double
	store double %radius, double* %pont_2
	%cas_4 = load double, double* %pont_2
	%cas_5 = call double @Square(double %cas_4)
	%cas_6 = load double, double* @PI
	%cas_7 = fmul double %cas_6, %cas_5
	ret double %cas_7
}

define i64 @main() {
	%r = alloca double
	store double 5.0, double* %r
	%cas_8 = load double, double* %r
	%cas_9 = call double @CircleArea(double %cas_8)
	%area = alloca double
	store double %cas_9, double* %area
	%pont_3 = getelementptr inbounds [38 x i8], [38 x i8]* @.str1, i64 0, i64 0
	call void @print_string(i8* %pont_3)
	%cas_11 = load double, double* %area
	call void @print_double(double %cas_11)
	ret i64 0
}
