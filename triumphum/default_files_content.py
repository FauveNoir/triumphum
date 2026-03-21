defaultGenresContent="""{
	"genres": [
		{
			"name": "Action",
			"abbr": "Act",
			"code": "action"
		},
		{
			"name": "Aventure",
			"abbr": "Adv",
			"code": "aventure"
		},
		{
			"name": "Jeu de r\u00f4le,",
			"abbr": "RPG",
			"code": "rpg"
		},
		{
			"name": "Strat\u00e9gie",
			"abbr": "Strat",
			"code": "strategie"
		},
		{
			"name": "Strat\u00e9gie en temps r\u00e9el",
			"abbr": "STR",
			"code": "rts"
		},
		{
			"name": "Strat\u00e9gie au tour par tour",
			"abbr": "STT",
			"code": "tbs"
		},
		{
			"name": "Simulation",
			"abbr": "Sim",
			"code": "simulation"
		},
		{
			"name": "Simulation \u00e9conomique",
			"abbr": "Tycoon",
			"code": "tycoon"
		},
		{
			"name": "Sport",
			"abbr": "Spo",
			"code": "sport"
		},
		{
			"name": "Bac \u00e0 sable",
			"abbr": "B\u00c0S",
			"code": "sandbox"
		},
		{
			"name": "Course",
			"abbr": "Crs",
			"code": "race"
		},
		{
			"name": "Puzzle",
			"abbr": "Puz",
			"code": "puzzle"
		},
		{
			"name": "Horreur",
			"abbr": "Hor",
			"code": "horreur"
		},
		{
			"name": "FPS (First Person Shooter)",
			"abbr": "FPS",
			"code": "fps"
		},
		{
			"name": "TPS (Third Person Shooter)",
			"abbr": "TPS",
			"code": "tps"
		},
		{
			"name": "Roguemorphe",
			"abbr": "Rogue",
			"code": "roguelike"
		},
		{
			"name": "Plateforme",
			"abbr": "Platef",
			"code": "platformer"
		},
		{
			"name": "shoot them up",
			"abbr": "Shmup",
			"code": "shmup"
		},
		{
			"name": "Metrog\u00e8ne",
			"abbr": "Metro",
			"code": "citybuilder"
		},
		{
			"name": "MMORPG (Massively Multiplayer Online Role-Playing Game)",
			"abbr": "MMORPG",
			"code": "mmorpg"
		},
		{
			"name": "ABC",
			"code": "abc"
		},
		{
			"name": "Blablab",
			"code": "blablablabla1"
		}
	]
}"""

