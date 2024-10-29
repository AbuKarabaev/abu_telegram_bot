# import re
# import sympy as sp
# from telegram import Update
# from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes

# # Функция для обработки вопросов
# async def handle_question(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
#     question = update.message.text.lower()

#     # Простой калькулятор для базовых математических операций
#     if any(op in question for op in ['+', '-', '*', '/']):
#         try:
#             result = eval(question)
#             await update.message.reply_text(f"Результат: {result}")
#         except Exception as e:
#             await update.message.reply_text("Извините, не могу решить этот пример.")
#         return

#     # Решение уравнений (например, "реши x + 5 = 10")
#     if "реши" in question:
#         try:
#             equation = question.replace("реши", "").strip()
#             x = sp.symbols('x')
#             solution = sp.solve(equation, x)
#             await update.message.reply_text(f"Решение: x = {solution}")
#         except Exception as e:
#             await update.message.reply_text("Не могу решить уравнение.")
#         return

#     # Вопросы по Python
#     if "python" in question:
#         await update.message.reply_text("Вопрос по Python? Вот простой пример: чтобы вывести текст, используйте print('Ваш текст').")
#         return

#     # Вопросы по Django
#     if "django" in question:
#         await update.message.reply_text("Вопрос по Django? Начните с создания проекта командой `django-admin startproject projectname`.")
#         return

#     # Если вопрос не распознан
#     await update.message.reply_text("Извините, я пока не знаю ответа на этот вопрос.")

# # Функция для обработки команды /start
# async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
#     await update.message.reply_text("Привет! Я бот, который может помочь с математикой, Python и Django.")

# # Основная функция
# def main() -> None:
#     app = ApplicationBuilder().token("7553655606:AAHkNfm3JcwR4UP2TVMQj3TS0Yp_sFTUAFs").build()
    
#     app.add_handler(CommandHandler("start", start))
#     app.add_handler(CallbackQueryHandler(lambda update, context: None))  # Здесь нужно обработать кнопки, если они есть
#     app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_question))

#     app.run_polling()

# if __name__ == '__main__':
#     main()















import random
import re
import sympy as sp
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
import wikipedia
import wolframalpha

wikipedia.set_lang("ru")
wolfram_client = wolframalpha.Client("YOUR_WOLFRAM_APP_ID")

templates = {
    "django": [
        {
            "code": """# Простой макет Django
from django.shortcuts import render

def home(request):
    return render(request, 'home.html', {'title': 'Главная страница'})""",
            "explanation": "Этот код определяет представление (view) для главной страницы. Он возвращает HTML-шаблон 'home.html' с переданным контекстом."
        },
        {
            "code": """# Формы в Django
from django import forms

class ContactForm(forms.Form):
    name = forms.CharField(label='Ваше имя', max_length=100)
    email = forms.EmailField(label='Ваш email')""",
            "explanation": "Этот код создает форму для сбора имени и адреса электронной почты пользователя. Используется класс Form из модуля django.forms."
        },
    ],
    "python": [
        {
            "code": """# Простой макет Python
def greet(name):
    return f'Привет, {name}!'

print(greet('Мир'))""",
            "explanation": "Эта функция 'greet' принимает имя и возвращает приветствие. Затем она вызывается с аргументом 'Мир'."
        },
        {
            "code": """# Использование списков в Python
fruits = ['яблоко', 'банан', 'вишня']
for fruit in fruits:
    print(f'Я люблю {fruit}')""",
            "explanation": "Этот код создает список фруктов и выводит сообщение для каждого фрукта с помощью цикла for."
        },
    ]
}

async def handle_question(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    question = update.message.text.lower().strip()

    if "создай макет" in question or "покажи макет" in question:
        if "джанго" in question:
            template = random.choice(templates["django"])
            await update.message.reply_text(f"**Макет Django:**\n```\n{template['code']}\n```\n\n**Объяснение:** {template['explanation']}")
            return
        elif "пайтон" in question:
            template = random.choice(templates["python"])
            await update.message.reply_text(f"**Макет Python:**\n```\n{template['code']}\n```\n\n**Объяснение:** {template['explanation']}")
            return

    if any(op in question for op in ['+', '-', '*', '/']):
        try:
            result = eval(question)
            await update.message.reply_text(f"Результат: {result}")
        except Exception:
            await update.message.reply_text("Извините, не могу решить этот пример.")
        return

    if "реши" in question:
        try:
            equation = re.sub(r'[^\w\s+=*/-]', '', question.replace("реши", "").strip())
            x = sp.symbols('x')
            solution = sp.solve(equation, x)
            await update.message.reply_text(f"Решение: x = {solution}")
        except Exception:
            await update.message.reply_text("Не могу решить уравнение.")
        return

    try:
        wolfram_res = wolfram_client.query(question)
        wolfram_answer = next(wolfram_res.results).text
        await update.message.reply_text(f"Wolfram Alpha: {wolfram_answer}")
        return
    except Exception:
        pass

    if "что такое" in question or "кто такой" in question:
        try:
            wiki_res = wikipedia.summary(question, sentences=2)
            await update.message.reply_text(f"Wikipedia: {wiki_res}")
            return
        except wikipedia.exceptions.DisambiguationError as e:
            await update.message.reply_text("Уточните ваш запрос.")
        except Exception:
            await update.message.reply_text("Не могу найти информацию в Wikipedia.")
        return

    await update.message.reply_text("Извините, я пока не знаю ответа на этот вопрос.")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "Привет! Я бот, который может помочь с математикой, Python, Django и многими другими темами. "
        "Задайте свой вопрос, и я постараюсь ответить!"
    )

def main() -> None:
    app = ApplicationBuilder().token("7553655606:AAHkNfm3JcwR4UP2TVMQj3TS0Yp_sFTUAFs").build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_question))

    app.run_polling()

if __name__ == '__main__':
    main()
