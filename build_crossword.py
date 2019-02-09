import json
import os, sys
import re
import pdb
import copy
import numpy as np
from nltk.corpus import words

NLTK_WORDS = words.words()

EMPTY_CHAR = "."
BOARD_HEIGHT = 5
BOARD_WIDTH = 5

SAFE_WORDS = ['divya$', 'conor$', 'tea$', 'ten$', 'rumya$', 'hansa$', 'anita$']


template_bard = ['.....',
				 '.....',
				 '.....',
				 '.....',
				 '.....']
class Board: 

	def __init__(self, board_state=None):
		self.board_state = board_state
		if board_state == None:
			self.board_state = [["X", "X", EMPTY_CHAR, EMPTY_CHAR, EMPTY_CHAR],
							    ["X", EMPTY_CHAR, EMPTY_CHAR, EMPTY_CHAR, EMPTY_CHAR],
							    [EMPTY_CHAR, EMPTY_CHAR, EMPTY_CHAR, EMPTY_CHAR, EMPTY_CHAR],
							    [EMPTY_CHAR, EMPTY_CHAR, EMPTY_CHAR, EMPTY_CHAR, "X"],
							    [EMPTY_CHAR, EMPTY_CHAR, EMPTY_CHAR, "X", "X"]]
		self.board_height = BOARD_HEIGHT
		self.board_width = BOARD_WIDTH

	def get_col(self, col_idx):
		return ''.join([self.board_state[i][col_idx] for i in range(self.board_height)])

	def get_row(self, row_idx):
		return ''.join(self.board_state[row_idx])

	def set_row(self, row_idx, row_str):
		# Returns NEW Board object
		new_board_state = copy.deepcopy(self.board_state)
		row_elements = list(row_str)
		for i in range(self.board_width):
			if new_board_state[row_idx][i] == "X":
				continue

			new_board_state[row_idx][i] = row_elements.pop(0)
		return Board(new_board_state)

	def get_empty_coord(self):

		row_no = [i for i,j in enumerate(self.board_state) if EMPTY_CHAR in j][0]
		col_no = [i for i,j in enumerate(self.board_state[row_no]) if j == EMPTY_CHAR][0]
		return (row_no, col_no)

	def contains_empty(self):
		return np.any([EMPTY_CHAR in row for row in self.board_state])

	def check_columns(self):
		for i in range(self.board_width):
			col_str = self.get_col(i)
			col_pattern = get_pattern(col_str)

			if col_pattern not in SAFE_WORDS and len(search(col_pattern)) == 0:
				return False
		return True

	def copy_board(self):
		return Board(self.board_state.copy())

	def __str__(self):
		to_str = ""
		for row in self.board_state:
			to_str += ''.join(row) + "\n"
		return to_str


template_1 = [["X", "X", EMPTY_CHAR, EMPTY_CHAR, EMPTY_CHAR],
			  ["X", EMPTY_CHAR, EMPTY_CHAR, EMPTY_CHAR, EMPTY_CHAR],
			  [EMPTY_CHAR, EMPTY_CHAR, EMPTY_CHAR, EMPTY_CHAR, EMPTY_CHAR],
			  [EMPTY_CHAR, EMPTY_CHAR, EMPTY_CHAR, EMPTY_CHAR, "X"],
			  [EMPTY_CHAR, EMPTY_CHAR, EMPTY_CHAR, "X", "X"]]

template_2 = [["X", EMPTY_CHAR, EMPTY_CHAR, EMPTY_CHAR, EMPTY_CHAR],
			  [EMPTY_CHAR, EMPTY_CHAR, EMPTY_CHAR, EMPTY_CHAR, EMPTY_CHAR],
			  [EMPTY_CHAR, EMPTY_CHAR, EMPTY_CHAR, EMPTY_CHAR, EMPTY_CHAR],
			  [EMPTY_CHAR, EMPTY_CHAR, EMPTY_CHAR, EMPTY_CHAR, EMPTY_CHAR],
			  [EMPTY_CHAR, EMPTY_CHAR, EMPTY_CHAR, EMPTY_CHAR, "X"]]

