
function object_autocomplete_constructor() {
	local title=$1
	local error_message=$2
	local command_option=$3

	string_values="$(triumphum $command_option)"
	eval "local -a values=($string_values)"
	if [ ${#values} -gt 0 ]; then
		_values  "${title}" $values
	else
		_message "${error_message}"
	fi
}

function _triumphum_run_games {
	object_autocomplete_constructor "Jeux disponibles"     "Aucun jeu ne semble être disponible"      "--ag"
}

function _triumphum_list_licences {
	object_autocomplete_constructor "Licences disponibles" "Aucune licence ne semble être disponible" "--al"
}

function _triumphum_list_platforms {
	object_autocomplete_constructor "Plateformes disponibles" "Aucune plateforme ne semble être disponible" "--ap"
}

function _triumphum_list_genres {
	object_autocomplete_constructor "Genres disponibles" "Aucun genre ne semble être disponible" "--at"
}

_triumphum_complete() {
_arguments \
  {-h,--help}'[show help options]' \
  --tui'[Run the game selection interface]' \
  {-r,--run}'[Run a given game and track playing time.]: :_triumphum_run_games' \
  {-a,--about}'[Show about message.]' \
  {-d,--donate}'[Open link to give a tip.]' \
  --no-splash'[Do not show splash at opening.]' \
  --list-games'[Afficher la liste des jeux.]' \
  --list-licences'[Afficher la liste des licences.]' \
  --list-genres'[Afficher la liste des genres de jeu.]' \
  --list-platforms'[Afficher la liste des genres des plateformes.]' \
  {-c,--config-file}'[Select different config file from default one.]' \
  {-g,--games}'[Select different game file from default one.]' \
  {-p,--platforms}'[Select different platform file from default one.]' \
  {-l,--licences}'[Select different licence file from default one.]' \
  {-t,--game-genres}'[Select different game genre file from default one.]' \
  --layout'[Utiliser des raccourcis dactyliques adaptés à la disposition de clavier.]' \
  --add-game'[Ajouter un nouveau jeu.]' \
  --add-licence'[Ajouter une nouvelle licence.]' \
  --add-genre'[Ajouter un nouveau genre de jeu.]' \
  --add-platform'[Ajouter une nouvelle plateforme.]' \
  --del-game'[Suprimer un jeu.]: :_triumphum_run_games' \
  --del-licence'[Suprimer une licence.]: :_triumphum_list_licences' \
  --del-genre'[Suprimer un genre de jeu.]: :_triumphum_list_genres' \
  --del-platform'[Suprimer une plateforme.]: :_triumphum_list_platforms' \
}

compdef _triumphum_complete triumphum
