from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

client = OpenAI(
  base_url="http://localhost:1234/v1", api_key="lm-studio",
)

with open('data/text_for_summary.txt') as f:
    text_for_summary = f.read()

with open('system_prompt.txt') as f:
    system_prompt = f.read()

with open('data/reviews_for_classification.txt') as f:
    reviews_for_classification = f.read()

def general_function():
  response = client.chat.completions.create(
    model="vikhr-llama-3.2-1b-instruct",
    messages=[
        {
            "role": "system",
            "content": system_prompt
        },
        {
          "role": "user",
          "content": f"""Все было очень вкусно, но пришлось долго ждать, внутри очень душно, зато вкусные"""
        }
    ],
    temperature=0,
    max_completion_tokens=500
  )

  if response.choices and response.choices[0].message.content:
      print(response.choices[0].message.content)
  else:
      print("Ошибка: не удалось получить ответ от API")

def user_assistant():
  examples = [
      ['Это просто возмутительно! Деньги списали, товар не привезли, а поддержка молчит уже вторые сутки. Верните мои деньги!', 'Оценка: 1'],
      ['Привезли не тот цвет, который я заказывал. Доставка была долгой, коробка вся грязная. Оставил себе только потому, что нет времени на возврат. Больше здесь не куплю', 'Оценка: 2'],
      ['Обычный сервис. Заказ пришел в срок, но курьер был не в настроении и даже не поздоровался. Товар нормальный, но вау-эффекта нет. Обычный магазин как сотни других.', 'Оценка: 3'],
      ['Хороший магазин, большой выбор. Заказ подтвердили быстро, привезли на следующий день. Снимаю звезду за то, что на сайте не было информации, что товар идет без батареек.', 'Оценка: 4'],
      ['Я в восторге! Заказал подарок жене в последний момент, ребята вошли в положение и доставили через 2 часа. Качество упаковки — премиум класс. Огромное спасибо!', 'Оценка: 5']
  ]

  messages=[
        {
            "role": "system",
            "content": '''
            # Роль и способности ассистента

            ## Роль
            Ты - умный ассистент. 

            ## Способности

            ### Классификация отзывов
            Ты — эксперт по анализу клиентского опыта. Твоя задача — классифицировать отзывы по шкале от 1 до 5, опираясь на тональность и факты. Используй приведенные ниже примеры как эталон логики. На каждый новый отзыв выдавай ответ без объяснений в формате: Оценка: [число].
            
            # Ограничения
            Если запрос или вопрос не относится к указанным способностям, вежливо откажись отвечать и выполнять задание.'''
        },
    ]
  
  for example in examples:
      messages.append({
          "role": "user",
          "content": example[0]
      })
      messages.append({
          "role": "assistant",
          "content": example[1]
      })
  
  messages.append({
      "role": "user",
      "content": 'Доставка отличная но товар оказался бракованным, очень жаль что так вышло.'
  })

  response = client.chat.completions.create(
    model="vikhr-llama-3.2-1b-instruct",
    messages=messages,
    temperature=0,
    max_completion_tokens=500
  )

  if response.choices and response.choices[0].message.content:
      print(response.choices[0].message.content)
  else:
      print("Ошибка: не удалось получить ответ от API")

def chat_bot():
    
    messages = [
            {
                "role": "system",
                "content": "Ты - полезный ассистент."
            }
    ]

    while True:
      user_prompt = input('Введите ваш запрос (или "выход" для завершения): ')

      if user_prompt.lower() == "выход":
        break
      
      messages.append(
            {
              "role": "user",
              "content": user_prompt
            }
          )

      response = client.chat.completions.create(
        model="vikhr-llama-3.2-1b-instruct",
        messages=messages
      )

      print(response.choices[0].message.content)
      messages.append(
            {
              "role": "assistant",
              "content": response.choices[0].message.content
            }
      )

if __name__ == "__main__":
    # print("=== General Function ===")
    # general_function()
    # print("\n=== User Assistant ===")
    # user_assistant()
    print("\n=== Chat Bot ===")
    chat_bot()
