import re
import csv
import numpy as np
import matplotlib.pyplot as plt
import random
from PIL import Image
import os


# -*- coding: UTF-8 -*-

def generate_piechart(labels, values, colors, title, output, round=True):
    """Generates a piechart"""

    def absolute_value(val):
        a = np.round(val / 100. * values.sum(), 0)
        return '{0:g}'.format(float(a))

    def absolute_value_full(val):
        a = np.round(val / 100. * values.sum(), 2)
        return a

    plt.clf()
    plt.figure(figsize=(14, 7))
    if round:
        plt.pie(values, labels=labels, colors=colors,
                autopct=absolute_value, startangle=90, textprops={'fontsize': 14})
    else:
        plt.pie(values, labels=labels, colors=colors,
                autopct=absolute_value_full, startangle=90, textprops={'fontsize': 14})
    plt.title(title, fontsize=17)
    plt.axis('equal')
    plt.tight_layout()
    plt.savefig(output)


def generate_barchart(labels, values, ylabel, title, output):
    """Generates a barchart"""
    plt.clf()
    plt.figure(figsize=(14, 7))
    y_pos = np.arange(len(labels))
    plt.bar(y_pos, values, align='center', alpha=0.5, color=generate_colors([0])[0], width=0.4)
    plt.xticks(y_pos, labels, fontname="Segoe UI Emoji", fontsize=11)
    plt.ylabel(ylabel, fontsize=13)
    plt.title(title, fontsize=17)
    plt.savefig(output, dpi=100)


def collect_members(csv_path):
    """Creates a list of all participants in chat"""
    users = {}
    with open(csv_path, encoding="utf8") as csvfile:
        r = csv.reader(csvfile, delimiter=";")
        for row in r:
            if len(row) == 4:
                user = row[2]
                if user not in users:
                    users[user] = 0
    return users


def generate_csv(file_path, csv_path):
    """Creates a csv formatted file from chat.txt"""
    file_txt = open(file_path, "r", encoding="utf8")
    file_csv = open(csv_path, "w", encoding="utf8")
    chat = file_txt.read()
    # Bring into csv format
    # Remove ; because it could interfere with delimiters
    chat = chat.replace(";", ":")
    # Create delimiters for user
    chat = re.sub("(\d{2}\.\d{2}\.\d{2}, \d{2}:\d{2} - )(.*?):", r"\1\2;", chat)
    # Create delimiters for date and time
    chat = re.sub(r"(^[0-9]{2}\.[0-9]{2}\.[0-9]{2}), ", r"\1;", chat, flags=re.MULTILINE)
    chat = re.sub(r"([0-9]{2}:[0-9]{2}) - ", r"\1;", chat)
    # Remove unicode new line char
    chat = chat.replace('\u200e', '')
    # Pictures and stuff
    chat = chat.replace('<Medien ausgeschlossen>', "<Bild>")
    # Merge messages over multiple lines into one line
    chat = re.sub(r'\n', ' ', chat, flags=re.MULTILINE)
    chat = re.sub(r'([0-9]{2}\.[0-9]{2}\.[0-9]{2})', r'\n\1', chat)

    # Write formatted data in csv file and close everything
    file_csv.write(chat)
    file_txt.close()
    file_csv.close()


def generate_colors(users):
    """Generates a list of length of users of HEX valued colors"""
    color = ["#" + ''.join([random.choice('0123456789ABCDEF') for j in range(6)])
             for i in range(len(users))]
    return color


def get_total_messages(amount_messages):
    """Collects amount of total messages"""
    total = 0
    for k, v in amount_messages.items():
        total += v
    return total


def generate_charts(users):
    """Generates png files for charts"""
    colors = generate_colors(users)
    labels_messages = []
    values_messages = []
    labels_words = []
    values_words = []
    labels_average = []
    values_average = []
    total_messages = get_total_messages(amount_messages)
    words_per_message = get_words_per_message(users)
    for user in users:
        labels_messages.append("von {}".format(user))
        labels_words.append("von {}".format(user))
        values_messages.append(amount_messages[user])
        values_words.append(amount_words_user[user])
        labels_average.append("{}".format(user))
        values_average.append(words_per_message[user])
    values_messages = np.array(values_messages)
    values_words = np.array(values_words)
    values_average = np.array(values_average)
    title_messages = "Nachrichten seit {}\nGesamt: {}\n".format(first_date, total_messages)
    output_messsages = 'img/messages_piechart.png'
    title_words = "Wörter gesamt: {}\n".format(total_words)
    output_words = "img/words_piechart.png"
    title_average = "Wörter pro Nachricht im Schnitt"
    output_average = 'img/average_piechart.png'

    generate_piechart(labels_words, values_words, colors, title_words, output_words)
    generate_piechart(labels_messages, values_messages, colors, title_messages, output_messsages)
    generate_piechart(labels_average, values_average, colors, title_average, output_average, round=False)
    generate_barchart(list_words, list_words_values, "Anzahl", "Meist genutzte Wörter", "img/words_barchart.png")
    generate_barchart(list_words_month, list_words_month_values, "Anzahl", "Anzahl Wörter pro Monat",
                      "img/words_month_barchart.png")
    generate_barchart(list_emojis, list_emojis_values, "Anzahl", "Meist genutzte Emojis", "img/emojis_barchart.png")

