import telebot

token = ''

bot = telebot.TeleBot(token)
# todos = {'date':[[task1, category], [task2, category], ...], 'date2':[...], ... }
todos = {}  # todos: list -> dict

HELP = '''
List of available commands:
* /print Date1 Date2 ... - print all tasks on the specified date
* /todo - add a task
* /help - Print help
'''


def add_todo(date, task, category):
    # Check if we already have a task on the date
    if date in todos:
        todos[date].append([task, category])
    else:
        todos[date] = [[task, category]]
    print(f'Task "{task}" with category "{category}" add on {date}')


@bot.message_handler(commands=["help"])
def help(message):
    bot.send_message(message.chat.id, HELP)


@bot.message_handler(commands=["add"])
def add(message):
    # /add task @category - Split on 3 parts
    # 1 - command (will ignore)
    # 2 - date
    # 3 - task with category
    splitted_command = message.text.split(maxsplit=2)
    date = splitted_command[1].lower()
    # task @category - Split on 2 parts
    # 1 - task
    # 2 - category
    splitted_task = splitted_command[2].split(' @')
    task = splitted_task[0]
    category = splitted_task[1]
    if len(task) < 3:
        bot.send_message(message.chat.id, f'Unable to add the task on {date}, because the task is too short')
    else:
        add_todo(date, task, category)
        bot.send_message(message.chat.id, f'Task "{task}" with category "{category}" was added on {date}')


@bot.message_handler(commands=["print"])
def print_tasks(message):
    # /print Date1 Date2 ...
    splitted_command = message.text.split()
    for date in splitted_command[1:]:
        date = date.lower()
        text = ''
        if date in todos:
            for task in todos[date]:
                text = text + f'[{date}] {task[0]} @{task[1]}\n'
        else:
            text = f'You have no task on {date}'
        bot.send_message(message.chat.id, text)


bot.polling(none_stop=True)