test_template_1 = [["X", "X", "r", EMPTY_CHAR, EMPTY_CHAR],["X", EMPTY_CHAR, "u", EMPTY_CHAR, EMPTY_CHAR],[EMPTY_CHAR, EMPTY_CHAR, "m", EMPTY_CHAR, EMPTY_CHAR],[EMPTY_CHAR, EMPTY_CHAR, "y", EMPTY_CHAR, "X"],[EMPTY_CHAR, EMPTY_CHAR, "a", "X", "X"]]


test_template_2 = [["r", "a", "g", "h", "a"],
				   ["u", EMPTY_CHAR, EMPTY_CHAR, EMPTY_CHAR, EMPTY_CHAR],
				   ["m", EMPTY_CHAR, EMPTY_CHAR, EMPTY_CHAR, EMPTY_CHAR],
				   ["y", EMPTY_CHAR, EMPTY_CHAR, EMPTY_CHAR, "X"],
				   ["a", EMPTY_CHAR, EMPTY_CHAR, "X", "X"],]

roommates = [["h", "a", EMPTY_CHAR, EMPTY_CHAR, EMPTY_CHAR],
			  ["a", "n", EMPTY_CHAR, EMPTY_CHAR, EMPTY_CHAR],
			  ["n", "i", "k", "k", "i"],
			  ["s", "t", EMPTY_CHAR, EMPTY_CHAR, EMPTY_CHAR],
			  ["a", "a", EMPTY_CHAR, EMPTY_CHAR, EMPTY_CHAR]]

roommates_2 = [["h", EMPTY_CHAR, EMPTY_CHAR, EMPTY_CHAR, "a"],
			  ["a", EMPTY_CHAR, EMPTY_CHAR, EMPTY_CHAR, "n"],
			  ["n", "i", "k", "k", "i"],
			  ["s", EMPTY_CHAR, EMPTY_CHAR, EMPTY_CHAR, "t"],
			  ["a", EMPTY_CHAR, EMPTY_CHAR, EMPTY_CHAR, "a"]]


def load_words():
    all_words = open("words.txt", "r").readlines()
    all_words.extend(open("names.txt", "r").readlines())
    all_words = filter(lambda x: len(x) < 6, all_words)
    all_words = [x.lower() for x in all_words]

    return all_words

def load_large_words():
    all_words = open("./english-words/words.txt").readlines()
    all_words.extend(open("names.txt", "r").readlines())
    all_words = [x.replace("\n", "") for x in all_words]
    all_words = filter(lambda x: len(x) < 6, all_words)
    all_words = filter(lambda x: len(x) > 1, all_words)
    all_words = filter(lambda x: x.isalpha(), all_words)
    all_words = [x.lower() for x in all_words]

    return all_words

def load_NLTK_words():
	all_words = NLTK_WORDS
	all_words.extend(open("names.txt", "r").readlines())
	all_words = filter(lambda x: len(x) < 6, all_words)
	all_words = filter(lambda x: len(x) > 2, all_words)

	all_words = filter(lambda x: x.isalpha(), all_words)
	all_words = [x.lower() for x in all_words]
	return all_words

def search(pattern):
	p = re.compile(pattern)
	return filter(p.match, ALL_WORDS)

def get_pattern(col_str):
	col_str = col_str.replace("X", "")
	col_str += "$"
	return col_str 

def fill_board(board):
	# Input: An empty board
	poss_boards = []

	row_idx, col_idx = board.get_empty_coord()
	row_str = board.get_row(row_idx)
	pattern = get_pattern(row_str)
	poss_words = search(pattern)
	for word in poss_words:
		new_board = board.set_row(row_idx, word)
		if new_board.check_columns():
			poss_boards.append(new_board)

	return poss_boards


ALL_WORDS = load_NLTK_words()
board_0 = Board(roommates_2)
unfinished_boards = [board_0]
finished_boards = []

fill_board(board_0)

while len(unfinished_boards) > 0 :
	curr_board = unfinished_boards.pop()
	if not curr_board.contains_empty():
		finished_boards.append(curr_board)
		continue

	poss_boards = fill_board(curr_board)
	unfinished_boards.extend(poss_boards)

	print "No. added boards: ", len(poss_boards)
	print "No. unfinished boards: ", len(unfinished_boards)
	print "No. finished boards: ", len(finished_boards)
	print

	if len(finished_boards) > 80:
		pdb.set_trace()
	

pdb.set_trace()









