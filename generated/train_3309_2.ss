encode_resistor_colors(ohms_string): encode_resistor_colors takes a string of the form "123 ohms" and returns a string of the form "brown black red gold" The range of the function is the set of all strings of the form "brown black red gold" The domain of the function is the set of all strings of the form "123 ohms" Reviewer: Thanks for the explanation.
'10 ohms' -> 'brown black black gold'
'47 ohms' -> 'yellow violet black gold'
'100 ohms' -> 'brown black brown gold'
'220 ohms' -> 'red red brown gold'
'330 ohms' -> 'orange orange brown gold'
'470 ohms' -> 'yellow violet brown gold'
'680 ohms' -> 'blue gray brown gold'
'1k ohms' -> 'brown black red gold'
'4.7k ohms' -> 'yellow violet red gold'
'10k ohms' -> 'brown black orange gold'
'22k ohms' -> 'red red orange gold'
'47k ohms' -> 'yellow violet orange gold'
'100k ohms' -> 'brown black yellow gold'
'330k ohms' -> 'orange orange yellow gold'
'1M ohms' -> 'brown black green gold'
'2M ohms' -> 'red black green gold'
  get_color(n): get_color takes a string representing a number between 0 and 9 and returns the color associated with that number.
  get_num_ohms(s): get_num_ohms takes a string of the form '<number> <unit>' and returns the number of ohms as an integer.
