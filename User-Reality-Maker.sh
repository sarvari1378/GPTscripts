#!/bin/bash

# Set the input file
input_file="users.txt"

# Set the output directory
output_dir="Users"

# Create the output directory if it doesn't exist
mkdir -p "$output_dir"

# Loop through each row in the input file
while IFS=", " read -r name age; do
  # Set the output file name based on the row name
  output_file="$output_dir/${name}"

  # Check if the value in the second column is 0
  if [[ "$age" -le "0" ]]; then
    # Write a custom message to the output file
    echo "vless://64694d4a-2c05-4ffe-aef1-68c0169cccb7@146.248.115.39:443?encryption=none&fp=firefox&mode=gun&pbk=TXpA-KUEqsg6YlZUXf0gZIe14rFjKZZNAqWzjruNoh8&security=reality&serviceName=&sid=790d3c76&sni=www.speedtest.net&spx=%2F&type=grpc#Your-subscription-has-ended." > "$output_file"
  else
    # Copy the template file to the output file
    cp template "$output_file"
  fi
done < "$input_file"
