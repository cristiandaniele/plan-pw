# plan-pw project
Password manager for macOS.

Follow these steps to build some easy command line commands for the management of your password
## Edit configuration files
Open and edit the file **setting.json** adding:

1) in **pathFile** the path (and the file name) where you want to save your password. For example
> /Users/user123/Documents/encrypted_pw.txt

1) in **tmp_file_path** the path (and the file name) where you want to temporary save the crafted password. For example
> /Users/user123/Documents/tmp.txt

**Be careful, the document names MUST be different**
## Launch python script
1) Clone the repository in your laptop

2) Move to the project directory typing in your terminal: `cd <project_path>`

2) Install the project dependencies typing in your terminal:
`pip install -r requirements.txt`

3) Test the python script typing in your terminal: `python3 planpw.py -h`

If the script works, you will see the manual of the script in your terminal something like this:

    usage: python3 planpw.py [options] <flags>
        [options]:
            -get [tag]                      : get the password saved with [value] tag
            -set [tag]                      : add a new password with the tag [value]
            -find [string]                  : show all the tags matching with [string]
            -craft <flags>                  : craft a new password
                <-s>            -> allow special characters
                <-l> [lenght]   -> set password lenght
            -del [tag]                      : delete an existing password
            -h                              : show this manual
## 2. Create command line commands

Every following actions must be executed on these files:

- getpw
- setpw
- craftpw
- delpw
- findpw

### 2.1 Modify the files

Open every file and substitute **_project_path_here_** with **_you project file path_**

### 2.2 Copy the files

Copy every file to the folder **/usr/local/bin/**.

> You can access to this folder by typing in your terminal   
> **open /usr/local/bin/**

### 2.2 Make the file executable
To be able to use the commands, type in your terminal:

`sudo chmod +x /usr/local/bin/getpw`

`sudo chmod +x /usr/local/bin/setpw`

`sudo chmod +x /usr/local/bin/craftpw`

`sudo chmod +x /usr/local/bin/delpw`

`sudo chmod +x /usr/local/bin/findpw`

### 3. Enjoy your new commands

Open a terminal and use the commands.
