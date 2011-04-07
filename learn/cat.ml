let echo chan =
  try 
    while true do print_endline (input_line chan) done
  with End_of_file -> ();;

let rec echo_files argv =
  match argv with h::t -> (echo (open_in h)) ; echo_files t | [] -> echo stdin;;

match (Array.to_list Sys.argv) with h::t -> echo_files t | [] -> echo stdin;;
