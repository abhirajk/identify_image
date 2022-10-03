from image_recognition.TargetShift import TargetShift
from queue import Queue

class AdjustServo:

    targetShifts: "Queue[TargetShift]" = Queue()

    def __init__(self):
       pass;

    def append(self, targetShift: TargetShift):
        self.targetShifts.put(targetShift);




