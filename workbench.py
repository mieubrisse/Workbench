'''
Created on Feb 1, 2013
Main execution for the JarInstaller application
@author: Kevin Today
'''

import jardispenser
import sys
from Tkconstants import CURRENT

if __name__ == '__main__':
    """ Prints help information on a given topic, or general help if no topic is given """
    def help(topic):
        if topic == None or len(topic) == 0 or topic == "help":
            print(
                  """
                  Type 'help <command>' for specific help:\n
                      get     - Download a JAR file\n
                      use     - Use a downloaded JAR\n
                      list    - List all stored JARs\n
                  """)
        elif topic == "get":
            print(
                  """
                      Syntax: get <version name>\n
                      Use: Download the JAR file with <version name> and\n
                          store it so you can use it later.\n
                  """)
        else:
            print("No help available\n")
            
            
            
    """ Displays the given prompt and asks the user for a Y/n answer to return True/False respectively """
    def display_yes_no_prompt(prompt):
                response = raw_input(prompt + " [Y/n]: ")
                response = response.lower().strip()
                if response == "y" or response == "ye" or response == "yes":
                    return True
                else:
                    return False
                
                
    
    jar_dispenser = jardispenser.JarDispenser()  # Load model
    workbench_running = True
    
    # Read-eval-print loop to interact with system
    while workbench_running == True:
        # Grab, normalize, and split user input
        lower_user_input = raw_input("D-- ").lower()
        if len(lower_user_input) > 100:
            print("Input too long")
            continue
        input_words = lower_user_input.split()
        num_input_words = len(input_words)
        if num_input_words <= 0:
            continue
            
        command = input_words[0]
        
        ### TODO Command to disable the automatic push-update 
        
        # Download the given version if possible
        if command == "get":
            if num_input_words < 2:
                help("get")
                continue
            version_name = input_words[1]
            if version_name == None or len(version_name) == 0:
                print("Invalid version name")
                continue
            if version_name in jar_dispenser.list_versions():
                is_answer_yes = display_yes_no_prompt("You already have the version " + version_name + " JAR. Re-download it?")
                if not is_answer_yes:
                    continue
            try:
                jar_dispenser.download_jar(version_name)
            except BaseException as e:
                print("Error in downloading JAR: " + str(e))
                continue
            print("Successfully downloaded version " + " JAR")
            
        # Attempt to use given version and offer to download it if it isn't stored yet
        elif command == "use":
            if num_input_words < 2:
                help("use")
                continue
            version_name = input_words[1]
            if version_name == None or len(version_name) == 0:
                print("Invalid version name")
                continue
            if version_name not in jar_dispenser.list_versions():
                is_answer_yes = display_yes_no_prompt("You don't have a JAR of version " + version_name + ". Download and use it?")
                if not is_answer_yes:
                    continue
                try:
                    jar_dispenser.download_jar(version_name)
                except Exception as e:
                    print("Could not download JAR: " + str(e))
                    continue
                print("Successfully downloaded version " + version_name + " JAR")
            jar_dispenser.use_jar(version_name)
            print("Now using version " + version_name + " JAR")
            
        # List current binary version and all stored versions
        elif command == "list":
            current_version = jar_dispenser.current_version()
            versions_list = jar_dispenser.list_versions()
            output = "Current version: " + current_version + "\nStored versions: \n"
            for version in versions_list:
                output += "\t" + version + "\n"
            print(output)
            
        # Quit the REPL
        elif command == "quit" or command == "exit":
            workbench_running = False
            
        # Call help if nothing can be recognized
        else:
            help(None)
    
    