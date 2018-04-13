import re
import csv
import numpy as np
import matplotlib.pyplot as plt

# TODO
# most used emojis
# Cleanup

# The input file, Send via E-Mail as txt in whatsapp
file_txt = open("chat.txt", "r", encoding="utf8")

# Output .csv in format dd.mm.yy;hh.mm;sender;message
file_csv = open("chat.csv", "w", encoding="utf8")

# Global variables
usr_sender = "EnterFirstNameHere"
usr_recpt = "EnterSecondNameHere"

def generate_piechart(labels, values, colors, title, output):
    def absolute_value(val):
        a = np.round(val / 100. * values.sum(), 0)
        return a
    plt.clf()
    plt.pie(values, labels=labels, colors=colors,
            autopct=absolute_value, startangle=90)
    plt.title(title)
    plt.axis('equal')
    plt.tight_layout()
    plt.savefig(output)

def generate_barchart(labels, values, ylabel, title, output):
    plt.clf()
    plt.figure(figsize=(12, 5))
    x_axis = tuple(labels)
    y_pos = np.arange(len(x_axis))
    plt.bar(y_pos, values, align='center', alpha=0.5)
    plt.xticks(y_pos, x_axis)
    plt.ylabel(ylabel)
    plt.title(title)
    plt.savefig(output)

chat = file_txt.read()
# Bring into csv format
# Remove ; because it could interfere with delimiters
chat = chat.replace(";", ":")
chat = re.sub(r" um | - ", ";", chat)
# Make column for users
chat = chat.replace("{}: ".format(usr_sender), "{};".format(usr_sender))
chat = chat.replace("{}: ".format(usr_recpt), "{};".format(usr_recpt))
# Remove unicode new line char
chat = chat.replace('\u200e', '')

# Clean messages over multiple lines up and move them into one, probably should be made recursive instead of looping
for i in range(1, 35):
    chat = re.sub(r'(\d{2}\.\d{2}.*)\n(?!\d{2}\.\d{2}\.\d{2};)(.*)', r'\1\2', chat)

# Write formatted data in csv file and close everything
file_csv.write(chat)
file_txt.close()
file_csv.close()

amount_messages = {usr_sender: 0, usr_recpt: 0}
total_words = 0
amount_words = {}
amount_words_user = {usr_sender: 0, usr_recpt: 0}
amount_months = {}

# Read fields from csv into variables
with open('chat.csv', encoding="utf8") as csvfile:
    reader = csv.reader(csvfile, delimiter=";")
    first_line = True
    for row in reader:
        full_date = row[0]
        if first_line:
            first_date = full_date
            first_line = False
        clock = row[1]
        sender = row[2]
        message = row[3].lower()
        # Count messages per user
        if sender in amount_messages:
            amount_messages[sender] += 1

        # Count words
        message_list = message.split()
        for word in message_list:
            if word in amount_words:
                amount_words[word] += 1
            else:
                amount_words[word] = 1
            if sender in amount_words_user:
                amount_words_user[sender] += 1
            total_words += 1

        # Messages by month
        month = re.sub('^..\.', "", full_date)
        if month in amount_months:
            amount_months[month] += 1
        else:
            amount_months[month] = 1

sorted_words_values = sorted(amount_words.items(), key=lambda x: x[1], reverse=True)
list_words = []
list_words_values = []
list_words_month_values = []
list_words_month = []

# Summary
total_messages = num_lines = sum(1 for line in open('chat.csv', encoding="utf8"))
print("Nachrichten seit {}".format(first_date))
print("Nachrichten gesamt: {}".format(total_messages))
print(" Nachrichten von {}: {}".format(usr_recpt, amount_messages[usr_recpt]))
print(" Nachrichten von {}: {}".format(usr_sender, amount_messages[usr_sender]))
print("Wörter gesamt: {}".format(total_words))
print(" Wörter von {}: {}".format(usr_recpt, amount_words_user[usr_recpt]))
print(" Wörter von {}: {}".format(usr_sender, amount_words_user[usr_sender]))
print("Meist genutzte Wörter: ")
for counter in range(0, 19):
    print(" {}: {}-mal".format(sorted_words_values[counter][0], sorted_words_values[counter][1]))
    list_words.append(sorted_words_values[counter][0])
    list_words_values.append(sorted_words_values[counter][1])
print("Nachrichten pro Monat")
for k, v in amount_months.items():
    print(" Monat {} - {} Nachrichten".format(k, v))
    list_words_month.append(k)
    list_words_month_values.append(v)


# Generate graphical output
# Messages
colors = ['lightcoral', 'lightskyblue']
labels_messages = ["Nachrichten\nvon {}".format(usr_recpt), "Nachrichten\nvon {}".format(usr_sender)]
values_messages = np.array([amount_messages[usr_recpt], amount_messages[usr_sender]])
title_messages = "Nachrichten seit {}\nGesamt: {}".format(first_date, total_messages)
output_messsages = 'img/messages_piechart.png'
generate_piechart(labels_messages, values_messages, colors, title_messages, output_messsages)

#Words
labels_words = ["Wörter\nvon {}".format(usr_recpt), "Wörter\nvon {}".format(usr_sender)]
values_words = np.array([amount_words_user[usr_recpt], amount_words_user[usr_sender]])
title_words = "Wörter gesamt: {}".format(total_words)
output_words = "img/words_piechart.png"
generate_piechart(labels_words, values_words, colors, title_words, output_words)

generate_barchart(list_words, list_words_values, "Anzahl", "Meist genutzte Wörter", "img/words_barchart.png")
generate_barchart(list_words_month, list_words_month_values, "Anzahl", "Anzahl Wörter pro Monat", "img/words_month_barchart.png")
