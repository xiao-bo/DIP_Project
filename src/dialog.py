

dialogContent=[
"hello welcome to XX, please smile",\
"your smile is good ",\
"explaing smile",\
"Do you want experience school? ",\
"school....",\
"bug hole will open",\
"Goodbye"
]##index from 0 to 6

class Dialog:
	def __init__(self):
		pass

	def load(self,index):
		text = dialogContent[index]
		return text