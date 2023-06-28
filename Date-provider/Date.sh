#!/bin/bash

file="Users.txt"
temp_file=$(mktemp)

while IFS=, read -r name days; do
    echo "$name, $((days - 1))"
done < "$file" > "$temp_file"

mv "$temp_file" "$file"