def get_words_per_message(users):
    words_per_message = {}
    for user in users:
        words_per_message[user] = round(amount_words_user[user]/amount_messages[user], 2)
    return words_per_message

def generate_summary(users):

    total_messages = get_total_messages(amount_messages)
    words_per_message = get_words_per_message(users)
    print("Nachrichten seit {}".format(first_date))
    print("Nachrichten gesamt: {}".format(total_messages))
    print("Wörter gesamt: {}".format(total_words))
    for user in users:
        print(" Nachrichten von {}: {}".format(user, amount_messages[user]))
        print(" Wörter von {}: {}".format(user, amount_words_user[user]))
        print(" Wörter pro Nachricht im Schnitt von {}: {}".format(user, words_per_message[user]))
    print("Meist genutzte Wörter: ")
    for counter in range(0, 20):
        print(" {}: {}-mal".format(sorted_words_values[counter][0], sorted_words_values[counter][1]))
        list_words.append(sorted_words_values[counter][0])
        list_words_values.append(sorted_words_values[counter][1])
    print("Meist genutzte Emojis: ")
    for counter in range(0, 10):
        print(" {}: {}-mal".format(sorted_emojis[counter][0], sorted_emojis[counter][1]))
        list_emojis.append(sorted_emojis[counter][0])
        list_emojis_values.append(sorted_emojis[counter][1])
    print("Nachrichten pro Monat")
    for k, v in amount_months.items():
        print(" Monat {} - {} Nachrichten".format(k, v))
        list_words_month.append(k.replace(".", "/"))
        list_words_month_values.append(v)


def generate_output():
    """Generates a file with all charts"""
    def merge_vertically(images_list):
        imgs = [Image.open(i) for i in images_list]
        min_img_shape = sorted([(np.sum(i.size), i.size) for i in imgs])[0][1]
        img_merge = np.hstack((np.asarray(i.resize(min_img_shape, Image.ANTIALIAS)) for i in imgs))
        img_merge = Image.fromarray(img_merge)
        img_merge.save("{}_v.png".format(images_list[0]))

    def merge_horizontally(images_list):
        imgs = [Image.open(i) for i in images_list]
        min_img_shape = sorted([(np.sum(i.size), i.size) for i in imgs])[0][1]
        img_merge = np.vstack((np.asarray(i.resize(min_img_shape, Image.ANTIALIAS)) for i in imgs))
        img_merge = Image.fromarray(img_merge)
        img_merge.save('img/complete.png')

    def cleanup():
        file_list = pair1 + pair2 + ['img/words_month_barchart.png', 'img/messages_piechart.png_v.png',
                                     'img/words_barchart.png_v.png', 'img/average_piechart.png', 'img/words_month_barchart.png_v.png']
        for file in file_list:
            os.remove(file)

    pair1 = ['img/messages_piechart.png', 'img/words_piechart.png']
    pair2 = ['img/words_barchart.png', 'img/emojis_barchart.png']
    pair3 = ['img/words_month_barchart.png', 'img/average_piechart.png']

    merge_vertically(pair1)
    merge_vertically(pair2)
    merge_vertically(pair3)
    merge_horizontally(['img/messages_piechart.png_v.png', 'img/words_barchart.png_v.png', 'img/words_month_barchart.png_v.png'])
    cleanup()


generate_csv("chat_group.txt", "chat.csv")

users = collect_members("chat.csv")
amount_messages = {}
amount_words_user = {}
for user in users:
    amount_messages[user] = 0
    amount_words_user[user] = 0
total_words = 0
amount_words = {}
amount_months = {}
amount_emojis = {}
pattern_not_emoji = '[\d\w!"§\\$%&@/\'„“()=?`´²–³{[\].|}^*\-+#,;:<>]'

# Read fields from csv into variables
with open('chat.csv', encoding="utf8") as csvfile:
    reader = csv.reader(csvfile, delimiter=";")
    # Skip the first line, it is empty
    next(csvfile)
    first_line = True
    for row in reader:
        full_date = row[0]
        if first_line:
            first_date = full_date
            first_line = False
        if len(row) == 4:
            clock = row[1]
            sender = row[2]
            message = row[3].lower()
        else:
            continue
        # Count messages per user
        if sender in amount_messages:
            amount_messages[sender] += 1

        # Count words
        message_list = message.split()
        for word in message_list:
            # Count most used words
            if word in amount_words:
                amount_words[word] += 1
            else:
                amount_words[word] = 1
            # Count words per sender
            if sender in amount_words_user:
                amount_words_user[sender] += 1
            # Count emojis
            if not re.match(pattern_not_emoji, word):
                # Remove everything else from emojis
                emoji = re.sub(pattern_not_emoji + '♀', '', word)
                for char in list(emoji):
                    if '\u200d' not in emoji:
                        if char in amount_emojis:
                            amount_emojis[char] += 1
                        else:
                            amount_emojis[char] = 1
            total_words += 1

        # Messages by month
        month = re.sub('^..\.', "", full_date)
        if month in amount_months:
            amount_months[month] += 1
        else:
            amount_months[month] = 1

sorted_words_values = sorted(amount_words.items(), key=lambda x: x[1], reverse=True)
sorted_emojis = sorted(amount_emojis.items(), key=lambda x: x[1], reverse=True)
list_words = []
list_words_values = []
list_emojis = []
list_emojis_values = []
list_words_month_values = []
list_words_month = []

generate_summary(users)
generate_charts(users)
generate_output()
