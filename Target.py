from Location import Location


class Target:
    def __init__(self, kind: str, score: float, location: Location):
        self.kind = kind;
        self.score = score;
        self.location = location;

    def __str__(self):
        return "{ kind: "+self.kind+", score: "+str(self.score)+", location: "+str(self.location)+" }";