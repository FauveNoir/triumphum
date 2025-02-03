
<h1>Triumphum</h1>
			<h2><a name="nom"></a><a href="#nom">NOM</a></h2>
			<p>
            <img src="./logo.svg" alt="Triumphum — gestionnaire de ludothèque en Python et NCurses pour GNU/Linux" />
			</p>
			<h2><a name="devise"></a><a href="#devise">DEVISE</a></h2>
			<p>LACRIMOSA·GAVDIVM·EST</p>
			<h2><a name="synopsis"></a><a href="#synopsis">SYNOPSIS</a></h2>
			<code><b class="constant">triumphum</b> [<span class="option">-h</span> | <span class="option">-a</span> | <span class="option">-d</span>]</code>

<code><b class="constant">triumphum</b> [<span class="option">--config-file</span> <var>FICHIER_CONF</var>] [<span class="option">--games</span> <var>FICHIER_JEUX</var>] [<span class="option">--platforms</span> <var>FICHIER_PLATEFORMES</var>] [<span class="option">--licences</span> <var>FICHIER_LICENCES</var>] [<span class="option">--genres</span> <var>FICHIERS_GENRES</var>] [<span class="option">-v</span>]
          [<span class="option">--tui</span>] [<span class="option">--no-splash</span>] [<span class="option">--layout</span> <var>LAYOUT</var>]</code>

<code><b class="constant">triumphum</b> [<span class="option">--config-file</span> <var>FICHIER_CONF</var>] [<span class="option">--games</span> <var>FICHIER_JEUX</var>] [<span class="option">--platforms</span> <var>FICHIER_PLATEFORMES</var>] [<span class="option">--licences</span> <var>FICHIER_LICENCES</var>] [<span class="option">--genres</span> <var>FICHIERS_GENRES</var>] [<span class="option">-v</span>]
          <span class="option">-r</span> <var>JEU</var></code>

<code><b class="constant">triumphum</b> [<span class="option">--config-file</span> <var>FICHIER_CONF</var>] [<span class="option">--games</span> <var>FICHIER_JEUX</var>] [<span class="option">--platforms</span> <var>FICHIER_PLATEFORMES</var>] [<span class="option">--licences</span> <var>FICHIER_LICENCES</var>] [<span class="option">--genres</span> <var>FICHIERS_GENRES</var>] [<span class="option">-v</span>]
          [<span class="option">--add-game</span> <var>DESCRIPTEUR_JEU</var> | <span class="option">--add-licence</span> <var>DESCRIPTEUR_LICENCE</var> | <span class="option">--add-genre</span> <var>DESCRIPTEUR_GENRE</var> | <span class="option">--add-platform</span> <var>DESCRIPTEUR_PLATEFORME</var> | <span class="option">--del-game</span> <var>JEU</var> | <span class="option">--del-licence</span> <var>LICENCE</var> | <span class="option">--del-genre</span> <var>GENRE</var> | <span class="option">--del-platform</span> <var>PLATEFORME</var>]</code>

<code><b class="constant">triumphum</b> [<span class="option">--config-file</span> <var>FICHIER_CONF</var>] [<span class="option">--games</span> <var>FICHIER_JEUX</var>] [<span class="option">--platforms</span> <var>FICHIER_PLATEFORMES</var>] [<span class="option">--licences</span> <var>FICHIER_LICENCES</var>] [<span class="option">--genres</span> <var>FICHIERS_GENRES</var>] [<span class="option">-v</span>]
          [<span class="option">--list-games</span> | <span class="option">--list-licences</span> | <span class="option">--list-genres</span> | <span class="option">--list-platforms</span>]</code>

