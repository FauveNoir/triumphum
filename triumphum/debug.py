########################################################################
# fonctions de test
########################################################################
from datetime import  datetime
import inspect

def tprint(content):
	# Éxactement la même chose que la fonction print mais utilisée lors des testes pour la retrouver vite avec un ctrl-f
	print(content)

def writeInTmp(text):
	# Écrit les  résultats des points d’arret dans un fichier lorsque la sortie standard est cachée
	stack = inspect.stack()
	current_function = stack[1].function  # 
	with open('/tmp/triumphum-output', 'a') as f:
		f.write(f"[{datetime.now()}] [{current_function}] {text} \n")

