import json
import requests
import base64
import random

# Define your group ID
group_id = "-1001693083938"
TOKEN = '6911644031:AAGWT-c1LTUd22AeV1Nob-YERQTo0nuOYhk'
URL = f"https://api.telegram.org/bot{TOKEN}/"
github_token = "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"
waiting_for_custom_username = False
custom_username = None
Custom = False
correct_array = []
notcorrect_array = []
sent_message_ids = []

def get_updates(offset=None):
    url = URL + "getUpdates?timeout=100"
    if offset:
        url += f"&offset={offset}"
    response = requests.get(url)
    return json.loads(response.content)

####def send_message(chat_id, text, reply_markup=None):
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

def send_message(chat_id, text, reply_markup=None):
    url = URL + f"sendMessage?chat_id={chat_id}&text={text}"
    if reply_markup:
        url += f"&reply_markup={json.dumps(reply_markup)}"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        message_ID = data.get('result', {}).get('message_id', None)
        if message_ID is not None:
            print(f"Message ID: {message_ID}")  # Print the message ID
            # Add the sent message ID to the list
            sent_message_ids.append(message_ID)
            return message_ID
        else:
            print("Failed to retrieve message ID from the response.")
            return None
    else:
        print(f"Failed to send the message. Status code: {response.status_code}")
        return None

def delete_message(chat_id, message_id):
    delete_url = f"https://api.telegram.org/bot{TOKEN}/deleteMessage?chat_id={chat_id}&message_id={message_id}"
    response = requests.get(delete_url)

    if response.status_code == 200:
        print(f"Message with ID {message_id} deleted successfully.")
    else:
        print(f"Failed to delete the message with ID {message_id}. Status code: {response.status_code}")

def search_last_message_by_phrase(chat_id, search_phrase):
    
    # Get chat updates
    get_updates_url = f"https://api.telegram.org/bot{TOKEN}/getUpdates?chat_id={chat_id}"
    response = requests.get(get_updates_url)

    last_message_id = None
    
    if response.status_code == 200:
        data = response.json()
        messages = data.get('result', [])

        for message in messages[::-1]:
            message_text = message.get('message', {}).get('text', '')

            if search_phrase in message_text:
                last_message_id = message.get('message', {}).get('message_id')
                break

    return last_message_id


####################### my own functions

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

#def send_photo(chat_id, file_id, caption=None, reply_markup=None):
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
    # Set your GitHub personal access token and the repository details
    repo_owner = "sarvari1378"
    repo_name = "GPTscripts"
    file_path = "Users.txt"

    # Define the content you want to add
    new_line = f"{username}, {date}\n"

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

        # Remove trailing newline character if it exists
        if current_content.endswith('\n'):
            current_content = current_content[:-1]

        # Split the content into lines
        lines = current_content.split("\n")
        updated_lines = []

        # Initialize Tarikh
        Tarikh = None

        # Search for the username and update or add the line
        for line in lines:
            parts = line.split(", ")
            if len(parts) == 2 and parts[0] == username:
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

        # Encode the new content
        new_content_encoded = base64.b64encode(new_content.encode("utf-8")).decode("utf-8")

        # Create a commit with the updated content
        commit_message = f"Update or add {username},{date} in Users.txt"
        data = {
            "message": commit_message,
            "content": new_content_encoded,
            "sha": file_content["sha"]
        }
        response = requests.put(url, headers=headers, data=json.dumps(data))

        if response.status_code == 200:
            if Tarikh is not None:
                print(f"Updated line for {username} on {date} in Users.txt.")
            else:
                print(f"Added new line for {username} on {date} in Users.txt.")
        else:
            print("Failed to update the file.")
    else:
        print("Failed to retrieve the file.")

def remove_line_from_github_file(username):
    # Set your GitHub personal access token and the repository details

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

def trigger_github_workflow():
    repo_owner = "sarvari1378"
    repo_name = "GPTscripts"
    workflow_name = "Creator_manual"

    
    headers = {
        "Authorization": f"token {github_token}"
    }

    # Define the workflow file name
    workflow_file = f"{workflow_name}.yml"

    # Define the workflow dispatch endpoint
    workflow_dispatch_url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/actions/workflows/{workflow_file}/dispatches"

    payload = {
        "ref": "main"  # Specify the branch where the workflow is located
    }

    response = requests.post(workflow_dispatch_url, headers=headers, json=payload)

    if response.status_code == 204:
        print(f"Successfully triggered the '{workflow_name}' workflow.")
    else:
        print(f"Failed to trigger the workflow. Status code: {response.status_code}")
        print(response.text)

######## Lists
def Welcome_list(chat_id):
    inline_keyboard = [
        [
            {"text": "خرید سرویس", "callback_data": "welcome1"},
            {"text": "تمدید سرویس قدیمی", "callback_data": "welcome2"},
            {"text": "راهنما", "callback_data": "welcome3"}
        ]
    ]
    reply_markup = {"inline_keyboard": inline_keyboard}
    text = "سلام به ربات خوش آمدید. من ربات دستیار ساجد هستم برای راحتی کار میتوانید به من مراجعه کنید. میخواهید چه کاری برایتان انجام بدهم؟"
    send_message(chat_id, text, reply_markup)

def Guide_list(chat_id):
    guides = [
        {"text": "ایفون برنامه Striisland", "callback_data": "Guide1"},
        {"text": "اندروید برنامه V2rayNG", "callback_data": "Guide2"},
        {"text": "لینک دانلود نرم افزارها", "callback_data": "Guide3"},
        {"text": "راهنمای اطلاع از فعال شدن لینک", "callback_data": "Guide4"}
    ]

    inline_keyboard = []

    for guide in guides:
        inline_keyboard.append([guide])

    reply_markup = {"inline_keyboard": inline_keyboard}
    text = "راهنمای مورد نیاز شما کدام مورد است؟"
    send_message(chat_id, text, reply_markup)

