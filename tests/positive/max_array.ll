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
@.str1 = private unnamed_addr constant [37 x i8] c"The maximum number in the array is: \00"

define i64 @find_maximum(i64* %array, i64 %size) {
	%pont_1 = alloca i64*
	store i64* %array, i64** %pont_1
	%pont_2 = alloca i64
	store i64 %size, i64* %pont_2
	%pont_3 = getelementptr inbounds i64, i64* %array, i64 0
	%cas_1 = load i64, i64* %pont_3
	%max = alloca i64
	store i64 %cas_1, i64* %max
	%i = alloca i64
	store i64 1, i64* %i
	br label %while.guard._label_1
while.guard._label_1:
	%cas_2 = load i64, i64* %i
	%cas_3 = load i64, i64* %pont_2
	%cas_4 = icmp slt i64 %cas_2, %cas_3
	br i1 %cas_4, label %while.body._label_2, label %while.end._label_3
while.body._label_2:
	%cas_5 = load i64, i64* %i
	%pont_4 = getelementptr inbounds i64, i64* %array, i64 %cas_5
	%cas_6 = load i64, i64* %pont_4
	%cas_7 = load i64, i64* %max
	%cas_8 = icmp sgt i64 %cas_6, %cas_7
	br i1 %cas_8, label %if.then._label_4, label %if.else._label_5
if.then._label_4:
	%cas_9 = load i64, i64* %i
	%pont_5 = getelementptr inbounds i64, i64* %array, i64 %cas_9
	%cas_10 = load i64, i64* %pont_5
	store i64 %cas_10, i64* %max
	br label %if.end._label_6
if.else._label_5:
	br label %if.end._label_6
if.end._label_6:
	%cas_11 = load i64, i64* %i
	%cas_12 = add i64 %cas_11, 1
	store i64 %cas_12, i64* %i
	br label %while.guard._label_1
while.end._label_3:
	%cas_13 = load i64, i64* %max
	ret i64 %cas_13
}

define i64 @main() {
	%array_size = alloca i64
	store i64 5, i64* %array_size
	%cas_14 = load i64, i64* %array_size
	%cas_15 = call i64* @create_array_int(i64 %cas_14)
	%numbers = alloca i64*
	store i64* %cas_15, i64** %numbers
	%value = alloca i64
	store i64 3, i64* %value
	%i = alloca i64
	store i64 0, i64* %i
	br label %while.guard._label_7
while.guard._label_7:
	%cas_16 = load i64, i64* %value
	%cas_17 = icmp slt i64 %cas_16, 5
	br i1 %cas_17, label %while.body._label_8, label %while.end._label_9
while.body._label_8:
	%cas_18 = load i64*, i64** %numbers
	%cas_19 = load i64, i64* %i
	%cas_20 = load i64, i64* %value
	call void @write_to_array_int(i64* %cas_18, i64 %cas_19, i64 %cas_20)
	%cas_22 = load i64, i64* %i
	%cas_23 = add i64 %cas_22, 1
	store i64 %cas_23, i64* %i
	%cas_24 = load i64, i64* %value
	%cas_25 = add i64 %cas_24, 2
	store i64 %cas_25, i64* %value
	br label %while.guard._label_7
while.end._label_9:
	%cas_26 = load i64*, i64** %numbers
	%cas_27 = load i64, i64* %array_size
	%cas_28 = call i64 @find_maximum(i64* %cas_26, i64 %cas_27)
	%max_number = alloca i64
	store i64 %cas_28, i64* %max_number
	%pont_6 = getelementptr inbounds [37 x i8], [37 x i8]* @.str1, i64 0, i64 0
	call void @print_string(i8* %pont_6)
	%cas_30 = load i64, i64* %max_number
	call void @print_int(i64 %cas_30)
	ret i64 0
}
