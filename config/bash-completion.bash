_triumphum_complete() {
	local cur prev opts
	# Liste des options disponibles
	opts="-h --help --tui -r --run -a --about -d --donate --no-splash --list-games --list-licences --list-genres --list-platforms -c --config-file -g --games -p --platforms -l --licences -t --game-genres --layout --add-game --add-licence --add-genre --add-platform --del-game --del-licence --del-genre --del-platform"
	
	# Déterminer le mot courant
	cur="${COMP_WORDS[COMP_CWORD]}"
	prev="${COMP_WORDS[COMP_CWORD-1]}"

	# Si l'option courante est "--run" ou "--del-game", afficher les jeux
	if [[ "$prev" == "-r" || "$prev" == "--run" ]]; then
		COMPREPLY=( $(compgen -W "$( triumphum --ag | sed -E "s/\[[^]]*\]//g")" -- "$cur") )
		return 0
	fi
	
	# Si l'option courante est "--del-game", afficher les jeux à supprimer
	if [[ "$prev" == "--del-game" ]]; then
		COMPREPLY=( $(compgen -W "$( triumphum --ag | sed -E "s/\[[^]]*\]//g")" -- "$cur") )
		return 0
	fi

	# Si l'option courante est "--del-licence", afficher les licences
	if [[ "$prev" == "--del-licence" ]]; then
		COMPREPLY=( $(compgen -W "$( triumphum --al | sed -E "s/\[[^]]*\]//g")" -- "$cur") )
		return 0
	fi

	# Si l'option courante est "--del-genre", afficher les genres
	if [[ "$prev" == "--del-genre" ]]; then
		COMPREPLY=( $(compgen -W "$( triumphum --at | sed -E "s/\[[^]]*\]//g")" -- "$cur") )
		return 0
	fi

	# Si l'option courante est "--del-platform", afficher les plateformes
	if [[ "$prev" == "--del-platform" ]]; then
		COMPREPLY=( $(compgen -W "$( triumphum --ap | sed -E "s/\[[^]]*\]//g")" -- "$cur") )
		return 0
	fi

	# Si aucune option spécifique n'est trouvée, afficher toutes les options possibles
	COMPREPLY=( $(compgen -W "$opts" -- "$cur") )
}

complete -F _triumphum_complete triumphum
