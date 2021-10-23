import RPi.GPIO as GPIO
import time

class keyBoardInput:
    """
    Checks if a key is pressed on a keyboard (matching the keys from CHAR_MAP below).
    Returns the last pressed key when queried or None if no key was pressed
    """
    
    sleep = 0.1
    CHAR_MAP = [
        ["1","2","3","A"],
        ["4","5","6","B"],
        ["7","8","9","C"],
        ["*","0","#","D"],
    ]
    column = 0
    row = 0

    def __init__(self, portRow0: int, portRow1: int, portRow2: int, portRow3: int, portCol0: int, portCol1: int, portCol2: int, portCol3: int):
        self.isKeyPressed = 0
        self.rowPorts = [portRow0, portRow1, portRow2, portRow3]
        self.columnPorts = [portCol0, portCol1, portCol2, portCol3]

        #setup ports
        for rowPort in self.rowPorts:
            GPIO.setup(rowPort, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        for colPort in self.columnPorts:
            GPIO.setup(colPort, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        
        self.activate()

    def wasKeyPressed(self)->bool:
        return self.isKeyPressed >= 2

    def getInput(self) -> str:
        time.sleep(self.sleep)
        if(self.isKeyPressed >= 2):
            self.isKeyPressed = 0
            return self.CHAR_MAP[self.row][self.column]
        return None

    def activate(self, should_activate: bool = True) -> None:
        if (should_activate):
            for rowPort in self.rowPorts:
                GPIO.add_event_detect(rowPort, GPIO.RISING, callback=self.setRow, bouncetime=100)
            for colPort in self.columnPorts:
                GPIO.add_event_detect(colPort, GPIO.FALLING, callback=self.setColumn, bouncetime=100)
        else:
            for rowPort in self.rowPorts:
                GPIO.remove_event_detect(rowPort)
            for colPort in self.columnPorts:
                GPIO.remove_event_detect(colPort)

    def setRow(self, ev:int=None)->None:
        self.row = self.rowPorts.index(ev)
        self.isKeyPressed += 1

    def setColumn(self, ev:int=None)->None:
        self.column = self.columnPorts.index(ev)
        self.isKeyPressed += 1