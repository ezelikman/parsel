decrypt(text, n): decrypt takes a string and an integer and returns a string that is the original string decrypted n times.
'This is a test!',0 -> 'This is a test!'
'hsi  etTi sats!',1 -> 'This is a test!'
's eT ashi tist!',2 -> 'This is a test!'
' Tah itse sits!',3 -> 'This is a test!'
'This is a test!',4 -> 'This is a test!'
'This is a test!',-1 -> 'This is a test!'
'hskt svr neetn!Ti aai eyitrsig',1 -> 'This kata is very interesting!'
'',0 -> ''
None,0 -> None
  decrypt_once(s): decrypt_once takes a string s and returns a string that is the result of taking the first half of s and appending it to the second half of s.
