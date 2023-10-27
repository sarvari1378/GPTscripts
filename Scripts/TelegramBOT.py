import json
import requests
import base64

# Define your group ID
group_id = "-1001693083938"
TOKEN = '6911644031:AAGWT-c1LTUd22AeV1Nob-YERQTo0nuOYhk'
URL = f"https://api.telegram.org/bot{TOKEN}/"

def get_updates(offset=None):
    url = URL + "getUpdates?timeout=100"
    if offset:
        url += f"&offset={offset}"
    response = requests.get(url)
    return json.loads(response.content)


def send_message(chat_id, text, reply_markup=None):
    url = URL + f"sendMessage?chat_id={chat_id}&text={text}"
    if reply_markup:
        url += f"&reply_markup={json.dumps(reply_markup)}"
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        message_ID = data.get('result', {}).get('message_id', None)
        if message_ID is not None:
            return message_ID
        else:
            print("Failed to retrieve message ID from the response.")
            return None
    else:
        print(f"Failed to send the message. Status code: {response.status_code}")
        return None

####################### my own functions
def delete_message(chat_id, message_id):
    url = URL + f"deleteMessage?chat_id={chat_id}&message_id={message_id}"
    response = requests.get(url)
    
    if response.status_code == 200:
        print(f"Message {message_id} deleted successfully.")
    else:
        print(f"Failed to delete message {message_id}. Status code: {response.status_code}")


def edit_message(chat_id, message_ID, new_text, reply_markup=None):
    
    url = URL + f"editMessageText?chat_id={chat_id}&message_id={message_ID}&text={new_text}"
    if reply_markup:
        url += f"&reply_markup={json.dumps(reply_markup)}"
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        if data.get('ok', False):
            return True
        else:
            print(f"Failed to edit the message. Error message: {data.get('description')}")
            return False
    else:
        print(f"Failed to edit the message. Status code: {response.status_code}")
        return False


def send_photo(chat_id, file_id, caption=None, reply_markup=None):
    url = URL + "sendPhoto"
    params = {
        'chat_id': chat_id,
        'photo': file_id,
    }
    if caption:
        params['caption'] = caption
    if reply_markup:
        params['reply_markup'] = json.dumps(reply_markup)
    
    response = requests.get(url, params=params)
    
    if response.status_code == 200:
        data = response.json()
        message_id = data.get('result', {}).get('message_id', None)
        
        if message_id is not None:
            return message_id
        else:
            print("Failed to retrieve message ID from the response.")
            return None
    else:
        print(f"Failed to send the photo message. Status code: {response.status_code}")
        return None

def add_line_to_github_file(username, date):
    file_path = "Users.txt"  # Replace with your desired file path

    try:
        # Define the content you want to add
        new_line = f"{username}, {date}\n"

        # Read the current content of the local file
        with open(file_path, "r") as file:
            current_content = file.read()

        # Split the content into lines
        lines = current_content.split("\n")
        updated_lines = []

        # Initialize Tarikh
        Tarikh = None

        # Search for the username and update or add the line
        for line in lines:
            parts = line.split(", ")
            if len parts == 2 and parts[0] == username:
                try:
                    # Try to convert the number to an integer
                    Tarikh = int(parts[1])
                except ValueError:
                    # Handle the case where the number is not a valid integer
                    print(f"Invalid number for {username}: {parts[1]}")
                continue  # Skip the line with the username
            updated_lines.append(line)

        # If Tarikh is not None, update the line
        if Tarikh is not None:
            plus = int(date) + Tarikh
            new_line = f"{username}, {plus}"

        # Add the new line
        updated_lines.append(new_line)

        # Join the lines back together
        new_content = "\n".join(updated_lines)

        # Write the updated content back to the local file
        with open(file_path, "w") as file:
            file.write(new_content)

        if Tarikh is not None:
            print(f"Updated line for {username} on {date} in {file_path}.")
        else:
            print(f"Added a new line for {username} on {date} in {file_path}.")
    except Exception as e:
        print(f"An error occurred: {e}")


