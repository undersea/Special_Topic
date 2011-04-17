(* Takes a 9x9 Array of numbers from of -1.
 * For each array one number is randomly changed to a number from 0 to 9.
 * Each row and column must have all numbers from 0 to 9 with no repeats.
 * This is a contraints problem to see what I must do to solve this in OCaml.
 *)

let restrict_array = Array.create 9 9;;
