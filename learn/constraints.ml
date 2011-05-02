(* Takes a 9x9 Array of numbers from of -1.
 * For each array one number is randomly changed to a number from 0 to 9.
 * Each row and column must have all numbers from 0 to 9 with no repeats.
 * This is a contraints problem to see what I must do to solve this in OCaml.
 *)

Random.self_init ();;

let restrict_matrix = Array.make_matrix 9 9 (-1);;
let print_matrix matrix = Array.iter (function c -> Array.iter (function x -> print_int x; print_string "\t") c; print_endline "") matrix;;


let rec assign matrix line number pos = 
  if (List.exists (function t -> t.(pos) == number)(Array.to_list matrix)) then 
    let number = Random.int ((Array.length line)+1) 
    and pos = Random.int ((Array.length line)) in 
    assign matrix line number pos 
  else line.(pos) <- number

let init matrix = Array.iter (function c -> 
  let number = Random.int ((Array.length c)+1) 
  and pos = Random.int ((Array.length c)) in 
  assign matrix c number pos
  ) matrix;;

init restrict_matrix;;

print_matrix restrict_matrix;;