def remove_line_from_github_file(username):
    # Set your GitHub personal access token and the repository details
    github_token = "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"
    repo_owner = "sarvari1378"
    repo_name = "GPTscripts"
    file_path = "Users.txt"

    # Get the current content of the file from the repository
    url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/contents/{file_path}"
    headers = {
        "Authorization": f"token {github_token}",
        "Accept": "application/vnd.github.v3+json"
    }
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        # Decode the file content
        file_content = response.json()
        current_content = base64.b64decode(file_content["content"]).decode("utf-8")

        # Split the content into lines
        lines = current_content.split("\n")

        # Create a new content with the line containing the username removed
        new_lines = [line for line in lines if username not in line]

        # Join the lines back together
        new_content = "\n".join(new_lines)

        # Encode the new content
        new_content_encoded = base64.b64encode(new_content.encode("utf-8")).decode("utf-8")

        # Create a commit with the updated content
        commit_message = f"Remove {username} from Users.txt"
        data = {
            "message": commit_message,
            "content": new_content_encoded,
            "sha": file_content["sha"]
        }
        response = requests.put(url, headers=headers, data=json.dumps(data))

        if response.status_code == 200:
            print(f"Removed {username} from Users.txt.")
        else:
            print("Failed to update the file.")
    else:
        print("Failed to retrieve the file.")

def RemainDays(username):
    # Set your GitHub personal access token and the repository details
    github_token = "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"
    repo_owner = "sarvari1378"
    repo_name = "GPTscripts"
    file_path = "Users.txt"

    # Get the current content of the file from the repository
    url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/contents/{file_path}"
    headers = {
        "Authorization": f"token {github_token}",
        "Accept": "application/vnd.github.v3+json"
    }
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        # Decode the file content
        file_content = response.json()
        current_content = base64.b64decode(file_content["content"]).decode("utf-8")

        # Split the content into lines
        lines = current_content.split("\n")

        # Search for the username and return the number after the comma
        for line in lines:
            parts = line.split(",")
            if len(parts) == 2 and parts[0].strip() == username:
                number = parts[1].strip()
                return int(number)  # Return as an integer

        # If the username was not found, return None
        return None
    else:
        return None


######## Lists
def Welcome_list(chat_id):
    inline_keyboard = [
        [
            {"text": "خرید سرویس", "callback_data": "welcome1"},
            {"text": "تمدید سرویس قدیمی", "callback_data": "welcome2"},
            {"text": "راهنمای استفاده از لینک ها", "callback_data": "welcome3"}
        ]
    ]
    reply_markup = {"inline_keyboard": inline_keyboard}
    text = "سلام به ربات خوش آمدید. من ربات دستیار ساجد هستم برای راحتی کار میتوانید به من مراجعه کنید. میخواهید چه کاری برایتان انجام بدهم؟"
    send_message(chat_id, text, reply_markup)

def Guide_list(chat_id):
    guides = [
        {"text": "ایفون برنامه Striisland", "callback_data": "Guide1"},
        {"text": "اندروید برنامه V2rayNG", "callback_data": "Guide2"},
        {"text": "لینک دانلود نرم افزارها", "callback_data": "Guide3"}
    ]

    inline_keyboard = []

    for guide in guides:
        inline_keyboard.append([guide])

    reply_markup = {"inline_keyboard": inline_keyboard}
    text = "راهنمای مورد نیاز شما کدام مورد است؟"
    send_message(chat_id, text, reply_markup)


def Correct_list(chat_id):
    guides = [
        {"text": "تایید", "callback_data": "correct1"},
        {"text": "عدم تایید", "callback_data": "correct2"}
    ]

    inline_keyboard = []

    for guide in guides:
        inline_keyboard.append([guide])

    reply_markup = {"inline_keyboard": inline_keyboard}
    text = "آیا واریزی بالا درست میباشد؟"
    send_message(chat_id, text, reply_markup)

def Plan_list(chat_id):
    inline_keyboard = [
        [
            {"text": "یک ماهه ۱۱۰ هزار تومان", "callback_data": "plan1"},
            {"text": "شش ماهه ۶۰۰ هزار تومان", "callback_data": "plan2"}
        ]
    ]
    reply_markup = {"inline_keyboard": inline_keyboard}
    text = "سرویس مورد نظر شما کدام است؟"
    send_message(chat_id, text, reply_markup)

