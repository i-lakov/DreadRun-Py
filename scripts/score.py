class Score:
    calculated_score = 0

    def __init__(self):
        self._cur_score = 0
        self._cur_pos = 0
        self._actual_pos = 0
        
        file = open("highscore.txt", "r")
        self._highscore = int(file.read())
        file.close()
    
    def receive_pos(self, pos):
        self._cur_pos = pos
        self.calculate_score()

    def calculate_score(self):
        self._actual_pos += self._cur_pos
        self._cur_score = self._actual_pos / 50
        Score.calculated_score = self._cur_score

        # update all time high score if necessary
        if self._highscore < self._cur_score:
            self._highscore = self._cur_score
            file = open("highscore.txt", "w")
            file.write(str(int(self._cur_score)))
            file.close()
