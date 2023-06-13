	.text
	.file	"circlearea.ll"
	.globl	print_int                       # -- Begin function print_int
	.p2align	4, 0x90
	.type	print_int,@function
print_int:                              # @print_int
	.cfi_startproc
# %bb.0:
	pushq	%rax
	.cfi_def_cfa_offset 16
	movq	%rdi, %rsi
	leaq	.Lint_format(%rip), %rdi
	movb	$0, %al
	callq	printf@PLT
	popq	%rax
	.cfi_def_cfa_offset 8
	retq
.Lfunc_end0:
	.size	print_int, .Lfunc_end0-print_int
	.cfi_endproc
                                        # -- End function
	.globl	print_double                    # -- Begin function print_double
	.p2align	4, 0x90
	.type	print_double,@function
print_double:                           # @print_double
	.cfi_startproc
# %bb.0:
	pushq	%rax
	.cfi_def_cfa_offset 16
	leaq	.Ldouble_format(%rip), %rdi
	movb	$1, %al
	callq	printf@PLT
	popq	%rax
	.cfi_def_cfa_offset 8
	retq
.Lfunc_end1:
	.size	print_double, .Lfunc_end1-print_double
	.cfi_endproc
                                        # -- End function
	.globl	print_string                    # -- Begin function print_string
	.p2align	4, 0x90
	.type	print_string,@function
print_string:                           # @print_string
	.cfi_startproc
# %bb.0:
	pushq	%rax
	.cfi_def_cfa_offset 16
	movq	%rdi, %rsi
	leaq	.Lstring_format(%rip), %rdi
	movb	$0, %al
	callq	printf@PLT
	popq	%rax
	.cfi_def_cfa_offset 8
	retq
.Lfunc_end2:
	.size	print_string, .Lfunc_end2-print_string
	.cfi_endproc
                                        # -- End function
	.globl	create_array_int                # -- Begin function create_array_int
	.p2align	4, 0x90
	.type	create_array_int,@function
create_array_int:                       # @create_array_int
	.cfi_startproc
# %bb.0:
	pushq	%rax
	.cfi_def_cfa_offset 16
	shlq	$2, %rdi
	callq	malloc@PLT
	popq	%rcx
	.cfi_def_cfa_offset 8
	retq
.Lfunc_end3:
	.size	create_array_int, .Lfunc_end3-create_array_int
	.cfi_endproc
                                        # -- End function
	.globl	create_array_double             # -- Begin function create_array_double
	.p2align	4, 0x90
	.type	create_array_double,@function
create_array_double:                    # @create_array_double
	.cfi_startproc
# %bb.0:
	pushq	%rax
	.cfi_def_cfa_offset 16
	shlq	$3, %rdi
	callq	malloc@PLT
	popq	%rcx
	.cfi_def_cfa_offset 8
	retq
.Lfunc_end4:
	.size	create_array_double, .Lfunc_end4-create_array_double
	.cfi_endproc
                                        # -- End function
	.globl	write_to_array_int              # -- Begin function write_to_array_int
	.p2align	4, 0x90
	.type	write_to_array_int,@function
write_to_array_int:                     # @write_to_array_int
	.cfi_startproc
# %bb.0:
	movq	%rdx, (%rdi,%rsi,8)
	retq
.Lfunc_end5:
	.size	write_to_array_int, .Lfunc_end5-write_to_array_int
	.cfi_endproc
                                        # -- End function
	.globl	write_to_array_double           # -- Begin function write_to_array_double
	.p2align	4, 0x90
	.type	write_to_array_double,@function
write_to_array_double:                  # @write_to_array_double
	.cfi_startproc
# %bb.0:
	movsd	%xmm0, (%rdi,%rsi,8)
	retq
.Lfunc_end6:
	.size	write_to_array_double, .Lfunc_end6-write_to_array_double
	.cfi_endproc
                                        # -- End function
	.globl	freeInt                         # -- Begin function freeInt
	.p2align	4, 0x90
	.type	freeInt,@function
freeInt:                                # @freeInt
	.cfi_startproc
# %bb.0:
	pushq	%rax
	.cfi_def_cfa_offset 16
	callq	free@PLT
	popq	%rax
	.cfi_def_cfa_offset 8
	retq
