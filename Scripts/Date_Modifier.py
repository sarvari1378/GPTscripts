import uuid

class User:
    def __init__(self, name, date, tel_username=None):
        self.name = name
        self.date = date
        self.tel_username = tel_username

def read_users_from_file(filename):
    users = []
    with open(filename, 'r') as file:
        lines = file.readlines()[1:]  # Skip the first line
        for line in lines:
            parts = line.strip().split(', ')
            if parts[0]:  # check if line is not empty
                name = parts[0]
                date = int(parts[1])
                tel_username = parts[2] if len(parts) > 2 else None
                user = User(name, date, tel_username)
                users.append(user)
    return users

def write_users_to_file(users, filename):
    with open(filename, 'w') as file:
        unique_id = str(uuid.uuid4())[:6]  # Generate a unique identifier
        file.write(f"{unique_id}, 1\n")  # Write the new unique identifier at the beginning of the file
        for user in users:
            line = f"{user.name}, {user.date}"
            if user.tel_username:
                line += f", {user.tel_username}"
            file.write(line + '\n')

# Example of usage
users_file = 'Users.txt'
users = read_users_from_file(users_file)

for user in users:
    user.date = user.date - 1

write_users_to_file(users, users_file)