<code><b class="constant">triumphum</b> [<span class="option">--config-file</span> <var>FICHIER_CONF</var>] [<span class="option">--games</span> <var>FICHIER_JEUX</var>] [<span class="option">--platforms</span> <var>FICHIER_PLATEFORMES</var>] [<span class="option">--licences</span> <var>FICHIER_LICENCES</var>] [<span class="option">--genres</span> <var>FICHIERS_GENRES</var>] [<span class="option">-v</span>]
          [<span class="option">--ag</span> | <span class="option">--al</span> | <span class="option">--at</span> | <span class="option">--ap</span>]</code>
			<h2><a name="description"></a><a href="#description">DESCRIPTION</a></h2>
			<p>
			Triumphum est un gestionnaire de collection de jeux pour GNU/Linux. Il permet d’avoir une liste des jeux disponibles (ou ayant été à un moment donné disponible), de les lancer, et aussi d’avoir un suivi du temps qui y a été consacré.<br />
			Lorsqu’il est ouvert avec l’option <b><a href="#option--tui" class="option">--tui</a></b> qui est le comportement par défaut, Triumphum présente l’interface en TUI où l’utilisateur peut interagir interactivement.
			</p>
			<h2><a name="terminologie"></a><a href="#terminologie">TERMINOLOGIE</a></h2>
			<p>
			Dans la suite, sera utilisé le terme « genre » pour désigner ce qui ailleurs est appelé « type » de jeu (stratégie, temps réel, tour par tour, etc). « Genre » a été préféré à « type » dans la nomenclature de Triumphum car ce dernier a été jugé trop ambigüe.
			</p>
			<h2><a name="options"></a><a href="#options">OPTIONS</a></h2>
			<h3><a name="options-aide"></a><a href="#options-aide">Aide</a></h3>
			<dl>
				<dt><a name="option--help"></a><a href="#option--help"><span class="option">-h</span>, <span class="option">--help</span></a></dt>
				<dd>Montre une aide succincte sur la ligne de commande</dd>
				<dt><a name="option--about"></a><a href="#option--about"><span class="option">-a</span>, <span class="option">--about</span></a></dt>
				<dd>Présente rapidement les informations sur la commande et son auteur</dd>
				<dt><a name="option--donate"></a><a href="#option--donate"><span class="option">-d</span>, <span class="option">--donate</span></a></dt>
				<dd>Ouvrir le lien de don sur le navigateur.</dd>
			</dl>
			<h3><a name="comportement-interface"></a><a href="#comportement-interface">Comportement de l’interface</a></h3>
			<dl>
				<dt><a name="option--tui"></a><a href="#option--tui" class="option">--tui</a></dt>
				<dd>Ouvre l’interface interactive en TUI. Ceci est le comportement par défaut.</dd>
				<dt><a name="option--run"></a><a href="#option--run"><span class="option">-r</span> <var>JEU</var>, <span class="option">--run</span> <var>JEU</var></a></dt>
				<dd>Lancer le jeu de code <var>JEU</var> en traquant le temps qui y est consacré par Triumphum.</dd>
			</dl>
			<h3><a name="options-generales"></a><a href="#options-generales">Options générales</a></h3>
			<dl>
				<dt><a name="option--verbose"></a><a href="#option--verbose"><span class="option">-v</span>, <span class="option">--verbose</span></a></dt>
				<dd>Mode verbeux. Donne des informations sur les configurations en cours.</dd>
				<dt><a name="option--no-splash"></a><a href="#option--no-splash"><span class="option">--no-splash</span></a></dt>
				<dd>N’imprime pas la bannière en art ASCII sur la sortie standard. Comportement par défaut.</dd>
				<dt><a name="option--list-games"></a><a href="#option--list-games"><span class="option">--list-games</span></a></dt>
				<dd>Afficher la liste détaillée des jeux.</dd>
				<dt><a name="option--list-licences"></a><a href="#option--list-licences"><span class="option">--list-licences</span></a></dt>
				<dd>Afficher la liste détaillée des licences.</dd>
				<dt><a name="option--list-genres"></a><a href="#option--list-genres"><span class="option">--list-genres</span></a></dt>
				<dd>Afficher la liste détaillée des genres de jeu.</dd>
				<dt><a name="option--list-platforms"></a><a href="#option--list-platforms"><span class="option">--list-platforms</span></a></dt>
				<dd>Afficher la liste détaillée des genres des plateformes.</dd>
			</dl>
			<h3><a name="options-configuration"></a><a href="#options-configuration">Options de configuration</a></h3>
			<dl>
				<dt><a name="option--config-file"></a><a href="#option--config-file"><span class="option">-c</span> <var>FICHIER_CONF</var>, <span class="option">--config-file</span> <var>FICHIER_CONF</var></a></dt>
				<dd>Utiliser comme fichier de configuration générale <var>FICHIER_CONF</var>, au lieux de celui par défaut. Voir la section  <b><a class="ref-to-h3" href="#triumphumrc">triumphumrc</a></b>. </dd>
				<dt><a name="option--games"></a><a href="#option--games"><span class="option">-g</span> <var>FICHIER_JEUX</var>, <span class="option">--games</span> <var>FICHIER_JEUX</var></a></dt>
				<dd>Utiliser comme fichier de description des jeux <var>FICHIER_JEUX</var>, au lieux de celui par défaut. Voir la section  <b><a class="ref-to-h3" href="#games.json">games.json</a></b>.</dd>
				<dt><a name="option--platforms"></a><a href="#option--platforms"><span class="option">-p</span> <var>FICHIER_PLATEFORMES</var>, <span class="option">--platforms</span> <var>FICHIER_PLATEFORMES</var></a></dt>
				<dd>Utiliser comme fichier de description des jeux <var>FICHIER_PLATEFORMES</var>, au lieux de celui par défaut. Voir la section  <b><a class="ref-to-h3" href="#listOfPlatforms.json">listOfPlatforms.json</a></b>.</dd>
				<dt><a name="option--licences"></a><a href="#option--licences"><span class="option">-l</span> <var>FICHIER_LICENCES</var>, <span class="option">--licences</span> <var>FICHIER_LICENCES</var></a></dt>
				<dd>Utiliser comme fichier de description des licence <var>FICHIER_LICENCES</var>, au lieux de celui par défaut. Voir la section  <b><a class="ref-to-h3" href="#listOfLicences.json">listOfLicences.json</a></b>.</dd>
				<dt><a name="option--genres"></a><a href="#option--genres"><span class="option">-t</span> <var>FICHIER_GENRES</var>, <span class="option">--genres</span> <var>FICHIER_GENRES</var></a></dt>
				<dd>Utiliser comme fichier de description des genres <var>FICHIER_GENRES</var>, au lieux de celui par défaut. Voir la section  <b><a class="ref-to-h3" href="#listOfGenres.json">listOfGenres.json</a></b></dd>
				<dt><a name="option--layout"></a><a href="#option--layout"><a name="option--layout"></a><span class="option">--layout</span> <var>DISPOSITION</var></a></dt>
				<dd>Utiliser des raccourcis dactyliques adaptés à la disposition de clavier <var>DISPOSITION</var>. Valeurs possibles : bepo, azerty, qwerty. Voir la section <b><a class="ref-to-h2" href="#attribution-des-touches">ATTRIBUTION DES TOUCHES</a></b> affin de modifier les associations par défaut.</dd>
			</dl>
			<h3><a name="ajoutDonee"></a><a href="#ajoutDonee">Ajout de donnée</a></h3>
			<dl>
				<dt><a name="option--add-game"></a><a href="#option--add-game"><span class="option">--add-game</span> <var>DESCRIPTEUR_JEU</var></a></dt>
				<dd>Ajouter un nouveau jeu. Voir la section <b><a class="ref-to-h3" class="ref-to-h3" href="#descripteurs-jeux">Descripteurs des jeux</a></b>.</dd>
				<dt><a name="option--add-licence"></a><a href="#option--add-licence"><span class="option">--add-licence</span> <var>LICENCE</var></a></dt>
				<dd>Ajouter une nouvelle licence. Voir la section <b><a class="ref-to-h3" href="#descripteurs-licence">Descripteurs des licences</a></b>.</dd>
				<dt><a name="option--add-genre"></a><a href="#option--add-genre"><span class="option">--add-genre</span> <var>GENRE</var></a></dt>
				<dd>Ajouter un nouveau genre de jeu. Voir la section <b><a class="ref-to-h3" href="#descripteurs-genres">Descripteurs des genres</a></b>.</dd>
				<dt><a name="option--add-platform"></a><a href="#option--add-platform"><span class="option">--add-platform</span> <var>PLATFORM</var></a></dt>
				<dd>Ajouter une nouvelle plateforme. Voir la section <b><a class="ref-to-h3" href="#descripteurs-plateformes">Descripteurs des plateforme</a></b>.</dd>
			</dl>
			<h3><a name="suppression-donnee"></a><a href="#suppression-donnee">Suppression de donnée</a></h3>
			<dl>
				<dt><a name="option--del-game"></a><a href="#option--del-game"><span class="option">--del-game</span> <var>JEU</var></a></dt>
				<dd>Supprimer un jeu.</dd>
				<dt><a name="option--del-licence"></a><a href="#option--del-licence"><span class="option">--del-licence</span> <var>LICENCE</var></a></dt>
				<dd>Supprimer une licence.</dd>
				<dt><a name="option--del-genre"></a><a href="#option--del-genre"><span class="option">--del-genre</span> <var>GENRE</var></a></dt>
				<dd>Supprimer un genre de jeu.</dd>
				<dt><a name="option--del-platform"></a><a href="#option--del-platform"><span class="option">--del-platform</span> <var>PLATEFORME</var></a></dt>
				<dd>Supprimer une plateforme.</dd>
			</dl>
			<h3><a name="commandes-auto-completion"></a><a href="#commandes-auto-completion">Commandes utiles à l’auto-complétion</a></h3>
			<dl>
				<dt><a name="option--ag"></a><a href="#option--ag"><span class="option">--ag</span></a></dt>
				<dd>Lister les codes des jeux.</dd>
				<dt><a name="option--al"></a><a href="#option--al"><span class="option">--al</span></a></dt>
				<dd>Lister les codes des licences.</dd>
				<dt><a name="option--at"></a><a href="#option--at"><span class="option">--at</span></a></dt>
				<dd>Lister les codes des genres de jeu.</dd>
				<dt><a name="option--ap"></a><a href="#option--ap"><span class="option">--ap</span></a></dt>
				<dd>Lister les codes des plateformes.</dd>
			</dl>
			<h2><a name="exemples-utiles"></a><a href="#exemples-utiles">EXEMPLES UTILES</a></h2>
			<dl>
				<dt><b class="constant">triumphum</b> <span class="option">--run</span> <var>JEU</var></dt>
				<dd>Lancer le jeu <var>JEU</var> depuis le shell tout en traquant le temps de jeu par Triumphum</dd>
				<dt><b class="constant">triumphum</b> <span class="option">--layout</span> bepo</dt>
				<dd>Ouvrir l’interface TUI de Triumphum avec des associations de touches adaptées à la disposition BÉPO.</dd>
			</dl>
			<h2><a name="interface-tui"></a><a href="#interface-tui">INTERFACE TUI</a></h2>
			<p>
			À l’ouverture, l’interface se présente sous la forme de quatre zones principales.
			</p>
			<div class="full-view">
			<pre>┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃Barre de titre                                                  ┃