.Lfunc_end7:
	.size	freeInt, .Lfunc_end7-freeInt
	.cfi_endproc
                                        # -- End function
	.globl	freeDouble                      # -- Begin function freeDouble
	.p2align	4, 0x90
	.type	freeDouble,@function
freeDouble:                             # @freeDouble
	.cfi_startproc
# %bb.0:
	pushq	%rax
	.cfi_def_cfa_offset 16
	callq	free@PLT
	popq	%rax
	.cfi_def_cfa_offset 8
	retq
.Lfunc_end8:
	.size	freeDouble, .Lfunc_end8-freeDouble
	.cfi_endproc
                                        # -- End function
	.globl	Square                          # -- Begin function Square
	.p2align	4, 0x90
	.type	Square,@function
Square:                                 # @Square
	.cfi_startproc
# %bb.0:
	movsd	%xmm0, -8(%rsp)
	movsd	-8(%rsp), %xmm0                 # xmm0 = mem[0],zero
	mulsd	-8(%rsp), %xmm0
	retq
.Lfunc_end9:
	.size	Square, .Lfunc_end9-Square
	.cfi_endproc
                                        # -- End function
	.globl	CircleArea                      # -- Begin function CircleArea
	.p2align	4, 0x90
	.type	CircleArea,@function
CircleArea:                             # @CircleArea
	.cfi_startproc
# %bb.0:
	pushq	%rax
	.cfi_def_cfa_offset 16
	movsd	%xmm0, (%rsp)
	movsd	(%rsp), %xmm0                   # xmm0 = mem[0],zero
	callq	Square@PLT
	movq	PI@GOTPCREL(%rip), %rax
	mulsd	(%rax), %xmm0
	popq	%rax
	.cfi_def_cfa_offset 8
	retq
.Lfunc_end10:
	.size	CircleArea, .Lfunc_end10-CircleArea
	.cfi_endproc
                                        # -- End function
	.section	.rodata.cst8,"aM",@progbits,8
	.p2align	3                               # -- Begin function main
.LCPI11_0:
	.quad	0x4014000000000000              # double 5
	.text
	.globl	main
	.p2align	4, 0x90
	.type	main,@function
main:                                   # @main
	.cfi_startproc
# %bb.0:
	subq	$24, %rsp
	.cfi_def_cfa_offset 32
	movsd	.LCPI11_0(%rip), %xmm0          # xmm0 = mem[0],zero
	movsd	%xmm0, 16(%rsp)
	movsd	16(%rsp), %xmm0                 # xmm0 = mem[0],zero
	callq	CircleArea@PLT
	movsd	%xmm0, 8(%rsp)
	leaq	.L.str1(%rip), %rdi
	callq	print_string@PLT
	movsd	8(%rsp), %xmm0                  # xmm0 = mem[0],zero
	callq	print_double@PLT
	xorl	%eax, %eax
                                        # kill: def $rax killed $eax
	addq	$24, %rsp
	.cfi_def_cfa_offset 8
	retq
.Lfunc_end11:
	.size	main, .Lfunc_end11-main
	.cfi_endproc
                                        # -- End function
	.type	.Lint_format,@object            # @int_format
	.section	.rodata.str1.1,"aMS",@progbits,1
.Lint_format:
	.asciz	"%d\n"
	.size	.Lint_format, 4

	.type	.Ldouble_format,@object         # @double_format
.Ldouble_format:
	.asciz	"%f\n"
	.size	.Ldouble_format, 4

	.type	.Lstring_format,@object         # @string_format
.Lstring_format:
	.asciz	"%s\n"
	.size	.Lstring_format, 4

	.type	.L.str1,@object                 # @.str1
	.section	.rodata.str1.16,"aMS",@progbits,1
	.p2align	4
.L.str1:
	.asciz	"The are of a circle with 5 radius is:"
	.size	.L.str1, 38

	.type	PI,@object                      # @PI
	.data
	.globl	PI
	.p2align	3
PI:
	.quad	0x400921fb54442eea              # double 3.1415926535900001
	.size	PI, 8

	.section	".note.GNU-stack","",@progbits
	.addrsig
	.addrsig_sym printf
	.addrsig_sym malloc
	.addrsig_sym free
	.addrsig_sym print_double
	.addrsig_sym print_string
	.addrsig_sym Square
	.addrsig_sym CircleArea
	.addrsig_sym PI
