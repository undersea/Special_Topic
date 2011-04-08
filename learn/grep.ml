let pattern = match (Array.to_list Sys.argv) with h::t -> (match t with h::t -> Str.regexp h | [] -> Str.regexp "") | [] -> Str.regexp "";;


let files = match (Array.to_list Sys.argv) with 
  h::t -> (match t with 
    h::t -> t 
  | [] -> []) 
| [] -> [];;

let print_error err = print_endline "grep PATTERN [file1...file*]"

let process_line  line = try let _ = Str.search_forward pattern line 0 in print_endline line with Not_found -> ();;

let rec find_pattern chan = try process_line (input_line chan) ; find_pattern chan with End_of_file -> ();;

let rec parse_files files = match files with h::t -> print_endline "-------------"; print_endline h ; print_endline "-------------"; find_pattern (open_in h) ; parse_files t | [] -> ();;


let () = match files = [] with true -> print_error () | false -> parse_files files;;
