type count = {
    mutable chars: int;
    mutable lines: int;
    mutable words: int;
  };;

let new_count () = {chars = 0; lines = 0; words = 0};;
let total = new_count ();;

let rec process io iw wc =
  let c = input_char io in
  wc.chars <- wc.chars + 1;
  match c with
  | ' ' | '\t' -> 
      if iw then wc.words <- wc.words + 1 else ();
      process io false wc
  | '\n' ->
      wc.lines <- wc.lines + 1;
      if iw then wc.words <- wc.words + 1 else ();
      process io false wc
  | c ->
      process io true wc;;


let print_totals total name = 
  print_int total.lines;
  print_string " ";
  print_int total.words;
  print_string " ";
  print_int total.chars;
  print_string " ";
  print_endline name;;


let add_to_total total wc = 
  total.chars <- total.chars + wc.chars;
  total.lines <- total.lines + wc.lines;
  total.words <- total.words + wc.words;;

let rec process_files = function 
  | [] -> ()
  | h::t -> let wc = new_count () in let pd = open_in h in try process (pd) true wc with End_of_file -> close_in pd; print_totals wc h; add_to_total total wc; process_files t;;


let () = match Array.to_list Sys.argv with | h::t -> process_files t; print_totals total "total" | [] -> ();;
