from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

class Translation:
    def __init__(self, lang='en'):
        # Set the language for translation
        self.lang = lang
        self.translations = {
            'en': {
                "START_TEXT": """
👋 Hey {} 

I am a Telegram URL Uploader Bot.

**Send me a direct link and I will upload it to Telegram as a file/video**

Use the help button to know how to use me.
                """,
                "HELP_TEXT": """
Link to media or file

➠ Send a link for upload to Telegram file or media.

Set thumbnail

➠ Send a photo to make it as a permanent thumbnail.

Deleting thumbnail

➠ Send /delthumb to delete the thumbnail.

Settings

➠ Configure my settings to change upload mode.

Show Thumbnail

➠ Send /showthumb to view custom thumbnail.
                """,
                "ABOUT_TEXT": """
**My Name**: [Uploader Bot](🦋 @bimbo 🦋)

**Database**: [MongoDB](https://cloud.mongodb.com)

**Language**: [Python 3.12.5](https://www.python.org/)

**Framework**: [Pyrogram 2.3.45](https://docs.pyrogram.org/)

**Developer**: Bimbo69
                """,
                "START_BUTTONS": InlineKeyboardMarkup(
                    [
                        [InlineKeyboardButton('⚙️ Settings', callback_data='OpenSettings')],
                        [InlineKeyboardButton('❔ Help', callback_data='help'),
                         InlineKeyboardButton('👨‍🚒 About', callback_data='about')],
                        [InlineKeyboardButton('⛔️ Close', callback_data='close')]
                    ]
                ),
                "HELP_BUTTONS": InlineKeyboardMarkup(
                    [
                        [InlineKeyboardButton('🏡 Home', callback_data='home'),
                         InlineKeyboardButton('👨‍🚒 About', callback_data='about')],
                        [InlineKeyboardButton('⛔️ Close', callback_data='close')]
                    ]
                ),
                "ABOUT_BUTTONS": InlineKeyboardMarkup(
                    [
                        [InlineKeyboardButton('🏡 Home', callback_data='home'),
                         InlineKeyboardButton('❔ Help', callback_data='help')],
                        [InlineKeyboardButton('⛔️ Close', callback_data='close')]
                    ]
                ),
            },
            'es': {
                "START_TEXT": """
👋 Hola {} 

Soy un Bot de Cargador de URL de Telegram.

**Envíame un enlace directo y lo cargaré a Telegram como archivo/video**

Usa el botón de ayuda para saber cómo usarme.
                """,
                "HELP_TEXT": """
Enlace a medios o archivo

➠ Envía un enlace para cargar a Telegram archivo o medio.

Configurar miniatura

➠ Envía una foto para configurarla como miniatura permanente.

Eliminar miniatura

➠ Envia /delthumb para eliminar la miniatura.

Configuración

➠ Configura mis ajustes para cambiar el modo de carga.

Mostrar miniatura

➠ Envía /showthumb para ver la miniatura personalizada.
                """,
                "ABOUT_TEXT": """
**Mi Nombre**: [Uploader Bot](🦋 @bimbo 🦋)

**Base de datos**: [MongoDB](https://cloud.mongodb.com)

**Lenguaje**: [Python 3.12.5](https://www.python.org/)

**Framework**: [Pyrogram 2.3.45](https://docs.pyrogram.org/)

**Desarrollador**: Bimbo69
                """,
                "START_BUTTONS": InlineKeyboardMarkup(
                    [
                        [InlineKeyboardButton('⚙️ Configuración', callback_data='OpenSettings')],
                        [InlineKeyboardButton('❔ Ayuda', callback_data='help'),
                         InlineKeyboardButton('👨‍🚒 Acerca de', callback_data='about')],
                        [InlineKeyboardButton('⛔️ Cerrar', callback_data='close')]
                    ]
                ),
                "HELP_BUTTONS": InlineKeyboardMarkup(
                    [
                        [InlineKeyboardButton('🏡 Inicio', callback_data='home'),
                         InlineKeyboardButton('👨‍🚒 Acerca de', callback_data='about')],
                        [InlineKeyboardButton('⛔️ Cerrar', callback_data='close')]
                    ]
                ),
                "ABOUT_BUTTONS": InlineKeyboardMarkup(
                    [
                        [InlineKeyboardButton('🏡 Inicio', callback_data='home'),
                         InlineKeyboardButton('❔ Ayuda', callback_data='help')],
                        [InlineKeyboardButton('⛔️ Cerrar', callback_data='close')]
                    ]
                ),
            }
        }

    def get_translation(self, key):
        """Fetch the translation for the current language."""
        return self.translations[self.lang].get(key, key)

