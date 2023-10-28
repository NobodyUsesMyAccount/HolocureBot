import time
import pyautogui
import keyboard
import numpy as np

class FishingBot:
    def __init__(self):
        self.judgement_region = (1120,755,150,1)
        self.ok_region = (831,820,255,1)
        self.key = np.array(("z","up","down","left","right"))
        self.key_color = np.array(((174,49,208),(225,50,50),(52,145,247),(246,198,67),(45,234,43)))
        self.ok_color = np.array(((255,255,255)))
        self.instruction_pointer = 0
    
    def start(self):
        self.__run()
    
    def __run(self):
        state = False
        while not keyboard.is_pressed("q"):
            if state == True:
                self.fishing_interface()
            else:
                pass
            
            if keyboard.is_pressed("e"):
                state = not state
                if state:
                    print("Fishing bot activated")
                    time.sleep(1)
                else:
                    print("Fishing bot deactivated")
                    time.sleep(1)
        print("Program Ended")
    
    def capture(self,region):
        return np.array(pyautogui.screenshot(region=region))
    
    def fishing_interface(self):
        if self.instruction_pointer == 0:
            self.start_fisiing()
            self.instruction_pointer += 1
        elif self.instruction_pointer == 1:
            self.auto_rythm()
        elif self.instruction_pointer == 2:
            self.stop_fishing()
            time.sleep(0.5)
            self.instruction_pointer = 0
    
    def start_fisiing(self):
        print("Fishing Started")
        self.press("z")
    
    def stop_fishing(self):
        print("Fishing Ended, Continuing...")
        self.press("z")
    
    def auto_rythm(self):
        key = self.get_key()
        ok = self.get_ok_popup()
        if key != None:
            self.press(key)
            print(key)
        if ok:
            self.instruction_pointer += 1
    
    def get_key(self):
        x = self.capture(self.judgement_region)
        cond = self.key_color
        futures = np.zeros((cond.shape[0],x.shape[1])).astype("bool")

        for i in np.arange(cond.shape[0]):
            test = cond[i]
            out = np.abs(x.squeeze(axis=0) - test)
            result = out.sum(axis=1)/(255+255+255)
            #print(result)
            
            for j in np.arange(out.shape[0]):
                if result[j] < 0.05:
                    futures[i][j] = True
                    
        futures = futures.sum(axis=1).astype("bool")
        index = np.where(futures == True)[0]
        return self.key[index[0]] if index.size > 0 else None
        #print(futures)
    
    def get_ok_popup(self):
        x = self.capture(self.ok_region)
        cond = self.ok_color
        futures = np.zeros((x.shape[1],)).astype("bool")

        test = cond
        out = np.abs(x.squeeze(axis=0) - test)
        result = out.sum(axis=1)/(255+255+255)
        #print(result)

        for j in np.arange(out.shape[0]):
            if result[j] < 0.05:
                futures[j] = True
                    
        futures_size = futures.size
        confidence = futures.sum()/futures_size
        return True if confidence > 0.2 else None
    
    def press(self,key):
        keyboard.press(key)
        time.sleep(0.1)
        keyboard.release(key)

if __name__ == "__main__":
    test = FishingBot()
    test.start()
    #print(test.capture(test.ok_region))