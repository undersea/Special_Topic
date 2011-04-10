#load "str.cma"




let pattern = match (Array.to_list Sys.argv) with 
  h::t -> (match t with 
    h::t -> Str.regexp h 
  | [] -> Str.regexp "") 
| [] -> Str.regexp "";;





let files = match (Array.to_list Sys.argv) with 
  h::t -> (match t with h::t -> t | [] -> []) 
| [] -> [];;




let print_error err = 
  print_endline "grep PATTERN [file1...file*]"




let process_line  line no = 
  try 
    let _ = Str.search_forward pattern line 0 in 
    print_endline (String.concat "" [string_of_int no; ": "; line])
  with Not_found -> ();;




let rec find_pattern chan line = 
  try
    process_line (input_line chan) line; 
    find_pattern chan (line + 1)
  with End_of_file -> ();;




let rec parse_files files = 
  match files with 
    h::t -> 
      print_endline "-------------"; 
      print_endline h ; 
      print_endline "-------------"; 
      (try find_pattern (open_in h) 0 with x -> print_endline "Error: No such file or directory" );
      parse_files t 
  | [] -> ();;





let () = match files = [] with 
  true -> print_error () 
| false -> parse_files files;;
