let pattern = match (Array.to_list Sys.argv) with h::t -> (match t with h::t -> h | [] -> "") | [] -> "";;


let files = match (Array.to_list Sys.argv) with h::t -> (match t with h::t -> t | [] -> []) | [] -> [];;



(*let () = match (Array.to_list Sys.argv) with h::t -> print_endline h; ()
                                            | [] -> ();;*)


let print_error err = print_endline "grep PATTERN [file1...file*]"



let rec parse_file files = match files with h::t


let () = match pattern = "" with true -> print_error () | false -> ();;
