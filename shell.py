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
	if text == "exit":
		print("---\n> bye")
		break
	result, error = k.run('<stdin>', text)

	if error: print(error.as_string())
	else: print(result)