defaultLicencesContent="""{
	"licences": [
		{
			"name": "GNU General Public License",
			"abbr": "GPL",
			"code": "gpl",
			"url": "https://www.gnu.org/licenses/gpl-3.0.html",
			"shortText": "La licence publique générale GNU est une licence de logiciel libre adoptée par la Free Software Foundation (FSF) pour le projet GNU.",
			"freedomCoefficient": 0.8
		},
		{
			"name": "Domaine public",
			"abbr": "DP",
			"code": "dp",
			"shortText": "Le domaine public désigne l’ensemble des œuvres (littéraires, artistiques, logicielles, etc.) dont les droits patrimoniaux ont expiré, ont été renoncés ou sont inapplicables.",
			"freedomCoefficient": 1
		},
		{
			"name": "Droits d’auteur",
			"abbr": "©",
			"code": "c",
			"shortText": "Le droit d’auteur est un ensemble de droits exclusifs accordés par la loi aux auteurs ou à leurs ayants droit pour l’exploitation de leurs œuvres originales.",
			"freedomCoefficient": 0
		},
		{
			"name": "MIT License",
			"abbr": "MIT",
			"code": "mit",
			"url": "https://opensource.org/licenses/MIT",
			"shortText": "La licence MIT est une licence logicielle permissive, de courte durée, qui garantit la liberté d’utiliser, de copier, de modifier, de fusionner, de publier, de distribuer, de sous-licencier et de vendre des copies d’un logiciel, en accordant aux destinataires une autorisation limitée mais sans garantie.",
			"freedomCoefficient": 0.6
		},
		{
			"name": "Apache License",
			"abbr": "Apache",
			"code": "apache",
			"url": "https://www.apache.org/licenses/LICENSE-2.0",
			"shortText": "La licence Apache est une licence libre et ouverte pour les logiciels produite par la Apache Software Foundation (ASF), une organisation à but non lucratif dédiée à la promotion des logiciels open source.",
			"freedomCoefficient": 0.7
		},
		{
			"name": "BSD License",
			"abbr": "BSD",
			"code": "bsd",
			"url": "https://opensource.org/licenses/BSD-2-Clause",
			"shortText": "La licence BSD est une licence de logiciel libre permise par l’Université de Californie à Berkeley (UCB).",
			"freedomCoefficient": 0.9
		},
		{
			"name": "Creative Commons",
			"abbr": "CC",
			"code": "cc",
			"url": "https://creativecommons.org/licenses/",
			"shortText": "Creative Commons est une organisation à but non lucratif qui propose une série de licences juridiquement contraignantes gratuites pour les œuvres créatives.",
			"freedomCoefficient": 0.8
		},
		{
			"name": "Mozilla Public License",
			"abbr": "MPL",
			"code": "mozilla_public_license",
			"url": "https://www.mozilla.org/en-US/MPL/",
			"shortText": "La Mozilla Public License (MPL) est une licence de logiciel libre créée et maintenue par la Fondation Mozilla. Elle est conçue pour être compatible avec la GNU General Public License (GPL).",
			"freedomCoefficient": 0.6
		},
		{
			"name": "Unlicense",
			"abbr": "Unlicense",
			"code": "un",
			"url": "https://unlicense.org/",
			"shortText": "L’Unlicense est une licence de domaine public qui permet aux détenteurs de droits d’auteur de renoncer à leurs droits d’auteur sur leurs travaux et de les placer dans le domaine public. Elle est recommandée pour les œuvres destinées au domaine public.",
			"freedomCoefficient": 0.2
		},
		{
			"name": "Beerware License",
			"abbr": "Beerware",
			"code": "beerware",
			"shortText": "La Beerware License est une licence humoristique pour les logiciels. Elle est inspirée par la tradition de la bière dans la communauté des logiciels libres.",
			"freedomCoefficient": 0.7
		},
		{
			"name": "WTFPL (Do What The Fuck You Want To Public License)",
			"abbr": "WTFPL",
			"code": "wtfpl",
			"url": "http://www.wtfpl.net/",
			"shortText": "La WTFPL est une licence de logiciel libre très permissive qui permet de faire ce que vous voulez avec le logiciel, sans aucune restriction.",
			"freedomCoefficient": 1
		},
		{
			"name": "Fair License",
			"abbr": "Fair",
			"code": "fair_license",
			"url": "http://fairlicense.org/",
			"shortText": "La Fair License est une licence de logiciel libre qui se concentre sur la simplicité et la liberté. Elle vise à permettre aux développeurs de logiciels de partager leur code avec peu de restrictions.",
			"freedomCoefficient": 0.7
		},
		{
			"name": "GNU Lesser General Public License",
			"abbr": "LGPL",
			"code": "lgpl",
			"url": "https://www.gnu.org/licenses/lgpl-3.0.html",
			"shortText": "La GNU Lesser General Public License (LGPL) est une licence de logiciel libre conçue pour permettre l’utilisation de bibliothèques logicielles libres dans les logiciels propriétaires.",
			"freedomCoefficient": 0.8
		},
		{
			"name": "Microsoft Public License",
			"abbr": "MS-PL",
			"code": "ms",
			"url": "https://opensource.org/licenses/MS-PL",
			"shortText": "La Microsoft Public License (MS-PL) est une licence de logiciel libre proposée par Microsoft Corporation. Elle permet de modifier et de redistribuer librement le code source.",
			"freedomCoefficient": 0.5
		},
		{
			"name": "PostgreSQL License",
			"abbr": "PostgreSQL",
			"code": "postgresql_license",
			"url": "https://opensource.org/licenses/postgresql",
			"shortText": "La licence PostgreSQL est une licence libre et ouverte pour la base de données PostgreSQL. Elle est basée sur la licence BSD.",
			"freedomCoefficient": 0.6
		},
		{
			"name": "Artistic License",
			"abbr": "Artistic",
			"code": "artistic",
			"url": "https://www.perlfoundation.org/artistic-license-20.html",
			"freedomCoefficient": 0.7
		},
		{
			"name": "Abandogiciel",
			"abbr": "Abandogiciel",
			"code": "abandonware",
			"freedomCoefficient": 0.3
		},
		{
			"name": "Nethack General Public License",
			"abbr": "Nethack",
			"code": "nethack",
			"url": "https://nethack.org/common/license.html",
			"shortText": "La Nethack General Public License est une licence de logiciel libre utilisée pour distribuer le jeu Nethack. Elle est basée sur la licence GNU General Public License (GPL).",
			"freedomCoefficient": 0.6
		}
	]
}"""

