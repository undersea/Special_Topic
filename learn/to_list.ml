open Format;;
open String;;

let table = [|[|1;2;3|];[|4;5;6|]|];;

let rec to_list tablex n = if n = 0 then [] else (to_list tablex (n-1)) @ (Array.to_list (Array.get tablex (n-1)));;
let rec int_list_to_string_list = function
  | [] -> []
  | l -> (string_of_int (match l with | h::t -> h | [] -> 0))::int_list_to_string_list (List.tl l);;
print_endline (String.concat " " (int_list_to_string_list (to_list table (Array.length table))));;
