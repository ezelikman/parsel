get_strings(city): get_strings takes a string and returns a string of the form "letter:number,letter:number,..." where letter is a letter in the string and number is the number of times that letter appears in the string.
'Chicago' -> 'c:**,h:*,i:*,a:*,g:*,o:*'
'Bangkok' -> 'b:*,a:*,n:*,g:*,k:**,o:*'
'Las Vegas' -> 'l:*,a:**,s:**,v:*,e:*,g:*'
'Llanfairpwllgwyngyllgogerychwyrndrobwllllantysiliogogogoch' -> 'l:***********,a:***,n:****,f:*,i:***,r:****,p:*,w:****,g:*******,y:*****,o:******,e:*,c:**,h:**,d:*,b:*,t:*,s:*'
  c(lista): c is a function that takes a list of numbers and returns a function that takes a number and returns a tuple of that number and the number of times it appears in the list.
  star(n): star(n) returns a string of n stars.
  remover(lista): remover takes a list of numbers and returns a list of the same numbers with duplicates removed.
