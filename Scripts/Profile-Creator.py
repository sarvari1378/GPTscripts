# Import necessary libraries
from datetime import datetime
import requests
import pytz
import regex
from collections import namedtuple
import os
import base64
import json
import jdatetime
import binascii
from concurrent.futures import ThreadPoolExecutor, as_completed

# Add padding to base64 strings to ensure they are correctly formatted
def add_base64_padding(base64_string):
    padding_needed = 4 - (len(base64_string) % 4)
    if padding_needed:
        base64_string += "=" * padding_needed
    return base64_string

# Fetch the content of a URL
def fetch_url(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return url, response.text
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
    return url, None

# Fetch content from multiple URLs concurrently
def get_config(urls):
    responses = {}
    with ThreadPoolExecutor(max_workers=10) as executor:
        future_to_url = {executor.submit(fetch_url, url): url for url in urls}
        for future in as_completed(future_to_url):
            url, content = future.result()
            if content:
                responses[url] = content
    return responses

# Merge content from different sources and decode base64
def merge_content(responses):
    merged_content = ''
    for url in responses:
        content = responses[url]
        if content:
            try:
                # Decode the content from base64 and append it
                decoded_content = base64.b64decode(content).decode()
                merged_content += decoded_content + '\n'
            except Exception:
                # If decoding fails, append the raw content
                merged_content += content + '\n'
    return merged_content

# Extract a flag from the given line of text
def Simple_extract_flag(line):
    match = regex.search(r'\p{So}\p{So}', line)
    return match.group() if match else ''

# Extract flag from a 'vmess://' URL or a regular line of text
def extract_flag(line):
    if line.startswith('vmess://'):
        line = line[8:]
        line = add_base64_padding(line)
        try:
            # Decode the base64 string and extract the flag from the JSON payload
            line = json.loads(base64.b64decode(line).decode('utf-8'))
            flag = Simple_extract_flag(line["ps"])
        except (json.JSONDecodeError, binascii.Error):
            flag = ''
    else:
        flag = Simple_extract_flag(line)
    return flag

# Rename the 'ps' field in a 'vmess://' configuration
def Vmess_rename(vmess_config, new_name):
    vmess_data = vmess_config[8:]  # Remove 'vmess://' prefix
    vmess_data = add_base64_padding(vmess_data)  # Ensure proper padding
    try:
        # Decode, modify, and re-encode the configuration
        config = json.loads(base64.b64decode(vmess_data))
        config["ps"] = new_name
        encoded_data = base64.b64encode(json.dumps(config).encode()).decode()
        return "vmess://" + encoded_data
    except (json.JSONDecodeError, binascii.Error):
        return vmess_config  # Return unchanged configuration on error

# Rename configurations and add additional details
def rename_configs(content, name):
    lines = content.split('\n')
    new_lines = []
    now = datetime.now(pytz.timezone('Asia/Tehran'))
    hour = now.strftime('%H:%M')
    date = jdatetime.date.today().strftime('%Y-%m-%d')

    for i, line in enumerate(lines):
        if line.startswith('vmess://'):
            flag = extract_flag(line)
            new_name = f'|{flag}|{hour}|{date}|{name}|{i+1}|'
            line = Vmess_rename(line, new_name)
        elif '#' in line:
            flag = extract_flag(line)
            line = line.split('#')[0]
            line += f'#|{flag}|{hour}|{date}|{name}|{i+1}|'
        new_lines.append(line)
    return '\n'.join(new_lines)

# Remove a specified number of lines from the beginning of the content
def remove_lines(content, num):
    lines = content.split('\n')
    return '\n'.join(lines[num:])

# Retrieve user information from a URL
def get_users(url):
    response = requests.get(url)
    content = response.text.splitlines()
    
    User = namedtuple('User', ['username', 'date', 'telegram_id', 'preferd_Proctecol'])
    users = [User(*[item.strip() for item in line.split(',')]) for line in content if len(line.split(',')) >= 4]
    
    return users

# Write content to a specified file
def write_to_file(filename, content):
    with open(filename, 'w') as f:
        f.write(content)

# Create subscription files for users
def Create_SUBs(users, responses, protocol_name, links=None):
    if not os.path.exists('SUB'):
        os.makedirs('SUB')
    
    tasks = []
    
    if links is None:
        for user in users:
            if float(user.date) <= 0:
                content = 'vless://64694D4A-2C05-4FFE-AEF1-68C0169CCCB7@146.248.115.39:443?encryption=none&fp=firefox&mode=gun&pbk=TXpA-KUEqsg6YlZUXf0gZIe14rFjKZZNAqWzjruNoh8&security=reality&serviceName=&sid=790D3C76&sni=www.speedtest.net&spx=%2F&type=grpc#اشتراک شما به پایان رسیده است.'
            else:
                merged_content = merge_content(responses)
                content = rename_configs(merged_content, user.username)
                line = f'vless://64694D4A-2C05-4FFE-AEF1-68C0169CCCB7@146.248.115.39:443?encryption=none&fp=firefox&mode=gun&pbk=TXpA-KUEqsg6YlZUXf0gZIe14rFjKZZNAqWzjruNoh8&security=reality&serviceName=&sid=790D3C76&sni=www.speedtest.net&spx=%2F&type=grpc#|👤نام: {user.username}|⌛️روز های باقی مانده: {user.date}|'
                content = line + '\n' + content

            sub_filename = f'SUB/{protocol_name}-{user.username}'
            tasks.append((sub_filename, content))
            
            if protocol_name == user.preferd_Proctecol:
                main_filename = f'Major/{user.username}'
                tasks.append((main_filename, content))
    else:
        num_links = len(links)
        num_users = len(users)
        
        if num_links == 0:
            print(f"No links available for protocol: {protocol_name}")
            return

        users_per_link = num_users // num_links
        remainder = num_users % num_links

        user_index = 0
        for i, link in enumerate(links):
            if i >= num_links:
                break
            
            start_index = user_index
            end_index = user_index + users_per_link + (1 if i < remainder else 0)
            link_users = users[start_index:end_index]
            user_index = end_index
            
            if link in responses:
                content = responses[link]
            else:
                print(f"No content found for link: {link}")
                continue

            merged_content = merge_content({link: content})
            for user in link_users:
                if float(user.date) <= 0:
                    content = 'vless://64694D4A-2C05-4FFE-AEF1-68C0169CCCB7@146.248.115.39:443?encryption=none&fp=firefox&mode=gun&pbk=TXpA-KUEqsg6YlZUXf0gZIe14rFjKZZNAqWzjruNoh8&security=reality&serviceName=&sid=790D3C76&sni=www.speedtest.net&spx=%2F&type=grpc#اشتراک شما به پایان رسیده است.'
                else:
                    content = rename_configs(merged_content, user.username)
                    line = f'vless://64694D4A-2C05-4FFE-AEF1-68C0169CCCB7@146.248.115.39:443?encryption=none&fp=firefox&mode=gun&pbk=TXpA-KUEqsg6YlZUXf0gZIe14rFjKZZNAqWzjruNoh8&security=reality&serviceName=&sid=790D3C76&sni=www.speedtest.net&spx=%2F&type=grpc#|👤نام: {user.username}|⌛️روز های باقی مانده: {user.date}|'
                    content = line + '\n' + content

                filename = f'SUB/{protocol_name}-{user.username}'
                tasks.append((filename, content))

    # Use ThreadPoolExecutor to write files concurrently
    with ThreadPoolExecutor(max_workers=10) as executor:
        for filename, content in tasks:
            executor.submit(write_to_file, filename, content)

# Load configuration from a JSON file
json_file_path = 'Jsons/config.json'  # Adjust path as needed
with open(json_file_path, 'r') as f:
    config_data = json.load(f)

protocols = config_data['Protocol']

# Fetch user data
User_url = 'https://raw.githubusercontent.com/sarvari1378/GPTscripts/main/Users.txt'
users = get_users(User_url)

# Process each protocol configuration
for protocol in protocols:
    protocol_name = protocol['Name']
    protocol_links = protocol['Links']
    
    responses = get_config(protocol_links)
    
    if protocol.get('Split', False):
        Create_SUBs(users, responses, protocol_name, protocol_links)
        print(f"{protocol_name} is Split")
    else:
        Create_SUBs(users, responses, protocol_name)
        print(f"{protocol_name} is not split")
