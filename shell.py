#######################################
#  kiran  >  shell.py
#  Created by Uygur Kiran on 2021/4/11.
#######################################

import kiran as k

#######################################
# MAINLOOP
#######################################
while True:
	text = str(input('kiran > '))

	## IF EMPTY INPUT
	if text.strip() == "": continue

	## SHELL EXIT
	if text == "exit" or text == "quit":
		print("---\n> bye")
		break

	## RUN
	result, error = k.run('<stdin>', text)

	## HANDLE RESULT
	if error: print(error.as_string())
	elif result:
		if len(result.elements) == 1:
			print(repr(result.elements[0]))
		else:
			print(repr(result))

