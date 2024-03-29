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
@.str1 = private unnamed_addr constant [39 x i8] c"Mean of the numbers 3, 5, 7, 9, 11 is:\00"

@.str2 = private unnamed_addr constant [50 x i8] c"Ok, so it doesn't correctly calculate the mean...\00"

@.str3 = private unnamed_addr constant [82 x i8] c"But hey, if you are looking for a random number generator this works pretty good!\00"

declare double @sqrt(double)

define double @mean(i64* %arr, i64 %size) {
	%pont_1 = alloca i64*
	store i64* %arr, i64** %pont_1
	%pont_2 = alloca i64
	store i64 %size, i64* %pont_2
	%sum = alloca i64
	store i64 0, i64* %sum
	%i = alloca i64
	store i64 0, i64* %i
	br label %while.guard._label_1
while.guard._label_1:
	%cas_1 = load i64, i64* %i
	%cas_2 = load i64, i64* %pont_2
	%cas_3 = icmp slt i64 %cas_1, %cas_2
	br i1 %cas_3, label %while.body._label_2, label %while.end._label_3
while.body._label_2:
	%cas_4 = load i64, i64* %i
	%pont_3 = getelementptr inbounds i64, i64* %arr, i64 %cas_4
	%cas_5 = load i64, i64* %pont_3
	%cas_6 = load i64, i64* %sum
	%cas_7 = add i64 %cas_6, %cas_5
	store i64 %cas_7, i64* %sum
	%cas_8 = load i64, i64* %i
	%cas_9 = add i64 %cas_8, 1
	store i64 %cas_9, i64* %i
	br label %while.guard._label_1
while.end._label_3:
	%cas_10 = load i64, i64* %sum
	%cas_11 = load i64, i64* %pont_2
	%cas_13 = sitofp i64 %cas_10 to double
	%cas_14 = sitofp i64 %cas_11 to double
	%cas_12 = fdiv double %cas_13, %cas_14
	ret double %cas_12
}

define i64 @main() {
	%array_size = alloca i64
	store i64 5, i64* %array_size
	%cas_15 = load i64, i64* %array_size
	%cas_16 = call i64* @create_array_int(i64 %cas_15)
	%numbers = alloca i64*
	store i64* %cas_16, i64** %numbers
	%value = alloca i64
	store i64 3, i64* %value
	%i = alloca i64
	store i64 0, i64* %i
	br label %while.guard._label_4
while.guard._label_4:
	%cas_17 = load i64, i64* %value
	%cas_18 = icmp slt i64 %cas_17, 5
	br i1 %cas_18, label %while.body._label_5, label %while.end._label_6
while.body._label_5:
	%cas_19 = load i64*, i64** %numbers
	%cas_20 = load i64, i64* %i
	%cas_21 = load i64, i64* %value
	call void @write_to_array_int(i64* %cas_19, i64 %cas_20, i64 %cas_21)
	%cas_23 = load i64, i64* %i
	%cas_24 = add i64 %cas_23, 1
	store i64 %cas_24, i64* %i
	%cas_25 = load i64, i64* %value
	%cas_26 = add i64 %cas_25, 2
	store i64 %cas_26, i64* %value
	br label %while.guard._label_4
while.end._label_6:
	%cas_27 = load i64*, i64** %numbers
	%cas_28 = load i64, i64* %array_size
	%cas_29 = call double @mean(i64* %cas_27, i64 %cas_28)
	%mean_result = alloca double
	store double %cas_29, double* %mean_result
	%pont_4 = getelementptr inbounds [39 x i8], [39 x i8]* @.str1, i64 0, i64 0
	call void @print_string(i8* %pont_4)
	%cas_31 = load double, double* %mean_result
	call void @print_double(double %cas_31)
	%pont_5 = getelementptr inbounds [50 x i8], [50 x i8]* @.str2, i64 0, i64 0
	call void @print_string(i8* %pont_5)
	%pont_6 = getelementptr inbounds [82 x i8], [82 x i8]* @.str3, i64 0, i64 0
	call void @print_string(i8* %pont_6)
	ret i64 0
}