#########

#######################

def handle_updates(updates):
    for update in updates["result"]:
        message_text = None
        chat_id = None
        username = None
        image = None  # Variable to store the user's image

        if "message" in update:
            message = update["message"]
            if "text" in message:
                message_text = message["text"]
            chat_id = message["chat"]["id"]
            username = message["from"]["username"]
            if 'photo' in message:
                # Save the user's image in the 'image' variable
                image = message['photo'][-1]['file_id']
        elif "callback_query" in update:
            message_text = update["callback_query"]["data"]
            chat_id = update["callback_query"]["message"]["chat"]["id"]
            username = update["callback_query"]["from"]["username"]

        if message_text == "/start":
            ######## welcome message first
            Welcome_list(chat_id)
            #########
        elif message_text == "welcome1":
           Plan_list(chat_id)

        elif message_text == "plan1":
            new_message = "لطفا فیش واریزی به شماره کارت ۶۰۳۷۹۹۱۹۳۴۶۷۳۶۳۷ با نام محمد ساجد سروری را ارسال بفرمایید."
            send_message(chat_id, new_message)
            add_line_to_github_file(username, '30')
        elif message_text == "plan2":
            new_message = "لطفا فیش واریزی به شماره کارت ۶۰۳۷۹۹۱۹۳۴۶۷۳۶۳۷ با نام محمد ساجد سروری را ارسال بفرمایید."
            send_message(chat_id, new_message)
            add_line_to_github_file(username, '180')
        elif image:
            new_message = f"فیش شما دریافت شد. لینک اشتراک شما برای شما ارسال خواهد شد. برای استفاده از لینک میتوانید از بخش راهنمای من (همین ربات) استفاده کنید."
            send_message(chat_id, new_message)
            
            # Build the URL with the user's username
            Sub_url = f"https://raw.githubusercontent.com/sarvari1378/GPTscripts/main/SUB/REALITY-{username}"
            
            send_message(chat_id, Sub_url)
            warning = "دقت کنید که این لینک در صورتی که به هر دلیلی فیش واریزی شما تایید نشود با اطلاع رسانی به شما از کار خواهد افتاد و بایستی برای خرید مجدد اقدام کنید."
            send_message(chat_id,warning)

            
            send_photo(group_id,image,'@' + username + '\n' + '\n' + Sub_url)
            Correct_list(group_id)
            ########## welcom messge duplicate
            Welcome_list(chat_id)
            ###########
        elif message_text == "correct2":

            remove_line_from_github_file(username)
            send_message(group_id,"حذف شد!")

        elif message_text == "correct1":
            send_message(group_id,"تایید شد")
        
        elif message_text == "welcome2":
            Plan_list(chat_id)
            Remain = RemainDays(username)


        elif message_text == "welcome3":
            Guide_list(chat_id)
        elif message_text == "Guide1":
            Guide_Link = "https://telegra.ph/آموزش-استفاده-از-نرم-افزار-Streisland-08-26"
            send_message(chat_id, Guide_Link)
        elif message_text == "Guide2":
            Guide_Link = "https://telegra.ph/آموزش-کار-با-نرم-افزار-V2rayNG-07-15"
            send_message(chat_id, Guide_Link)
        elif message_text == "Guide3":
            Guide_Link = "Streisland appstore: https://apps.apple.com/us/app/streisand/id6450534064"
            send_message(chat_id, Guide_Link)
            Guide_Link = "V2rayNG APK: https://github.com/2dust/v2rayNG/releases/download/1.8.9/v2rayNG_1.8.9.apk"
            send_message(chat_id, Guide_Link)
        else:
            new_message = "لطفا متن ارسال نکنید و از دکمه های ربات استفاده کنید." + message_text
            send_message(chat_id, new_message)
            
        

###########


def main():
    last_update_id = None
    while True:
        updates = get_updates(last_update_id)
        if len(updates["result"]) > 0:
            last_update_id = updates["result"][-1]["update_id"] + 1
            handle_updates(updates)

if __name__ == '__main__':
    main()
