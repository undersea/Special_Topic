let () = match (Array.to_list Sys.argv) with h::t -> print_endline (match t with h::t -> h | [] -> "No pattern") | [] -> ();;

