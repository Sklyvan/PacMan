import os

Files = os.listdir()
for FileName in Files:
    if "Ghost" in FileName:
        NewName = FileName.replace("Down", "DOWN")
        NewName = NewName.replace("Left", "LEFT")
        NewName = NewName.replace("Right", "RIGHT")
        NewName = NewName.replace("Up", "UP")
        os.rename(FileName, NewName)
        
