import tkinter
import customtkinter
import smtplib
from email.mime.text import MIMEText
from email.header import Header
import datetime
import json

#перед использованием прочитайте README.md
#перед использованиеи создайте директорию (папку) под названием "logs"

app = customtkinter.CTk()
app.title("New year")
app.geometry("800x200")


def button_def():
    dialog = customtkinter.CTkInputDialog(text='Напиши сообщение', title='Написание письма')
    b = dialog.get_input()
    # token = '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'
    # openai.api_key = token
    # engine = "text-davinci-003"
    # prompt = f'Как дела?'
    # completion = openai.Completion.create(engine=engine, prompt=prompt,
    #                                       temperature=0.5, max_tokens=1000)
    # a = completion.choise[0]["text"]
    # print(completion.choise[0]["text"])

    import requests
    prompt = {
        "modelUri": "gpt://<your_akk_idendef_token>/yandexgpt-lite",
        "completionOptions": {
            "stream": False,
            "temperature": 0.6,
            "maxTokens": "2000"
        },
        "messages": [
            {
                "role": "system",
                "text": f'Оформи это письмо деду морозу красно речиво, исправь ошибки, сделай так, чтобы оно хорошо звучало, текст письма, которое нужно оформить: {b}'
            }
        ]
    }

    url = "https://llm.api.cloud.yandex.net/foundationModels/v1/completion"
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Api-Key <your_api_key>"
    }

    response = requests.post(url, headers=headers, json=prompt)
    result = json.loads(response.text)
    a = result["result"]["alternatives"][0]["message"]["text"]




    def send_massage(recipients, message):
        sender = "<your_mail>"
        password = "<your_paassword>"
        msg = MIMEText(f'{message}', 'plain', 'utf-8')
        msg['Subject'] = Header(f'Письмо деду морозу!', 'utf-8')
        msg['From'] = sender
        msg['To'] = recipients

        serv = smtplib.SMTP('smtp.yandex.ru', 587, timeout=10)

        try:
            serv.starttls()
            serv.login(sender, password)
            serv.sendmail(msg['From'], msg['To'], msg.as_string())
        except Exception as ex:
            return f'{ex}'
        finally:
            serv.quit()
            print("the email has been sent")
            create_file(message=message)



    def create_file(message):
        date = datetime.date.today()
        time = f'{datetime.datetime.now().time()}'.split(sep=".")
        time = time[0].replace(':', '-')
        name_file = f"message-{date}-{time}.txt"
        file = open(f'logs/{name_file}', 'w')
        file.write(f'{message}')
        print(f"created file -> {name_file}")

    def main(a):
        send_massage(recipients='zadjek@yandex.ru', message=a)

    if b != None:
        main(a)


label = customtkinter.CTkLabel(app, text='Все сообщения сохраняются в дирректории в виде "massage-(year-mountain-day)-(hours-minutes-seconds).txt"'
                                         '\nПример: massage-2023-12-01-22-25-56.txt', width=10)
label.pack(anchor=tkinter.CENTER, pady=20, padx=20)


button = customtkinter.CTkButton(app, text='Отправить письмо Деду Морозу', command=button_def)
button.pack(anchor=tkinter.CENTER, padx=20, pady=20)


app.mainloop()
