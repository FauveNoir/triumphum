########################################################################
# Variables globales
########################################################################

import pendulum
import humanize

APP_CODE_NAME="triumphum"
APP_FANCY_NAME="Triumphum"
APP_DESCRIPTION="Gestionnaire de ludothèque en Python et NCurses pour GNU/Linux"
APP_VERSION="1.0.1"
APP_AUTHOR="Fauve"
APP_LICENCE=""
APP_MOTO="LACRIMOSA·GAVDIVM·EST"
APP_AUTHOR_MAIL="fauve.ordinator@taniere.info"
APP_AUTHOR_DONATION_LINK="https://paypal.me/ihidev"
APP_SYMBOL="⚔"
APP_URL=""
SPLASH_MESSAGE=f"Ceci est {APP_FANCY_NAME} {APP_VERSION}\n" \
	f"{APP_DESCRIPTION}\n" \
	"Par Fauve alias Idriss al Idrissi <contact@taniere.info>"
APP_SPLASH=f"""
     /¯\\
     \\8/
      8
      8
ooooooooooooo
8'   888   `8
     888     .             o8o                                           oooo
     888   .o8             `"'                                           `888
     888 .o888oo oooo d8b oooo  oooo  oooo  ooo. .oo.  .oo.   oo.ooooo.   888 .oo.   oooo  oooo  ooo. .oo.  .oo.
     888   888   `888""8P `888  `888  `888  `888P"Y88bP"Y88b   888' `88b  888P"Y88b  `888  `888  `888P"Y88bP"Y88b
     888   888    888      888   888   888   888   888   888   888   888  888   888   888   888   888   888   888
     888   888 .  888      888   888   888   888   888   888   888   888  888   888   888   888   888   888   888
     888   "888" d888b    o888o  `V88V"V8P' o888o o888o o888o  888bod8P' o888o o888o  `V88V"V8P' o888o o888o o888o
     888       ┓ ┏┓┏┓┳┓╻┳┳┓┏┓┏┓┏┓ ┏┓┏┓╻╻┳┓┳╻╻┳┳┓ ┏┓┏┓┏┳┓       888
     888       ┃ ┣┫┃ ┣┫┃┃┃┃┃┃┗┓┣┫•┃┓┣┫┃┃┃┃┃┃┃┃┃┃•┣ ┗┓ ┃       o888o
     888       ┗┛┛┗┗┛┛╹╹┛ ┗┗┛┗┛┛┗ ┗┛┛┗┗┛┻┛┻┗┛┛ ┗ ┗┛┗┛ ┻
     888 
     888
     888       {SPLASH_MESSAGE.splitlines()[0]}
     888       {SPLASH_MESSAGE.splitlines()[1]}
     888
     o8o       {SPLASH_MESSAGE.splitlines()[2]}
     \8/
      V
"""

APP_NAME = APP_SYMBOL + " " + APP_FANCY_NAME + " | " + APP_DESCRIPTION
# Définir la locale dans Pendulum
pendulum.set_locale('fr')
_t = humanize.i18n.activate("fr_FR")

