#!/usr/bin/python3

import sys
MAXLENGHT=70

def fold_lines(input_file, output_file, max_length=MAXLENGHT, indent=' '):
	with open(input_file, 'r', encoding='utf-8') as f:
		lines = f.readlines()

	with open(output_file, 'w', encoding='utf-8') as f:
		for line in lines:
			line = line.rstrip()  # Supprimer les espaces de fin de ligne
			if line.startswith(' '):
				while len(line) > max_length:
					break_point = line.rfind(' ', 0, max_length)
					if break_point == -1:
						break_point = max_length  # Coupe brutalement si aucun espace trouvé
					f.write(line[:break_point] + '\n')
					line = indent + line[break_point:].lstrip()
			f.write(line + '\n')

if __name__ == "__main__":
	if len(sys.argv) != 3:
		print("Usage: python fold_lines.py <input_file> <output_file>")
	else:
		fold_lines(sys.argv[1], sys.argv[2])

