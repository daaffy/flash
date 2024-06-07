import pandas as pd
import numpy as np
import random
from unidecode import unidecode

class card:
    """
        Flash card data structure.
    """

    def __init__(self, SIDE_A, SIDE_B, CATEGORY, NOTES, SIDE = "A"):

        # checks
        assert isinstance(SIDE_A, list)
        assert isinstance(SIDE_B, list)
        # ...
        
        # A
        self.LABEL_A = SIDE_A[0]
        self.CONTENT_A = SIDE_A[1]

        # B
        self.LABEL_B = SIDE_B[0]
        self.CONTENT_B = SIDE_B[1]

        if SIDE == "A":
            self.PRESENT = self._split(self.CONTENT_A)
            self.ANSWER_CONTENT = self.CONTENT_B
            self.ANSWER = self._split(self.CONTENT_B)
        elif SIDE == "B":
            self.PRESENT = self._split(self.CONTENT_B)
            self.ANSWER_CONTENT = self.CONTENT_A
            self.ANSWER = self._split(self.CONTENT_A)
        else:
            raise
        
        # check which mode to interpret '/'
        if len(self.PRESENT) == len(self.ANSWER):
            self.MODE = 0      # 1-1 matching
        elif len(self.PRESENT) == 1 or len(self.ANSWER) == 1:
            self.MODE = 1      # any

        self.CATEGORY = CATEGORY
        self.NOTES = NOTES
    
    def _split(self, input):
        """
            split raw text into list of components by '/'
            ensure lower case...
        """
        tmp = input.split("/")
        return [unidecode(x.lower().strip()) for x in tmp]

    def present(self):
        """
            Present the appropriate side.
        """

        # randomly present from list
        self.present_ind = np.random.choice(list(range(len(self.PRESENT))))
        print(self.PRESENT[self.present_ind])
    
    def print_notes(self):
        print(self.NOTES)

    def check(self, ans):
        """
            Check whether the answer is correct (up to formatting).
        """
        assert isinstance(ans, str)

        if self.MODE == 0:
            return unidecode(ans.lower().strip()) == self.ANSWER[self.present_ind]
        elif self.MODE == 1:
            return unidecode(ans.lower().strip()) in self.ANSWER
        else:
            raise

    def _format_str(self):
        0

class kernel:

    def __init__(self, PATH, SIDE="A", CATEGORY=None):
        self.list_all_cards = []

        self._load(PATH, SIDE = SIDE, CATEGORY = CATEGORY)
        self.correct = 0
        self.incorrect = 0

        self.exit_status = False

    def run_default(self, n = 20):
        self.total = n
        if len(self.list_all_cards) < n: 
            self.total = len(self.list_all_cards)

        sample_cards = random.sample(self.list_all_cards,self.total)

        incorrect_cards = []
        for i in range(len(sample_cards)):
            c = sample_cards[i]
            print(str(i+1)+"/"+str(len(sample_cards)), end=" ")

            res = self._case(c)

            if self.exit_status:
                break

            if res:   # correct
                print("(:")
                self.correct = self.correct + 1
            else:               # incorrect
                print(")-: " + c.ANSWER_CONTENT)
                self.incorrect = self.incorrect + 1
                incorrect_cards.append(c)
            
            print("")

        if self.correct + self.incorrect > 0:
            print(str(self.correct/(self.correct + self.incorrect)*100.)+" %")

        # repeat incorrects
        if len(incorrect_cards) == 0 or self.exit_status:
            return
        
        print("\nlet's try these again...\n")
        for i in range(len(incorrect_cards)):
            c = incorrect_cards[i]

            res = self._case(c)

            if self.exit_status:
                break

            if res:   # correct
                print("(:")
                self.correct = self.correct + 1
            else:               # incorrect
                print(")-: " + c.ANSWER_CONTENT)
                self.incorrect = self.incorrect + 1

    def _case(self, card):
        """
            A case is a flash card being presented, an answer, answer being checked, or interpreting special commands (e.g., *skip).
        """
        card.present()
        
        while True:
            ans = input("-> ") + " "
            # check for special
            if ans[0] == '*':
                if ans[1:].strip() == "notes":
                    print(card.NOTES)
                elif ans[1:].strip() == "cat":
                    print(card.CATEGORY)
                elif ans[1:].strip() == "exit":
                    self.exit_status = True
                    break
                else:
                    print("special command not recognised...")
            else:
                break
        
        return card.check(ans)

    def _load(self, PATH, SIDE = "A", CATEGORY = None):
        """
            Load .csv file into a list of card data-structures.
        """
        df = pd.read_csv(PATH)

        if not CATEGORY == None:
            assert isinstance(CATEGORY, str)
            df = df[df['category'] == CATEGORY]

        for _, row in df.iterrows():
            self.list_all_cards.append(
                card(
                    [df.columns[0], row.iloc[0]],
                    [df.columns[1], row.iloc[1]],
                    row.iloc[2],
                    row.iloc[3],
                    SIDE = SIDE
                )
                )
