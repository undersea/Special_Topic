print_endline (String.concat " " (match (Array.to_list Sys.argv) with h::t -> t | [] -> []));;
