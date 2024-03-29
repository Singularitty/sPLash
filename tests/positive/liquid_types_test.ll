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
@.str1 = private unnamed_addr constant [34 x i8] c"The area of a circle with radius \00"

@.str2 = private unnamed_addr constant [3 x i8] c"is\00"

define double @func(i64 %r, double %pi) {
	%pont_1 = alloca i64
	store i64 %r, i64* %pont_1
	%pont_2 = alloca double
	store double %pi, double* %pont_2
	%cas_1 = load i64, i64* %pont_1
	%cas_2 = load i64, i64* %pont_1
	%cas_3 = mul i64 %cas_1, %cas_2
	%cas_4 = load double, double* %pont_2
	%cas_5 = sitofp i64 %cas_3 to double
	%cas_6 = fmul double %cas_5, %cas_4
	ret double %cas_6
}

define i64 @main() {
	%PI = alloca double
	store double 3.14159265359, double* %PI
	%PI_3 = alloca double
	store double 3.14, double* %PI_3
	%cas_7 = load double, double* %PI_3
	%PI_APROX = alloca double
	store double %cas_7, double* %PI_APROX
	%a = alloca i64
	store i64 1, i64* %a
	%cas_8 = load i64, i64* %a
	%b = alloca i64
	store i64 %cas_8, i64* %b
	%cas_9 = load i64, i64* %a
	%b2 = alloca i64
	store i64 %cas_9, i64* %b2
	%cas_10 = add i64 0, 1
	%c = alloca i64
	store i64 %cas_10, i64* %c
	%d = alloca i64
	store i64 0, i64* %d
	%radius = alloca i64
	store i64 12, i64* %radius
	%cas_11 = load i64, i64* %radius
	%cas_12 = load double, double* %PI_APROX
	%cas_13 = call double @func(i64 %cas_11, double %cas_12)
	%area = alloca double
	store double %cas_13, double* %area
	%pont_3 = getelementptr inbounds [34 x i8], [34 x i8]* @.str1, i64 0, i64 0
	call void @print_string(i8* %pont_3)
	%cas_15 = load i64, i64* %radius
	%cas_16 = sitofp i64 %cas_15 to double
	call void @print_double(double %cas_16)
	%pont_4 = getelementptr inbounds [3 x i8], [3 x i8]* @.str2, i64 0, i64 0
	call void @print_string(i8* %pont_4)
	%cas_19 = load double, double* %area
	call void @print_double(double %cas_19)
	ret i64 0
}