defaultPlatformsContent="""{
	"platforms":
	[
		{
			"name": "Linux",
			"code": "linux",
			"abbr": "LIN"
		},
		{
			"name": "Windows",
			"code": "windows",
			"abbr": "WIN"
		},
		{
			"name": "Mac OS",
			"code": "macos",
			"abbr": "MAC"
		},
		{
			"name": "DOS",
			"code": "dos",
			"abbr": "DOS"
		},
		{
			"name": "3DO",
			"code": "3do",
			"abbr": "3DO"
		},
		{
			"name": "Arcade",
			"code": "arcade",
			"abbr": "Arc"
		},
		{
			"name": "Atari 2600",
			"code": "atari2600",
			"abbr": "At. 2600"
		},
		{
			"name": "Atari 5200",
			"code": "atari5200",
			"abbr": "At. 5200"
		},
		{
			"name": "Atari 7800",
			"code": "atari7800",
			"abbr": "At. 7800"
		},
		{
			"name": "Atari Jaguar",
			"code": "jaguar",
			"abbr": "Jaguar"
		},
		{
			"name": "Atari Lynx",
			"code": "lynx",
			"abbr": "Lynx"
		},
		{
			"name": "Atari Falcon",
			"code": "falcon",
			"abbr": "Falcon"
		},
		{
			"name": "CHIP-8",
			"code": "chip8",
			"abbr": "CHIP-8"
		},
		{
			"name": "ColecoVision",
			"code": "colecovision",
			"abbr": "ColecoVision"
		},
		{
			"name": "Commodore 64",
			"code": "commodore64",
			"abbr": "C. 64"
		},
		{
			"name": "Dreamcast",
			"code": "dreamcast",
			"abbr": "Dreamcast"
		},
		{
			"name": "Famicom Disk System",
			"code": "fds",
			"abbr": "FDS"
		},
		{
			"name": "Game Boy Color",
			"code": "gameboycolor",
			"abbr": "GB Color"
		},
		{
			"name": "Game Boy Advance",
			"code": "gameboyadvance",
			"abbr": "GB Advance"
		},
		{
			"name": "GameCube",
			"code": "gamecube",
			"abbr": "GameCube"
		},
		{
			"name": "Game Gear",
			"code": "gamegear",
			"abbr": "GG"
		},
		{
			"name": "MSX",
			"code": "msx",
			"abbr": "MSX"
		},
		{
			"name": "Neo-Geo Pocket",
			"code": "neogeopocket",
			"abbr": "NGP"
		},
		{
			"name": "Neo-Geo Color",
			"code": "neogeocolor",
			"abbr": "NGC"
		},
		{
			"name": "NEC PC-98",
			"code": "necpc98",
			"abbr": "NEC PC-98"
		},
		{
			"name": "Nintendo 64",
			"code": "nintendo64",
			"abbr": "Nin. 64"
		},
		{
			"name": "Nintendo Entertainment System",
			"code": "nes",
			"abbr": "NES"
		},
		{
			"name": "Nintendo DS",
			"code": "nds",
			"abbr": "NDS"
		},
		{
			"name": "Nintendo 3DS",
			"code": "n3ds",
			"abbr": "Nin. 3DS"
		},
		{
			"name": "Odyssey²",
			"code": "odyssey2",
			"abbr": "Odyssey²"
		},
		{
			"name": "PC-FX",
			"code": "pcfx",
			"abbr": "PC-FX"
		},
		{
			"name": "32X",
			"code": "32x",
			"abbr": "32X"
		},
		{
			"name": "Mega CD",
			"code": "megacd",
			"abbr": "Mega CD"
		},
		{
			"name": "Mega Drive",
			"code": "megadrive",
			"abbr": "MD"
		},
		{
			"name": "Master System",
			"code": "mastersystem",
			"abbr": "Master Sys."
		},
		{
			"name": "PlayStation Portable",
			"code": "playstationportable",
			"abbr": "PSP"
		},
		{
			"name": "PlayStation",
			"code": "playstation",
			"abbr": "PS"
		},
		{
			"name": "Pokémon Mini",
			"code": "pokemonmini",
			"abbr": "Pok. Mini"
		},
		{
			"name": "Sega Saturn",
			"code": "saturn",
			"abbr": "Saturn"
		},
		{
			"name": "Super NES",
			"code": "supernes",
			"abbr": "SNES"
		},
		{
			"name": "Thomson MO/TO",
			"code": "thomsonmoto",
			"abbr": "MO/TO"
		},
		{
			"name": "TurboGrafx-16",
			"code": "turbografx16",
			"abbr": "TG16"
		},
		{
			"name": "SuperGrafx",
			"code": "supergrafx",
			"abbr": "SG"
		},
		{
			"name": "TurboGrafx-CD",
			"code": "turbografxcd",
			"abbr": "TG-CD"
		},
		{
			"name": "Vectrex",
			"code": "vectrex",
			"abbr": "VX"
		},
		{
			"name": "Virtual Boy",
			"code": "virtualboy",
			"abbr": "VB"
		},
		{
			"name": "WonderSwan",
			"code": "wonderswan",
			"abbr": "WS"
		},
		{
			"name": "ZX Spectrum",
			"code": "zxspectrum",
			"abbr": "ZXS"
		},
		{
			"name": "ZX81",
			"code": "zx81",
			"abbr": "ZX81"
		}
	]
}"""
