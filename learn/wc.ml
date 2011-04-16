type count = {
    mutable chars: int;
    mutable lines: int;
    mutable words: int;
  };;

let new_count () = {chars = 0; lines = 0; words = 0};;
let total = new_count ();;

let process io iw wc ->
  let c = input_char io in
  wc.chars <- wc.chars + 1;
  match c with
  | ' ' | '\t' -> 
      if iw then wc.words <- wc.words + 1 else ();
      process io false wc
  | '\n' ->
      if iw then wc.words <- wc.words + 1 else ();
      process io false wc
  | c ->
      process io true wc;;



