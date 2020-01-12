import time
from iconizer import *



#print("je passe")
#



if __name__ == "__main__":
    print("looking for new file in:     " + cfg.scan_folder_path)    
    iUI = IconUi()    

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()