┡━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩
│                                                                │
│                                                                │
│                                                                │
│                         Lite des jeux                          │
│                                                                │
│                                                                │
│                                                                │
│                                                                │
┢━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┪
┃Statu                                              Récapitulatif┃
┡━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩
│Zone de saisie de commande                                      │
└────────────────────────────────────────────────────────────────┘</pre>
			</div>
			<dl>
				<dt>Barre de titre</dt>
				<dd>Elle ne sert à rien sinon pour faire joli et présenter le nom du logiciel.</dd>
				<dt>Liste des jeux</dt>
				<dd>La liste des jeux à proprement parler qui est interactive.</dd>
				<dt>Barre de statu</dt>
				<dd>
					Elle même divisée en deux parties. À gauche sont présentées les messages affichés par Triumphum, et à droite un récapitulatif du temps cumulé de jeu de tous les jeux conofondus, sous la forme
					<div class="example">
						J: <var>&lt;jour&gt;</var>│S: <var>&lt;semaine&gt;</var>│M: <var>&lt;mois&gt;</var>│A: <var>&lt;année&gt;</var>
					</div>
					Où les valeurs associées à J, S, M, et A, correspondent respectivement au temps de jeu cumulé écoulé durant le jour, la semaine, le mois, et l’année.
				</dd>
				<dt>Zone de saisie de commande</dt>
				<dd>Lieu où s’affiche les commandes du shell interne saisies par l’utilisateur.</dd>
			</dl>
			<p>
			Au sein de l’interface TUI, il est possible d’interagir avec au travers des différentes actions qui s’actionnent par les touches dédiées dans la section <b><a class="ref-to-h2" href="#bindings">BINDINGS</a></b>.
			</p>
			<h2><a name="bindings"></a><a href="#bindings">BINDINGS</a></h2>
			<dl>
				<dt> t</dt>
				<dd>Aller vers l’élément au dessous</dd>
				<dt> s</dt>
				<dd>Aller vers l’élément au dessus</dd>
				<dt> Enter</dt>
				<dd>Lancer le jeu ayant le focus</dd>
				<dt> e</dt>
				<dd>Éditer le jeu ayant le focus (expérimental)</dd>
				<dt> a</dt>
				<dd>Ouvrir le lien associé au jeu ayant le focus</dd>
				<dt> y</dt>
				<dd>Copier le lien associé au jeu dans le presse-papier</dd>
				<dt> c</dt>
				<dd>Ajouter un commentaire au jeu (expérimental)</dd>
				<dt> b</dt>
				<dd>Trier la liste des jeux par ordre alphabétique des titres</dd>
				<dt> é</dt>
				<dd>Trier la liste des jeux par permissivité des licences</dd>
				<dt> p</dt>
				<dd>Trier la liste des jeux par ordre alphabétique des genres</dd>
				<dt> o</dt>
				<dd>Trier la liste des jeux par date de sortie</dd>
				<dt> è</dt>
				<dd>Trier la liste des jeux par date de dernière ouverture</dd>
				<dt> v</dt>
				<dd>Trier la liste des jeux par durée de jeu cumulée</dd>
				<dt> P</dt>
				<dd>Trier la liste des jeux par ordre alphabétique des noms de plateformes</dd>
				<dt> L</dt>
				<dd>Rafraichir la liste</dd>
				<dt> l</dt>
				<dd>Montrer la licence du jeu ayant le focus</dd>
				<dt> x</dt>
				<dd>Faire un don (ouvre le lien de don dans le navigateur)</dd>
				<dt> q</dt>
				<dd>Quitter le jeu</dd>
				<dt> /</dt>
				<dd>Filtrer selon le motif (expérimental)</dd>
				<dt> h</dt>
				<dd>Afficher l’aide</dd>
			</dl>
			<h2><a name="descripteurs"></a><a href="#descripteurs">DESCRIPTEURS</a></h2>
			<p>
			Les descripteurs des objets (jeux, licences, plateformes, genre), permettent d’ajouter de nouveaux objets à ceux gérés par Triumphum. Ils se présentent simplement sous la forme d’une suite de clés-valeurs, où les clés, dépendent de chaque type, et où certaines sont obligatoires pour certains types d’objets.
			</p>
			<h3><a name="descripteurs-jeux"></a><a href="#descripteurs-jeux">Descripteurs des jeux</a></h3>
			<dl>
				<dt>name</dt>
				<dd>Nom littéral du jeu. (Obligatoire)</dd>
				<dt>code</dt>
				<dd>Code à travers lequel le jeu sera traité et identifié par Triumphum. (Obligatoire)</dd>
				<dt>command</dt>
				<dd>Commande d’exécution du jeu. (Obligatoire)</dd>
				<dt>genre</dt>
				<dd>code du genre attribué au jeu.</dd>
				<dt>licence</dt>
				<dd>Code de la licence attribuée au jeu.</dd>
				<dt>url</dt>
				<dd>Lien du jeu.</dd>
				<dt>studios</dt>
				<dd>Noms du ou des studios ayant développé le jeu. Plusieurs studios ont leur noms séparés par une virgule.</dd>
				<dt>authors</dt>
				<dd>Noms du ou des auteurs ayant développé le jeu. Plusieurs auteurs ont leur noms séparés par une virgule.</dd>
				<dt>shortDesc</dt>
				<dd>Courte description du jeu.</dd>
				<dt>year</dt>
				<dd>Année de sortie du jeu.</dd>
				<dt>Exemple</dt>
				<dd><code><span class="Label">name</span>=<span class="String">"0 A. D."</span> <span class="Label">code</span>=<span class="String">0ad</span> <span class="Label">command</span>=<span class="String">0ad-pyrogenesis</span> <span class="Label">genre</span>=<span class="String">rts</span> <span class="Label">licence</span>=<span class="String">gpl</span> <span class="Label">url</span>=<span class="String">https://play0ad.com</span> <span class="Label">studios</span>=<span class="String">"Wildfire Games"</span> <span class="Label">authors</span>=<span class="String">Stanislas\ Dolcini</span> <span class="Label">shortdesc</span>=<span class="String">"RTS libre historique en 3D où s’affrontent diverses civilisations antiques."</span> <span class="Label">year</span>=2010</code></dd>
			</dl>
			<h3><a name="descripteurs-licence"></a><a href="#descripteurs-licences">Descripteurs des licences</a></h3>
			<dl>
				<dt>name</dt>
				<dd>Nom littéral de la licence. (Obligatoire)</dd>
				<dt>code (Obligatoire)</dt>
				<dd>Code à travers lequel la licence sera traitée et identifié par Triumphum. (Obligatoire)</dd>
				<dt>abbr</dt>
				<dd>Abréviation sous laquelle apparaitra le nom de la licence dans les situations qui l’exigent.</dd>
				<dt>url</dt>
				<dd>Lien de la licence.</dd>
				<dt>freedomCoefficient</dt>
				<dd>Coefficient de liberté de la licence de 0 à 1, où 1 représente la licence la plus permissive (par exemple domaine public ou LPRAB) et 0 la licence la moins permissive.</dd>
				<dt>shortDesc</dt>
				<dd>Courte description de la licence.</dd>
				<dt>Exemple</dt>
				<dd><span class="Label">name</span>=<span class="String">"Licence Art Libre"</span> <span class="Label">code</span>=<span class="String">lal</span> <span class="Label">abbr</span>=<span class="String">LAL</span> <span class="Label">url</span>=<span class="String">https://artlibre.org</span> <span class="Label">freedomCoefficient</span>=<span class="String">0.5</span> <span class="Label">shortDesc</span>=<span class="String">"La licence LAL (Licence Art Libre) permet la libre utilisation, modification et redistribution des œuvres, tant que la même liberté est préservée dans les œuvres dérivées."</span></dd>
			</dl>
			<h3><a name="descripteurs-plateformes"></a><a href="#descripteurs-plateformes">Descripteurs des plateformes</a></h3>
			<dl>
				<dt>name</dt>
				<dd>Nom littéral de la plateforme. (Obligatoire)</dd>
				<dt>code</dt>
				<dd>Code à travers lequel la plateforme sera traitée et identifiée par Triumphum. (Obligatoire)</dd>
				<dt>abbr</dt>
				<dd>Abréviation sous laquelle apparaitra le nom de la plateforme dans les situations qui l’exigent.</dd>
				<dt>Exemple</dt>
				<dd><span class="Label">name</span>=<span class="String">Linux</span> <span class="Label">code</span>=<span class="String">linux</span> <span class="Label">abbr</span>=<span class="String">LIN</span></dd>
			</dl>
			<h3><a name="descripteurs-genres"></a><a href="#descripteurs-genres">Descripteurs des genres</a></h3>
			<dl>
				<dt>name</dt>
				<dd>Nom littéral du genre. (Obligatoire)</dd>
				<dt>code</dt>
				<dd>Code à travers lequel le genre sera traité et identifié par Triumphum. (Obligatoire)</dd>
				<dt>abbr</dt>
				<dd>Abréviation sous laquelle apparaitra le nom du genre dans les situations qui l’exigent.</dd>
				<dt>Exemple</dt>
				<dd><span class="Label">name</span>=<span class="String">"Jeu de rôle en ligne massivement multijoueur"</span> <span class="Label">code</span>=<span class="String">mmorpg</span> <span class="Label">abbr</span>=<span class="String">MMORPG</span></dd>
			</dl>
			<h2><a name="fichiers-configuration"></a><a href="#fichiers-configuration">FICHIERS DE CONFIGURATION</a></h2>
			<h3><a name="triumphumrc"></a><a href="#triumphumrc">triumphumrc</a></h3>
			<p>
			Principal fichier de configuration portant essentiellement sur les raccourcis claviers et les éléments graphiques de l’interface TUI.
			</p>
			<p>
			Il est possible d’y configurer essentiellement deux aspects. D’une part les associations de touches, pour cela voir la section <b><a class="ref-to-h2" href="#attribution-des-touches">ATTRIBUTION DES TOUCHES</a></b> ; et d’autre part les éléments graphiques apparaissant sur l’interface, pour cela voir la section <b><a class="ref-to-h2" href="#elements-graphiques">ÉLÉMENTS GRAPHIQUES DE L’INTERFACE.</a></b>
			</p>
			<h3><a name="games.json"></a><a href="#games.json">games.json</a></h3>
			<p>
			Fichier de configuration des jeux tels qu’ils apprissent dans la liste principale.
			Il se présente sous la forme d’une liste JSON, où chaque entrée est un dictionnaire JSON représentant un jeu. 
			</p>
			<p>
			Dans chaque dictionnaire les clés sont les mêmes que celles du descripteur dans la section <b><a class="ref-to-h3" href="#descripteurs-jeux">Descripteurs des jeux</a></b>.
			Toute fois, les clés authors et studios sont sensées recevoir des listes en valeurs, même si elles ne doivent contenir qu’une seule valeur.
			</p>
			<dl>
				<dt>Exemple</dt>
				<dd>
					<pre><span class="Delimiter">{</span>
        &quot;<span class="Label">games</span>&quot;: <span class="Delimiter">[</span>
                <span class="Delimiter">{</span>
                        &quot;<span class="Label">name</span>&quot;: &quot;<span class="String">0 A. D.</span>&quot;,
                        &quot;<span class="Label">licence</span>&quot;: &quot;<span class="String">gpl</span>&quot;,
                        &quot;<span class="Label">year</span>&quot;: <span class="Number">2021</span>,
                        &quot;<span class="Label">genre</span>&quot;: &quot;<span class="String">rts</span>&quot;,
                        &quot;<span class="Label">command</span>&quot;: &quot;<span class="String">0ad</span>&quot;,
                        &quot;<span class="Label">code</span>&quot;: &quot;<span class="String">0ad</span>&quot;,
                        &quot;<span class="Label">url</span>&quot;: &quot;<span class="String"><a href="https://play0ad.com/">https://play0ad.com/</a></span>&quot;,
                        &quot;<span class="Label">platform</span>&quot;: &quot;<span class="String">linux</span>&quot;,
                        &quot;<span class="Label">studios</span>&quot;: <span class="Delimiter">[</span>
                                &quot;<span class="String">Wildfire Games</span>&quot;
                        <span class="Delimiter">]</span>,
                        &quot;<span class="Label">authors</span>&quot;: <span class="Delimiter">[</span>
                                &quot;<span class="String">Stanislas Dolcini</span>&quot;
                        <span class="Delimiter">]</span>,
                        &quot;<span class="Label">shortDesc</span>&quot;: &quot;<span class="String">RTS libre historique en 3D où s’affrontent diverses civilisations antiques.</span>&quot;
                <span class="Delimiter">}</span>,
                …
        <span class="Delimiter">]</span>
<span class="Delimiter">}</span></pre>
				</dd>
			</dl>
			<h3><a name="listOfGenres.json"></a><a href="#listOfGenres.json">listOfGenres.json</a></h3>
			<p>
			Fichier contenant les définitions des genres reconnus par Triumphum.<br />
			Il se présente sous la forme d’une liste JSON, où chaque entrée est un dictionnaire JSON représentant un genre. 
			</p>
			<p>
			Dans chaque dictionnaire les clés sont les mêmes que celles du descripteur dans la section <b><a class="ref-to-h3" href="#descripteurs-genres">Descripteurs des genres</a></b>.
			</p>
			<dl>
				<dt>Exemple</dt>
				<dd>
					<pre><span class="Delimiter">{</span>
        &quot;<span class="Label">genres</span>&quot;: <span class="Delimiter">[</span>
                <span class="Delimiter">{</span>
                        &quot;<span class="Label">name</span>&quot;: &quot;<span class="String">Action</span>&quot;,
                        &quot;<span class="Label">abbr</span>&quot;: &quot;<span class="String">Act</span>&quot;,
                        &quot;<span class="Label">code</span>&quot;: &quot;<span class="String">action</span>&quot;
                <span class="Delimiter">}</span>,
                …
        <span class="Delimiter">]</span>
<span class="Delimiter">}</span></pre>
				</dd>
			</dl>
			<h3><a name="listOfLicences.json"></a><a href="#listOfLicences.json">listOfLicences.json</a></h3>
			<p>
			Fichier contenant les définitions des licence reconnues par Triumphum.
			Il se présente sous la forme d’une liste JSON, où chaque entrée est un dictionnaire JSON représentant une Licence. 
			</p>
			<p>
			Dans chaque dictionnaire les clés sont les mêmes que celles du descripteur dans la section <b><a class="ref-to-h3" href="#descripteurs-licence">Descripteurs des licences</a></b>.
			</p>
			<dl>
				<dt>Exemple</dt>
				<dd>
					<pre><span class="Delimiter">{</span>
        &quot;<span class="Label">licences</span>&quot;: <span class="Delimiter">[</span>
                <span class="Delimiter">{</span>
                        &quot;<span class="Label">name</span>&quot;: &quot;<span class="String">GNU General Public License</span>&quot;,
                        &quot;<span class="Label">abbr</span>&quot;: &quot;<span class="String">GPL</span>&quot;,
                        &quot;<span class="Label">code</span>&quot;: &quot;<span class="String">gpl</span>&quot;,
                        &quot;<span class="Label">url</span>&quot;: &quot;<span class="String"><a href="https://www.gnu.org/licenses/gpl-3.0.html">https://www.gnu.org/licenses/gpl-3.0.html</a></span>&quot;,
                        &quot;<span class="Label">shortText</span>&quot;: &quot;<span class="String">La licence publique générale GNU est une licence de logiciel libre adoptée par la Free Software Foundation (FSF) pour le projet GNU.</span>&quot;,
                        &quot;<span class="Label">freedomCoefficient</span>&quot;: <span class="Number">0.8</span>
                <span class="Delimiter">}</span>,
                …
        <span class="Delimiter">]</span>
<span class="Delimiter">}</span></pre>
				</dd>
			</dl>
			<h3><a name="listOfPlatforms.json"></a><a href="#listOfPlatforms.json">listOfPlatforms.json</a></h3>
			<p>
			Fichier contenant les plateformes des licence reconnues par Triumphum.<br />
			Il se présente sous la forme d’une liste JSON, où chaque entrée est un dictionnaire JSON représentant une plateforme. 
			</p>
			<p>
			Dans chaque dictionnaire les clés sont les mêmes que celles du descripteur dans la section <b><a class="ref-to-h3" href="#descripteurs-plateformes">Descripteurs des plateformes</a></b>.
			</p>
			<dl>
				<dt>Exemple</dt>
				<dd>
					<pre><span class="Delimiter">{</span>
        &quot;<span class="Label">platforms</span>&quot;:
        <span class="Delimiter">[</span>
                <span class="Delimiter">{</span>
                        &quot;<span class="Label">name</span>&quot;: &quot;<span class="String">Linux</span>&quot;,
                        &quot;<span class="Label">code</span>&quot;: &quot;<span class="String">linux</span>&quot;,
                        &quot;<span class="Label">abbr</span>&quot;: &quot;<span class="String">LIN</span>&quot;
                <span class="Delimiter">}</span>,
                …
        <span class="Delimiter">]</span>
<span class="Delimiter">}</span></pre>
				</dd>
			</dl>
			<h3><a name="history.json"></a><a href="#history.json">history.json</a></h3>
			<p>
			Historique des parties jouées, avec heure de début, de fin, et temps de jeu.<br />
			Il se présente sous la forme d’une liste JSON où chaque entrée représente un jeu représenté par le code du dit jeu en tant que clé de l’entrée.
			</p>
			<p>
			En suite, à chaque entrée de jeu est associée comme valeur une liste où chaque entrée représente une session de jeu définie par les trois propriétés :
			</p>
			<dl>
				<dt>start_time</dt>
				<dd>Début de la session de jeu au format ISO. Exemple : 2024-04-20T18:36:35.</dd>
				<dt>end_time</dt>
				<dd>Fin de la session de jeu au format ISO. Exemple : 2024-04-20T18:36:40.</dd>
				<dt>duration</dt>
				<dd>Durée totale de la session, au format ISO. Exemple : 0:00:04.959013.</dd>
				<dl>Exemple d’historique pour un jeu</dl>
				<dd>
					<pre>&quot;<span class="Label">0ad</span>&quot;: <span class="Delimiter">[</span>
        <span class="Delimiter">{</span>
                &quot;<span class="Label">start_time</span>&quot;: &quot;<span class="String">2024-04-20T17:40:22</span>&quot;,
                &quot;<span class="Label">end_time</span>&quot;: &quot;<span class="String">2024-04-20T17:40:27</span>&quot;,
                &quot;<span class="Label">duration</span>&quot;: &quot;<span class="String">0:00:04.967317</span>&quot;
        <span class="Delimiter">}</span>,
        <span class="Delimiter">{</span>
                &quot;<span class="Label">start_time</span>&quot;: &quot;<span class="String">2024-04-20T18:07:47</span>&quot;,
                &quot;<span class="Label">end_time</span>&quot;: &quot;<span class="String">2024-04-20T18:07:51</span>&quot;,
                &quot;<span class="Label">duration</span>&quot;: &quot;<span class="String">0:00:03.419640</span>&quot;
        <span class="Delimiter">}</span>,
        <span class="Delimiter">{</span>
                &quot;<span class="Label">start_time</span>&quot;: &quot;<span class="String">2024-04-21T16:13:58</span>&quot;,
                &quot;<span class="Label">end_time</span>&quot;: &quot;<span class="String">2024-04-21T16:14:02</span>&quot;,
                &quot;<span class="Label">duration</span>&quot;: &quot;<span class="String">0:00:03.594571</span>&quot;
        <span class="Delimiter">}</span>,
        <span class="Delimiter">{</span>
                &quot;<span class="Label">start_time</span>&quot;: &quot;<span class="String">2024-04-21T17:10:58</span>&quot;,
                &quot;<span class="Label">end_time</span>&quot;: &quot;<span class="String">2024-04-21T17:11:02</span>&quot;,
                &quot;<span class="Label">duration</span>&quot;: &quot;<span class="String">0:00:03.840515</span>&quot;
        <span class="Delimiter">}</span>
<span class="Delimiter">]</span></pre><dd>
			</dl>
			<h2><a name="attribution-des-touches"></a><a href="#attribution-des-touches">ATTRIBUTION DES TOUCHES</a></h2>
			<p>
			Par défaut, le mécanisme général prévoit d’utiliser la carte d’association définie par la disposition choisie avec <b><a class="option" href="#option--layout">--layout</a></b>.
			Toutefois, il es possible de redéfinir de nouvelles associations de touches à travers le fichier <b><a href="#triumphumrc">triumphumrc</a></b> en associant la clé d’une action donnée à la touche voulue, sous la forme :
			</p>
			<div class="example">
				<var>&lt;clé&gt;</var>=<var>&lt;touche&gt;</var>
			</div>
			<p>
			Et ce où <var>&lt;clé&gt;</var> est l’une des valeurs de  <b><a href="#liste-bindings">Liste des bindings de touches</a></b> et où <var><touche></var> répond aux exigences de <b><a href="#codes-touches">Codes des touches</a></b>.
			</p>
			<h3><a name="liste-bindings"></a><a href="#liste-bindings">Liste des bindings de touches</a></h3>
			<dl>
				<dt>bind_down</dt>
				<dd>Aller vers l’élément au dessous (Défaut : t)</dd>
				<dt>bind_up</dt>
				<dd>Aller vers l’élément au dessus (Défaut : s)</dd>
				<dt>bind_play</dt>
				<dd>Lancer le jeu ayant le focus (Défaut : Enter)</dd>
				<dt>bind_edit</dt>
				<dd>Éditer le jeu ayant le focus (expérimental) (Défaut : e)</dd>
				<dt>bind_open_link</dt>
				<dd>Ouvrir le lien associé au jeu ayant le focus (Défaut : a)</dd>
				<dt>bind_copy_link</dt>
				<dd>Copier le lien associé au jeu dans le presse-papier (Défaut : y)</dd>
				<dt>bind_comment</dt>
				<dd>Ajouter un commentaire au jeu (expérimental) (Défaut : c)</dd>
				<dt>bind_sort_title</dt>
				<dd>Trier la liste des jeux par ordre alphabétique des titres (Défaut : b)</dd>
				<dt>bind_sort_licence</dt>
				<dd>Trier la liste des jeux par permissivité des licences (Défaut : é)</dd>
				<dt>bind_sort_game_genre</dt>
				<dd>Trier la liste des jeux par ordre alphabétique des genres (Défaut : p)</dd>
				<dt>bind_sort_year</dt>
				<dd>Trier la liste des jeux par date de sortie (Défaut : o)</dd>
				<dt>bind_sort_last_opening</dt>
				<dd>Trier la liste des jeux par date de dernière ouverture (Défaut : è)</dd>
				<dt>bind_sort_playing_duration</dt>
				<dd>Trier la liste des jeux par durée de jeu cumulée (Défaut : v)</dd>
				<dt>bind_sort_playing_platform</dt>
				<dd>Trier la liste des jeux par ordre alphabétique des noms de plateformes (Défaut : P)</dd>
				<dt>bind_refresh</dt>
				<dd>Rafraichir la liste (Défaut : L)</dd>
				<dt>bind_show_licence</dt>
				<dd>Montrer la licence du jeu ayant le focus (Défaut : l)</dd>
				<dt>bind_donate</dt>
				<dd>Faire un don (ouvre le lien de don dans le navigateur) (Défaut : x)</dd>
				<dt>bind_quit</dt>
				<dd>Quitter le jeu (Défaut : q)</dd>
				<dt>bind_filter</dt>
				<dd>Filtrer selon le motif (expérimental) (Défaut : /)</dd>
				<dt>bind_help</dt>
				<dd>Afficher l’aide (Défaut : h)</dd>
			</dl>
			<h3><a name="codes-touches"></a><a href="#codes-touches">Codes des touches</a></h3>
			<p>
			De façon générale, toutes les touches sont représentées par la lettre qui leur est associée. Ainsi le code pour la touche A est A. Toutefois le mécanisme est sensible à la casse.
			</p>
			<p>
			À cela, s’ajoute les cas particuliers suivants
			</p>
			<dl>
				<dt>Enter</dt>
				<dd>Touche entrée</dd>
				<dt>Space</dt>
				<dd>Touche espace</dd>
				<dt>Return</dt>
				<dd>Touche de retour</dd>
			</dl>
			<h2><a name="elements-graphiques"></a><a href="#elements-graphiques">ÉLÉMENTS GRAPHIQUES DE L’INTERFACE</a></h2>
			<p>
			Dans le  <b><a href="#triumphumrc">triumphumrc</a></b>, il est possible de changer divers symboles apparaissant sur l’interface TUI en associant la clé du dit symbole au nouveau symbole voulu, sous la forme :
			</p>
			<div class="example">
				<var>&lt;clé&gt;</var>=<var>&lt;symbole&gt;</var>
			</div>
			<p>
			Et ce où <var>&lt;clé&gt;</var> est l’une des valeurs ci-dessous
			et où <var>&lt;symbole&gt;</var> est une chaine de caractères.
			</p>
			<h3><a name="elements-liste"></a><a href="#elements-liste">Éléments de la liste</a></h3>
			<dl>
				<dt>general_void_symbol</dt>
				<dd>Symbole par défaut remplaçant toutes les valeurs manquantes de la liste (Défault : -)</dd>
				<dt>name_void_symbol</dt>
				<dd>Symbole remplaçant les noms de jeu manquants sur la liste (Défault : -)</dd>
				<dt>platform_void_symbol</dt>
				<dd>Symbole remplaçant les plateformes manquantes sur la liste (Défault : -)</dd>
				<dt>licence_void_symbol</dt>
				<dd>Symbole remplaçant les licences manquantes sur la liste (Défault : -)</dd>
				<dt>type_void_symbol</dt>
				<dd>Symbole remplaçant les types manquants sur la liste (Défault : -)</dd>
				<dt>date_void_symbol</dt>
				<dd>Symbole remplaçant les dates de sorties manquantes sur la liste (Défault : -)</dd>
				<dt>lastopening_void_symbol</dt>
				<dd>Symbole remplaçant les dates de dernière ouverture manquantes sur la liste (Défault : -)</dd>
				<dt>cumulatedtime_void_symbol</dt>
				<dd>Symbole remplaçant les temps totaux manquants sur la liste (Défault : -)</dd>
				<dt>author_void_symbol</dt>
				<dd>Symbole remplaçant les auteurs manquants sur la liste (Défault : -)</dd>
				<dt>studio_void_symbol</dt>
				<dd>Symbole remplaçant les studios manquants sur la liste (Défault : -)</dd>
			</dl>
			<h3><a name="elements-recapitulatif"></a><a href="#elements-recapitulatif">Éléments du récapitulatif</a></h3>
			<dl>
				<dt>cumulated_time_played_per_day</dt>
				<dd>Symbole antécédent au temps de jeu cumulé par jour (Défault : J)</dd>
				<dt>cumulated_time_played_per_week</dt>
				<dd>Symbole antécédent au temps de jeu cumulé par semaine (Défault : S)</dd>
				<dt>cumulated_time_played_per_month</dt>
				<dd>Symbole antécédent au temps de jeu cumulé par mois (Défault : M)</dd>
				<dt>cumulated_time_played_per_year</dt>
				<dd>Symbole antécédent au temps de jeu cumulé par année (Défault : A)</dd>
				<dt>cumulated_time_played_separator</dt>
				<dd>Séparateur entre les temps de jeux cumulés par périodes (Défault : │)</dd>
			</dl>
			<h2><a name="installation"></a><a href="#installation">INSTALLATION</a></h2>
			<h3><a name="installation-debian"></a><a href="#installation-debian">Debian, Ubuntu, et debianides</a></h3>
			<p>
			<pre>curl <span class="option">--location</span> <a class="link" href="https://github.com/FauveNoir/triumphum/raw/main/triumphum.deb">https://github.com/FauveNoir/triumphum/raw/main/triumphum.deb</a> | sudo dpkg <span class="option">--install</span> -
