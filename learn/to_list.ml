let table = [|[|1;2;3|];[|4;5;6|]|];;

let rec to_list tablex n = if n = 0 then [] else List.append (to_list tablex (n-1)) (Array.to_list (Array.get tablex n));;
let n = Array.length table;;
let m = n - 1;;
to_list table m;;
