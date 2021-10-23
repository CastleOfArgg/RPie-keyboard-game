import RPi.GPIO as GPIO
import time

class keyBoardInput:
    """
    
    """
    CHAR_MAP = [
        ["1","2","3","A"],
        ["4","5","6","B"],
        ["7","8","9","C"],
        ["*","0","#","D"],
    ]
    TIME = 0.001

    def __init__(self, portRow0: int, portRow1: int, portRow2: int, portRow3: int, portCol0: int, portCol1: int, portCol2: int, portCol3: int):
        self.isKeyPressed = False
        self.rowPorts = [portRow0, portRow1, portRow2, portRow3]
        self.columnPorts = [portCol0, portCol1, portCol2, portCol3]

        #setup ports
        for rowPort in self.rowPorts:
            GPIO.setup(rowPort, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        for colPort in self.colPorts:
            GPIO.setup(colPort, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        
        self.activate()

    def wasKeyPressed(self)->bool:
        return self.isKeyPressed

    def getInput(self) -> str:
        time.sleep(self.TIME)
        if(self.isKeyPressed):
            return self.CHAR_MAP[self.row][self.column]
        return None

    def activate(self, should_activate: bool = True) -> None:
        if (should_activate):
            for rowPort in self.rowPorts:
                GPIO.add_event_detect(rowPort, GPIO.RISING, callback=self.setRow, bouncetime=100)
            for colPort in self.colPorts:
                GPIO.add_event_detect(colPort, GPIO.FALLING, callback=self.setColumn, bouncetime=100)
        else:
            for rowPort in self.rowPorts:
                GPIO.remove_event_detect(rowPort)
            for colPort in self.colPorts:
                GPIO.remove_event_detect(colPort)

    def setRow(self, ev:int=None)->None:
        self.row = ev
        self.isKeyPressed = True

    def setColumn(self, ev:int=None)->None:
        self.column = ev