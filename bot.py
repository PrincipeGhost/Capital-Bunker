from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
import json
from stripe_checker import check_card
from bin_lookup import get_bin_info

API_TOKEN = '8074878440:AAEgi61kaBrUlfyVksyQ_zZLBrONMhAf_rU'
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

# Load users or create empty file if it doesn't exist
try:
    with open('users.json', 'r') as f:
        users = json.load(f)
except (FileNotFoundError, json.JSONDecodeError):
    users = {}

def save_users():
    with open('users.json', 'w') as f:
        json.dump(users, f)

@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    uid = str(message.from_user.id)
    if uid not in users:
        users[uid] = {"credits": 0}
        save_users()
    credits = users[uid]["credits"]
    await message.answer_photo(
        photo=open("FB_IMG_17529720788216929.jpg", "rb"),
        caption=f"""🏴‍☠️ *357 Checker* 🏴‍☠️

_Costo de Live:_ 1 crédito
_Costo de Dead:_ 1 crédito
_Pasarela:_ Stripe Live

📄 Envía las tarjetas en formato:
`5303xxxxxxxxxxxx|MM|YYYY|CVV`

Tienes {credits} créditos disponibles.
Escribe /stop para cancelar.
""",
        parse_mode="Markdown"
    )

@dp.message_handler(commands=['stop'])
async def stop(message: types.Message):
    await message.reply("✅ Sesión cancelada.")

@dp.message_handler()
async def process_cards(message: types.Message):
    uid = str(message.from_user.id)
    if uid not in users:
        await message.reply("❌ Debes usar /start primero.")
        return

    cards = message.text.strip().splitlines()
    responses = []
    for card in cards:
        if users[uid]["credits"] <= 0:
            await message.reply("⚠️ Sin créditos disponibles.")
            return

        try:
            number, mes, year, cvv = card.strip().split('|')
            result = check_card(number, mes, year, cvv)
            bin_data = get_bin_info(number[:6])

            respuesta = f"""💳 `{number}`  
Pais: {bin_data.get('country_name', '❓')}  
Banco: {bin_data.get('bank', '❓')}  
Tipo: {result['status']}  
Motivo: {result['message']}"""

            users[uid]["credits"] -= 1
            responses.append(respuesta)
        except:
            responses.append(f"❌ Error con formato o tarjeta: {card}")

    save_users()
    await message.reply("\n\n".join(responses), parse_mode="Markdown")

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)