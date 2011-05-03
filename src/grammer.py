'''
programme = "PROGRAMME", white space, identifier, white space,
            "BEGIN", white space,
            rules,
            "END";
identifier = alphabetic character , { alphabetic character | digit } ;
paper = digit, digit, digit, {".", digit|alphabetic character, [digit|alphabetic character, digit|alphabetic character]};
number = digit , { digit };
string = \'"\', { all characters - \'"\' }, \'"\';
alphabetic character = "A" | "B" | "C" | "D" | "E" | "F" | "G"
                     | "H" | "I" | "J" | "K" | "L" | "M" | "N"
                     | "O" | "P" | "Q" | "R" | "S" | "T" | "U"
                     | "V" | "W" | "X" | "Y" | "Z" ;
digit = "0" | "1" | "2" | "3" | "4" | "5" | "6" | "7" | "8" | "9" ;
white space = ? white space characters ? ;
all characters = ? all visible characters ? ;
rules = rule, {rule}
rule = "at", white space, "least"
     | "no", white space, "more", white space, "than"
     | "must", white space, "have",
     (number, "of", white space, "credits", white space, "at", number, white space, "level")|( 
'''
