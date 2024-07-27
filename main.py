
from aiogram import Bot, Dispatcher, types, filters, F
import asyncio
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
import openai
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup


bot = Bot(token="7224188489:AAEAdfwZpJkA9g4Myix95Mt2YmvqAbnUHBQ")
dp = Dispatcher(bot=bot)


openai.api_key ='sk-proj-UvFgUoMCDKM370wabpb7T3BlbkFJKVXojcXT8gK1kb9gDxht'


contact_button_ru = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="Отправить контакт",request_contact=True)]
])


language = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="Uzbek tili 🇺🇿"), KeyboardButton(text="Русский язык 🇷🇺")],
], resize_keyboard=True)


menu_uz = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="Kurslar"), KeyboardButton(text="Savat"), KeyboardButton(text="Biz haqimizda")],
    [KeyboardButton(text="Qo'llab-quvvatlash"), KeyboardButton(text="Tilni o'zgartirish")]
], resize_keyboard=True)

menu_ru = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="Курсы"), KeyboardButton(text="Корзинка"), KeyboardButton(text="О нас")],
    [KeyboardButton(text="Поддержка"), KeyboardButton(text="Язык")]
], resize_keyboard=True)


courses_keyboard_uz = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="Inter Nation School📒🇬🇧"), KeyboardButton(text="Mars It School💻")],
    [KeyboardButton(text="Yuksalish LEADERS ACADEMY💼📈"), KeyboardButton(text="My-School📕🇬🇧")],
    [KeyboardButton(text="CodeCraft Academy🖥"), KeyboardButton(text="Tech Innovators💱💲")],
    [KeyboardButton(text="Orqaga↩️")]
], resize_keyboard=True)



about_us_keyboard_uz = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Kompaniya haqida video", url="URL_TO_COMPANY_VIDEO")],
    [InlineKeyboardButton(text="Kompaniya sayti", url="URL_TO_COMPANY_WEBSITE")]
])

about_us_keyboard_ru = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Видео о компании", url="URL_TO_COMPANY_VIDEO")],
    [InlineKeyboardButton(text="Сайт компании", url="URL_TO_COMPANY_WEBSITE")]
])

course_keyboard_uz = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Sotib olish", callback_data="buy")],
    [InlineKeyboardButton(text="Bekor qilish", callback_data="cancel")]
])

course_keyboard_ru = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Купить", callback_data="buy")],
    [InlineKeyboardButton(text="Отменить", callback_data="cancel")]
])


class Reg(StatesGroup):
    name = State()
    number = State()


class Reg_uz(StatesGroup):
    ism = State()
    raqam = State()


def answer_process(question):
    response = openai.Completion.create(
        model='gpt-3.5-turbo-instruct',
        prompt=f"{question}",
        max_tokens=1000,
    )
    if response['choices'][0]['text']:
        answer = response['choices'][0]['text']
        answer.replace("_", "\\_")
        answer.replace("*", "\\*")
        answer.replace("[", "\\[")
        answer.replace("`", "\\`")
        answer.replace("=", "\\=")
        return answer
    else:
        return "Nima divossan? "




# @dp.message(F.text)
# async def chatgpt_function(message: types.Message):
#     result = await answer_process(question=message.text)
#     await message.answer(result)



@dp.message(filters.Command("start"))
async def start_function(message: types.Message, state: FSMContext):
    await state.set_state(Reg.name)
    await message.answer("Xush kelibsiz, ism kiriting")



@dp.message(F.text=="Ru")
async def reg1(message: types.Message, state: FSMContext):
    await state.set_state(Reg.name)
    await message.answer('Введите ваше имя')