sudo apt-get install <span class="option">--fix-broken</span> <span class="option">--assume-yes</span>
			</pre>
			</p>
			<h2><a name="extraloquence"></a><a href="#extraloquence">EXTRALOQUENCE</a></h2>
			<p>
			Cette section regroupe les propos additionnels ainsi que les réflexions connexes.
			</p>
			<h3><a name="histoire"></a><a href="#histoire">Histoire</a></h3>
			<h4><a name="histoire-2024-07-25"></a><a href="#histoire-2024-07-25">2024-07-25</a></h4>
			<p>
			L’idée originelle de ce logiciel provint de deux courroies. La première fût que j’avais dans mes moments creux besoins d’une réponse à la question « À quoi puis-je jouer en ce moment ? ». Bien entendu, sur la plus part des systèmes GNU/Linux, l’on peut lister le contenu de <var>/usr/games</var>, mais enfin, quiconque l’a inspecté au moins une fois s’est rendu compte qu’il ne répond pas vraiment à cette question. Car d’une part il peut contenir aussi bien des émulateurs, des éditeurs de cartes de jeu, ou tout logiciel ayant trait aux jeux sans être un jeu lui même ; et parce que d’autre part, il ne liste évidement pas des jeux que l’utilisateur aurait configuré sur des émulateurs, voir même des jeux qui ne se jouent qu’à travers le web.
			</p>
			<p>
			La deuxième courroie était le fait que je rencontrais une amie, elle même joueuse invétérée, qui profitait de tous ses congés pour s’adonner aux jeux sortis dans l’année auxquels elle n’avait pas pu consacré du temps. Et il se trouvait qu’elle maintenait un long tableur de bureautique contenant environ cent-trente jeu. Et avec le zèle d’une bonne élève, elle commentait méticuleusement dans une colonne dédiée ce qu’elle avait pensé de chaque jeu. C’est pourquoi il est prévu dans la raison d’être de Triumphum d’intégrer la possibilité de tenir un historique de commentaires qui refléteront l’évolution de l’utilisateur de ses réflexions concernant chaque jeu. Aussi cette fonctionnalité ne saurait tarder à venir dans de prochaines versions.
			</p>
			<p>
			Il s’est alors trouvé que de la conjonction de ces deux facteurs, l’idée de Triumphum s’imposa presque aussitot comme une évidence.
			</p>
			<h4><a name="histoire-2024-08-13"></a><a href="#histoire-2024-08-13">2024-08-13</a></h4>
			<p>
			Après la première publication de Triumphum, je recontactais cette amie pour lui faire part de la chose. Elle en fut amusée, et répondit :
			</p>
			<blockquote>
				Trop cool !<br />
				« un long tableur de bureautique contenant environ cent-trente jeu »<br />
				Comme c'est mignon 😂<br />
				Si c'est de moi que tu parles c'est un peu plus 😆
			</blockquote>
			<p>
			Et de me montrer sa liste qui désormais en contenait plus d’un millier.
			</p>
			<p>
			À cela je répondit que non seulement son besoin m’avait inspiré Triumphum, mais qu’avec le nombre de jeu elle avait plus que jamais besoin de cet utilitaire. Ce à quoi elle répondit « Mon tableur fait déjà l’affaire ».
			</p>
			<h3><a name="fonctionnalite-notation"></a><a href="#fonctionnalite-notation">Fonctionnalité de notation</a></h3>
			<p>
			Bien que dans l’industrie du jeu vidéo et l’univers qui y est associé, il est commun d’attribuer des notes aux jeu, j’ai décidé après mûre réflexion que jamais cette fonctionnalité ne sera intégrée à Triumphum.
			</p>
			<p>
			Le fait est que pareil usage n’a strictement aucune autre utilité que dans le contexte très particulier de l’industrie et plus encore des distributeurs. En d’autres termes, les notes de jeu attribuée par des magasines de connivence avec les éditeurs, n’a d’autre intérêt que de diriger le consommateur en lui disant qu’il doit acheter tel jeu car ayant une note de plus de huit ou neuf sur dix. Or, à priori, un utilisateur de Triumphum n’est pas ce père de famille qui, un 24 décembre à 20 h se demande désespérément quoi acheter comme jeu à ses enfants avant de se poser la même question dix minutes plus tard pour le parfum à acheter à sa femme. Triumphum ne vend rien à ses utilisateur, et n’a pas à reprendre à son compte les obsessions de l’industrie.
			</p>
			<h2><a name="a-faire"></a><a href="#a-faire">À FAIRE</a></h2>
			<ul>
				<li class="done">Autocompletion pour Zsh ;</li>
				<li class="done">Autocompletion pour Bash ;</li>
				<li class="done">Modularisation des différentes parties ;</li>
				<li class="undone">Paquet .deb ;</li>
				<li class="undone">Commenter le code ;</li>
				<li class="undone">Message d’érreur pour le terminal trop petit ;</li>
				<li class="undone">Gestion de la locale ;</li>
				<li class="undone">Graphique du temps et des dates de jeu ;</li>
				<li class="undone">Mode de recherche ;</li>
				<li class="undone">Prise de commentaire ;</li>
				<li class="undone">Génération de la manpage et du site web à travers xml ;</li>
				<li class="undone">Autocempletion dans le shell interne ;</li>
				<li class="undone">Consomation moyenne de RAM|GPU par jeu ;</li>
				<li class="undone">Poid des jeux ;</li>
				<li class="undone">Filtre ;</li>
				<li class="undone">Affichage de l’aide sur l’interface TUI ;</li>
				<li class="undone">Éditer les jeux sur l’interface TUI.</li>
			</ul>
			<h2><a name="captures-decran"></a><a href="#captures-decran">CAPTURES D’ÉCRAN</a></h2>
			<h3><a name="liste-des-jeux"></a><a href="#liste-des-jeux">Liste des jeux</a></h3>
			<p>
			<img src="./screanshots/acceuill.png" alt="Liste des jeux" />
			</p>
			<h3><a name="ecran-a-propos"></a><a href="#ecran-a-propos">Écran à propos</a></h3>
			<p>
			<img src="./screanshots/about.png" alt="À propos" />
			</p>
			<h2><a name="voir-aussi"></a><a href="#voir-aussi">VOIR AUSSI</a></h2>
			<ul class="inline">
				<li><a href="https://lutris.net/"><span class="externalCommand usermanual">lutris(1)</span><a>,</li>
				<li><a href="https://wiki.gnome.org/Apps/Games"><span class="externalCommand usermanual">gnome-games(1)</span><a>.</li>
			</ul>
			<h2><a name="liens"></a><a href="#liens">LIENS</a></h2>
			<h3><a name="site-web"></a><a href="#site-web">Site web</a></h3>
			<p>
			<a class="link" href="https://fauvenoir.github.io/triumphum/">https://fauvenoir.github.io/triumphum/</a>
			</p>
			<h3><a name="depot"></a><a href="#depot">Dépot Git</a></h3>
			<p>
			<a class="link" href="https://github.com/FauveNoir/triumphum/">https://github.com/FauveNoir/triumphum/</a>
			</p>
			<h3><a name="don"></a><a href="#don">Don</a></h3>
			<p>
			Pour soutenir Triumphum et faire en sorte qu’il continue et s’améliore, merci de faire un don sur
			<a class="link" href="https://paypal.me/ihidev">https://paypal.me/ihidev</a>.
			</p>
			<h2><a name="auteur"></a><a href="#auteur">AUTEUR</a></h2>
			<p>
			Écrit par Fauve alias Idriss al Idrissi &lt;<a href="mailto:contact@taniere.info" class="link">contact@taniere.info</a>&gt;.
			</p>