def Correct_list(chat_id, message_id):
    guides = [
        {"text": "تایید", "callback_data": f"correct{message_id}"},
        {"text": "عدم تایید", "callback_data": f"notcorrect{message_id}"}
    ]

    inline_keyboard = []

    for guide in guides:
        inline_keyboard.append([guide])

    reply_markup = {"inline_keyboard": inline_keyboard}
    text = "آیا واریزی بالا درست میباشد؟"
    correct_array.append(f"correct{message_id}")
    notcorrect_array.append(f"notcorrect{message_id}")
    message_id = send_message(chat_id, text, reply_markup)

    # Return the message_id after sending the message
    return message_id

def Plan_list(chat_id):
    inline_keyboard = []

    # Define your plan options with text and callback_data
    plan_options = [
        {"text": "(برای خودم) یک ماهه ۱۱۰ هزار تومان", "callback_data": "plan1"},
        {"text": "(برای خودم) شش ماهه ۶۰۰ هزار تومان", "callback_data": "plan2"},
        {"text": "(برای دیگران) یک ماهه ۱۱۰ هزار تومان", "callback_data": "plan3"},
        {"text": "(برای دیگران) شش ماهه ۶۰۰ هزار تومان", "callback_data": "plan4"}
    ]

    # Calculate the width for each button dynamically
    button_width = max(len(option["text"]) for option in plan_options)

    # Create inline keyboard with adjusted button width
    for option in plan_options:
        inline_keyboard.append([{"text": option["text"], "callback_data": option["callback_data"]}])

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
        global waiting_for_custom_username
        global custom_username
        global Custom

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

        elif message_text == "plan3":
            # Set the flag to indicate that we are waiting for the custom username.
            waiting_for_custom_username = True
            custom_username = None
            Custom = True
            new_message = "نام کاربری دلخواه خود را وارد کنید."
            send_message(chat_id, new_message)
        
        elif waiting_for_custom_username:
            # If we are waiting for the custom username, store it in the custom_username variable and add it to GitHub.
            custom_username = message_text
            add_line_to_github_file(custom_username, '30')
            new_message = "لطفا فیش واریزی به شماره کارت ۶۰۳۷۹۹۱۹۳۴۶۷۳۶۳۷ با نام محمد ساجد سروری را ارسال بفرمایید."
            send_message(chat_id,new_message)
            waiting_for_custom_username = False

        elif message_text == "plan4":
            # Set the flag to indicate that we are waiting for the custom username.
            waiting_for_custom_username = True
            custom_username = None
            Custom = True
            new_message = "نام کاربری دلخواه خود را وارد کنید."
            send_message(chat_id, new_message)
        
        elif waiting_for_custom_username:
            # If we are waiting for the custom username, store it in the custom_username variable and add it to GitHub.
            custom_username = message_text
            add_line_to_github_file(custom_username, '180')
            new_message = "لطفا فیش واریزی به شماره کارت ۶۰۳۷۹۹۱۹۳۴۶۷۳۶۳۷ با نام محمد ساجد سروری را ارسال بفرمایید."
            send_message(chat_id,new_message)
            waiting_for_custom_username = False        

        elif image:
            new_message = f"فیش شما دریافت شد. لینک اشتراک شما برای شما ارسال خواهد شد. برای استفاده از لینک میتوانید از بخش راهنمای من (همین ربات) استفاده کنید."
            send_message(chat_id, new_message)
            
            # Build the URL with the user's username
            if Custom:
                Sub_url = f"https://raw.githubusercontent.com/sarvari1378/GPTscripts/main/SUB/REALITY-{custom_username}"
                Custom = False
            else:
                Sub_url = f"https://raw.githubusercontent.com/sarvari1378/GPTscripts/main/SUB/REALITY-{username}"

            send_message(chat_id, Sub_url)
            Randomtime = round(random.uniform(4, 6), 1)
            Space = '\n'
            warning = f"دقت کنید که این لینک در صورتی که به هر دلیلی فیش واریزی شما تایید نشود با اطلاع رسانی به شما از کار خواهد افتاد و بایستی برای خرید مجدد اقدام کنید {Space}{Space} در ضمن اگر برای اولین باره که از این سرویس استفاده میکند لینکی که برای شما ارسال شده تا {Randomtime} دقیقه دیگرفعال نخواهد شد و بایستی منتظر بمانید. برای اطمینان از فعال شدن لینک میتوانید از بخش راهنمای من (همین ربات) استفاده کنید."
            send_message(chat_id,warning)

            
            PhotoID = send_photo(group_id,image,'@' + username + '\n' + '\n' + Sub_url)
            delete_message(chat_id,PhotoID)
            
            CorrectID = Correct_list(group_id,PhotoID)

            ########## welcom messge duplicate
            Welcome_list(chat_id)
            ###########
        
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
            ilo = search_last_message_by_phrase(chat_id,'V2rayNG')
            send_message(chat_id, ilo)
            
        elif message_text == "Guide4":
            
            message_text = "روی لینک تهیه شده کلیک کنید تا در صفحه مرور گر باز شود. اگر صفحه ای پر از نوشته های انگلیسی مشاهده کردید لینک شما فعال شده اما اگر با صفحه ای خالی از نوشته مواجه شدید لینک هنوز فعال نشده است و بایستی منتظر بمانید."
            send_message(chat_id,message_text)

        elif message_text in correct_array:
            extracted_value = message_text[len("correct"):]
            delete_message(chat_id,extracted_value)
            send_message(group_id,"تایید شد")
        
        elif message_text in notcorrect_array:
            send_message(group_id,"یوز حذف شد")
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
