# Folders synchroniser

### Project Description
The script creates a copy folder of the original folder and periodically updates it.

### Python version
The script was written in Python 3.10.7 with the use of build-in libraries.

### Running the Script
The program is run on the command line with four arguments: 

1. path of the folder
2. path of the synchronised copy folder
3. path of the log file
4. synchronisation interval in seconds

Example:

```
python main.py my_directory copy_my_directory log.txt 3
```

The program will run until interrupted within the terminal window.