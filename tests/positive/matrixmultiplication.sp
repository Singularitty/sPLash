(* Matrix multiplication in sPLash *)

(* Function to get an element of a matrix *)
get_element: Int (matrix: [Int], row: Int, col: Int, num_cols: Int) {
  return matrix[row * num_cols + col];
}

(* Function to set an element of a matrix *)
set_element: Void (matrix: [Int], row: Int, col: Int, num_cols: Int, value: Int) {
    write_to_array(matrix, row * num_cols + col, value);
}

(* Function to multiply two matrices *)
multiply_matrices: Void (a: [Int], b: [Int], result: [Int], rows_a: Int, cols_a: Int, cols_b: Int, i: Int, j: Int, k: Int) {
  if i < rows_a {
    if j < cols_b {
      if k < cols_a {
        set_element(result, i, j, cols_b, get_element(result, i, j, cols_b) + get_element(a, i, k, cols_a) * get_element(b, k, j, cols_b));
        multiply_matrices(a, b, result, rows_a, cols_a, cols_b, i, j, k + 1);
      } else {
        multiply_matrices(a, b, result, rows_a, cols_a, cols_b, i, j + 1, 0);
      }
    } else {
      multiply_matrices(a, b, result, rows_a, cols_a, cols_b, i + 1, 0, 0);
    }
  }
}

main: Int () {
    (* Implementation not finished *)
    return 0;
}
