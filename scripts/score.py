class Score:
    calculated_score = 0

    def __init__(self):
        self.cur_score = 0
        self.cur_pos = 0
        self.actual_pos = 0
        
        file = open("highscore.txt", "r")
        self.highscore = int(file.read())
        file.close()
    
    def receive_pos(self, pos):
        self.cur_pos = pos
        self.calculate_score()

    def calculate_score(self):
        self.actual_pos += self.cur_pos
        self.cur_score = self.actual_pos / 50
        Score.calculated_score = self.cur_score

        # update all time high score if necessary
        if self.highscore < self.cur_score:
            self.highscore = self.cur_score
            file = open("highscore.txt", "w")
            file.write(str(int(self.cur_score)))
            file.close()