@dp.message(Reg.name)
async def reg2(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(Reg.number)
    await message.answer('Введите номер телефона', reply_markup=contact_button_ru)


@dp.message(Reg.number)
async def two_three(message: types.Message, state: FSMContext):
    await state.update_data(number=message.contact.phone_number)
    data = await state.get_data()
    await message.answer(f"Спасибо, Вы прошли регистрацию\nИмя:  {data["name"]}\nНомер:  {data["number"]}", reply_markup=courses_keyboard_uz)
    await state.clear()

@dp.message(F.text == "Uz")
async def reg_uzz(message: types.Message, state: FSMContext):
    await state.set_state(Reg_uz.ism)
    await message.answer('Ismizni kiriting: ')

@dp.message(Reg_uz.ism)
async def reg_uzb(message: types.Message, state: FSMContext):
    await state.update_data(ism=message.text)
    await state.set_state(Reg_uz.raqam)
    await message.answer('Telefon raqamingizni kiriting: ', reply_markup=contact_button_uz)

@dp.message(Reg_uz.raqam)
async def two_three_uzb(message: types.Message, state: FSMContext):
    await state.update_data(raqam=message.contact.phone_number)
    data = await state.get_data()
    await message.answer(
        f"Siz muvaffaqaiyatli royxatdan otdingiz\nIsm:  {data["ism"]}\nTel raqam:  {data["raqam"]}",
        reply_markup=uz_menu)
    await state.clear()


@dp.message(filters.Command("start"))
async def start_function(message: types.Message):
    await message.answer("Tilini tanlang 🌐:\nВыберите язык 🌐:", reply_markup=language)


@dp.message(F.text == "Uzbek tili 🇺🇿")
async def uz_language(message: types.Message):
    await message.answer("Siz Uzbek tilini tanladingiz🔄🇺🇿", reply_markup=menu_uz)


@dp.message(F.text == "Русский язык 🇷🇺")
async def ru_language(message: types.Message):
    await message.answer("Вы выбрали русский язык🔄🇷🇺", reply_markup=menu_ru)


@dp.message(F.text == "Kurslar")
async def course_menu_uz(message: types.Message):
    await message.answer("Kursni tanlang:", reply_markup=courses_keyboard_uz)


@dp.message(F.text == "Курсы")
async def course_menu_ru(message: types.Message):
    await message.answer("Выберите курс:", reply_markup=courses_keyboard_ru)


@dp.message(F.text == "Savat")
async def cart_uz(message: types.Message):
    await message.answer("Savat bo'sh🗑:")


@dp.message(F.text == "Корзинка")
async def cart_ru(message: types.Message):
    await message.answer("Корзинка🗑:")


@dp.message(F.text == "Biz haqimizda")
async def about_us_uz(message: types.Message):
    photo = "https://png.klev.club/uploads/posts/2024-04/png-klev-club-qmhl-p-podderzhka-png-30.png"
    await message.answer_photo(photo=photo, caption="Biz haqimizda:\nKompaniya haqida ma'lumot", reply_markup=about_us_keyboard_uz)




@dp.message(F.text == "О нас")
async def about_us_ru(message: types.Message):
    photo = "https://png.klev.club/uploads/posts/2024-04/png-klev-club-qmhl-p-podderzhka-png-30.png"
    await message.answer_photo(photo=photo, caption="О нас:\nОписание компании", reply_markup=about_us_keyboard_ru)


@dp.message(F.text == "Qo'llab-quvvatlash")
async def support_uz(message: types.Message):
    await message.answer("Qo'llab-quvvatlash: ChatGPT bilan suhbat")


@dp.message(F.text == "Поддержка")
async def support_ru(message: types.Message):
    await message.answer("Поддержка: чат с ChatGPT")




@dp.message(F.text == "Tilni o'zgartirish")
async def change_language_uz(message: types.Message):
    await message.answer("Tilni o'zgartirish", reply_markup=language)


@dp.message(F.text == "Язык")
async def change_language_ru(message: types.Message):
    await message.answer("Поменять язык", reply_markup=language)


@dp.message(F.text == "Orqaga↩️")
async def back_uz(message: types.Message):
    await message.answer("Bosh menyuga qaytish", reply_markup=menu_uz)


@dp.message(F.text == "Назад↩️")
async def back_ru(message: types.Message):
    await message.answer("Возвращение в главное меню", reply_markup=menu_ru)


@dp.message(F.text == "Inter Nation School📒🇬🇧")
async def inter_nation_school_uz(message: types.Message):
    photo = "https://www.afisha.uz/uploads/media/2022/11/3acf1f5c74ae2a01bdc9c33db6752673.jpg"
    await message.answer_photo(photo=photo, caption="Inter Nation School 🌐®️\n888.000 som💲", reply_markup=course_keyboard_uz)


@dp.message(F.text == "Inter_Nation_School📒🇬🇧")
async def inter_nation_school_ru(message: types.Message):
    photo = "https://www.afisha.uz/uploads/media/2022/11/3acf1f5c74ae2a01bdc9c33db6752673.jpg"
    await message.answer_photo(photo=photo, caption="Inter Nation School 🌐®️\n888.000 сум💲", reply_markup=course_keyboard_ru)


@dp.message(F.text == "Mars It School💻")
async def mars_it_school_uz(message: types.Message):
    photo = ""
    await message.answer_photo(photo=photo, caption="Mars It School 💻®️\n1.090.000 som💲", reply_markup=course_keyboard_uz)


@dp.message(F.text == "Mars_It_School💻")
async def mars_it_school_ru(message: types.Message):
    photo = ""
    await message.answer_photo(photo=photo, caption="Mars It School 💻®️\n1.090.000 сум💲", reply_markup=course_keyboard_ru)


@dp.message(F.text == "Yuksalish LEADERS ACADEMY💼📈")
async def yuksalish_uz(message: types.Message):
    photo = "https://i3.photo.2gis.com/images/branch/0/30258560079256542_d925_328x170.jpg"
    await message.answer_photo(photo=photo, caption="Yuksalish LEADERS ACADEMY®️\n1.100.000 som💲", reply_markup=course_keyboard_uz)


@dp.message(F.text == "Yuksalish_LEADERS_ACADEMY💼📈")
async def yuksalish_ru(message: types.Message):
    photo = "https://i3.photo.2gis.com/images/branch/0/30258560079256542_d925_328x170.jpg"
    await message.answer_photo(photo=photo, caption="Yuksalish LEADERS ACADEMY®️\n1.100.000 сум💲", reply_markup=course_keyboard_ru)


@dp.message(F.text == "My-School📕🇬🇧")
async def my_school_uz(message: types.Message):
    photo = "https://i.ytimg.com/vi/TuIZb1xiS4k/maxresdefault.jpg"
    await message.answer_photo(photo=photo, caption="My School ®️\n750.000 som💲", reply_markup=course_keyboard_uz)


@dp.message(F.text == "My_School📕🇬🇧")
async def my_school_ru(message: types.Message):
    photo = "https://i.ytimg.com/vi/TuIZb1xiS4k/maxresdefault.jpg"
    await message.answer_photo(photo=photo, caption="My School ®️\n750.000 сум💲", reply_markup=course_keyboard_ru)


@dp.message(F.text == "CodeCraft Academy🖥")
async def codecraft_academy_uz(message: types.Message):
    photo = "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRopQrsX-sw-bkviP44aN-G6SxzqakB9FyM-w&usqp=CAU"
    await message.answer_photo(photo=photo, caption="CodeCraft Academy ®️\n950.000 som💲", reply_markup=course_keyboard_uz)


@dp.message(F.text == "CodeCraft_Academy🖥")
async def codecraft_academy_ru(message: types.Message):
    photo = "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRopQrsX-sw-bkviP44aN-G6SxzqakB9FyM-w&usqp=CAU"
    await message.answer_photo(photo=photo, caption="CodeCraft Academy ®️\n950.000 сум💲", reply_markup=course_keyboard_ru)


@dp.message(F.text == "Tech Innovators💱💲")
async def tech_innovators_uz(message: types.Message):
    photo = "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQYMrvFtbhCbe4n6Xo_Xqrud96auL7pUTTfRA&usqp=CAU"
    await message.answer_photo(photo=photo, caption="Tech Innovators ®️\n1.200.000 som💲", reply_markup=course_keyboard_uz)


@dp.message(F.text == "Tech_Innovators💱💲")
async def tech_innovators_ru(message: types.Message):
    photo = "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQYMrvFtbhCbe4n6Xo_Xqrud96auL7pUTTfRA&usqp=CAU"
    await message.answer_photo(photo=photo, caption="Tech Innovators ®️\n1.200.000 сум💲", reply_markup=course_keyboard_ru)




@dp.message(F.Text("buy"))
async def buy_course(callback_query: types.CallbackQuery):
    await callback_query.answer("Siz kursni sotib oldingiz!\nВы купили курс!", show_alert=True)


@dp.message(F.Text("cancel"))
async def cancel_course(callback_query: types.CallbackQuery):
    await callback_query.answer("Siz kursni bekor qildingiz.\nВы отменили курс.", show_alert=True)


async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())