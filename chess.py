from tkinter import *
import time
from threading import Event

Stop_root = Event( )

PIECES = {"P":"♙","N":"♘","B":"♗","R":"♖","Q":"♕","K":"♔",
					"p":"♟","n":"♞","b":"♝","r":"♜","q":"♛","k":"♚", "ok":"ok"}

INVERTED_PIECES = {"♙": "P", "♘": "N", "♗": "B", "♖": "R", "♕": "Q", "♔": "K",
										 "♟": "p", "♞": "n", "♝": "b", "♜": "r", "♛": "q", "♚": "k", "ok":"ok"}

WHITE_PIECES = ["P","N","B","Q","R","K"]
BLACK_PIECES = ["p","n","b","q","k","r"]
ALL_PIECES  = WHITE_PIECES + BLACK_PIECES
EXPECTED_PIECES = ["ok"]

STARTING_CHESS_BOARD = [
	["r", "n", "b", "q", "k", "b", "n", "r"],
	["p", "p", "p", "p", "p", "p", "p", "p"],
	[" ", " ", " ", " ", " ", " ", " ", " "],
	[" ", " ", " ", " ", " ", " ", " ", " "],
	[" ", " ", " ", " ", " ", " ", " ", " "],
	[" ", " ", " ", " ", " ", " ", " ", " "],
	["P", "P", "P", "P", "P", "P", "P", "P"],
	["R", "N", "B", "Q", "K", "B", "N", "R"]
]
BLANK_BOARD = [
	[" ", " ", " ", " ", " ", " ", " ", " "],
	[" ", " ", " ", " ", " ", " ", " ", " "],
	[" ", " ", " ", " ", " ", "K", " ", "k"],
	[" ", " ", " ", " ", " ", " ", " ", " "],
	[" ", "Q", " ", " ", " ", " ", " ", " "],
	[" ", " ", " ", " ", " ", " ", " ", " "],
	[" ", " ", " ", " ", " ", " ", " ", " "],
	[" ", " ", " ", " ", " ", " ", " ", " "]
	]

STARTING_BOARD = STARTING_CHESS_BOARD
STARTING_BOARD = BLANK_BOARD



class CHESS:
	def __init__(self,root):
		self.root = root
		self.board_state = [row[:] for row in STARTING_BOARD]
		self.selected_btn = None
		
		self.highlight_color = "lightgreen"
		
		self.buttons = {}
		self.inboard = {}
		self.history = []
		self.opponent_move = []
		
		self.player_turn = WHITE_PIECES
		
		self.King_move = False
		self.Rook1_move = False
		self.Rook2_move = False
		self.king_move = False
		self.rook1_move = False
		self.rook2_move = False
		
		self.empasent_square = None
		self.king_in_check = False
		self.win_label = None
		
		self.testing = False
		self.board( )
	
	
	
	
	def creat_btn(self, parent):
		return Button(parent,
						image = self.pixels,
						font=("Arial",-int(self.size*0.7)),
						text = " ",
						fg = "black",
						padx =0,
						pady = 0,
						bd = 10,
						width = self.size,
						compound = "c",
						highlightthickness = 6,
						highlightbackground = "black",
						anchor = "c")
				
	def board(self):
		self.pixels = PhotoImage(width=1, height=1)
		screen_width = self.root.winfo_screenwidth( )
		self.size = screen_width//8
		self.top = self.size*4
		
		
				
		for row in range(8):
			for col in range(8):
				self.btn = self.creat_btn(self.root)
				self.btn.config(command = lambda r = row, c = col: self.move(r,c))
				
				self.buttons[(row, col)] = self.btn
				self.btn.place(x=col*self.size, y=self.top+row*self.size)
		
		self.history.append(self.board_state.copy( ))
		self.history[-1] = [row[:]for row in self.board_state]
		self.action_btns( )
		self.draw_pieces( )
		
		
	def update_inboard(self):
		for row in range(8):
			for col in range(8):
				if self.board_state[row][col] in ("K","k"):
					self.inboard[self.board_state[row][col]] = (row,col)
	
	
	def draw_pieces(self, board=None):
		if board is None:
			board = self.board_state
			
		for row in range(8):
			for col in range(8):
				pieces = board[row][col]
				self.buttons[(row,col)].config(text = str(PIECES.get(pieces," ")+ " "),
				bg = "#90BFFF" if (row + col)%2 else "#DAEFFF", fg = "#0A0002"
				)
		
		self.update_inboard( )
		self.blocked_square( )
		self.check_king( )
	
		
	
	def move(self, row, col):
		btn = self.buttons[(row,col)]
		self.clicked_piece = self.board_state[row][col]
		# First click
		
		if self.selected_btn is None:
			if self.clicked_piece != " ":
				if self.clicked_piece in self.player_turn:
					self.selected_btn = (row,col)
					btn.config(bg = "darkgreen")
					self.Pieces_Movements(row, col)
					
				
		else:
			selected_row, selected_col = self.selected_btn
			
			self.moved_piece= self.board_state[selected_row][selected_col]
			pieces = WHITE_PIECES if self.moved_piece in WHITE_PIECES else BLACK_PIECES
			self.selected_btn = None
			
			
			if (row,col) in self.moves:
				self.history.append([self.board_state.copy( ), self.King_move, self.Rook1_move,
												self.Rook2_move, self.king_move, self.rook1_move, self.rook2_move,
												self.king_in_check, self.empasent_square ])
												
				self.history[-1][0] = [row[:] for row in self.board_state]
				self.board_state[row][col] = self.moved_piece
				self.board_state[selected_row][selected_col] = " "
				
				
				if self.moved_piece in ("K","k"):
					if (self.moved_piece == "K" and not self.King_move) or (self.moved_piece == "k" and not self.king_move):
						if col - selected_col == 2:
							self.board_state[selected_row][selected_col+1] = "R" if self.moved_piece == "K" else "r"
							self.board_state[selected_row][selected_col+3] = " "
							
						if selected_col - col == 2:
							self.board_state[selected_row][selected_col-1] = "R" if self.moved_piece == "K" else "r"
							self.board_state[selected_row][selected_col-4] = " "
							
					if self.moved_piece == "K":
						self.King_move = True
					if self.moved_piece == "k":
						self.king_move = True
						
				self.king_in_check = False
				
				if self.board_state[7][0] != "R":
					self.Rook1_move = True
				if self.board_state[7][7] != "R":
					self.Rook2_move = True
				if self.board_state[0][0] != "r":
					self.rook1_move = True
				if self.board_state[0][7] != "r":
					self.rook2_move = True
				
				
				if (row,col) == self.empasent_square:
					if self.moved_piece == "p":
						self.board_state[row-1][col] = " "
					if self.moved_piece == "P":
						self.board_state[row+1][col] = " "
					
				self.empasent_square = None
					
				if self.moved_piece in ("P","p"):
					if self.moved_piece == "p":
						if row - selected_row == 2:
							if (row, col-1) in self.buttons and (self.board_state[row][col-1] == "P"):
								self.empasent_square = (row-1,col)
							if (row, col+1) in self.buttons and (self.board_state[row][col+1] == "P"):
								self.empasent_square = (row-1,col)
						
					
							
					else:
						if selected_row - row == 2:
							if (row, col-1) in self.buttons and (self.board_state[row][col-1] == "p"):
								self.empasent_square = (row+1,col)
							if (row, col+1) in self.buttons and (self.board_state[row][col+1] == "p"):
								self.empasent_square = (row+1,col)
				
				
				
			
				self.player_turn = BLACK_PIECES if self.player_turn == WHITE_PIECES else WHITE_PIECES
				
				self.update_inboard( )
				self.blocked_square( )
				own = "k" if self.player_turn == WHITE_PIECES else "K"
				attack = self.blocked_squares_by_black if own == "K" else self.blocked_squares_by_white
				if self.inboard[own] in attack:
					self.actions("⤺")
					self.draw_pieces( )
					return
				
				if self.moved_piece in ("p","P") and (row == 0 or row == 7):
					self.promoting_square = (row, col)
					self.promoting_color = "white" if self.moved_piece == "P" else "black"
					self.pawn_promotion( )
					
			self.draw_pieces( )

	
	
	def Pieces_Movements(self, row, col):
		self.moves = []
					
		
		color_piece = WHITE_PIECES if self.clicked_piece in WHITE_PIECES else BLACK_PIECES
		opponent_piece = WHITE_PIECES if self.clicked_piece not in WHITE_PIECES else BLACK_PIECES
		
		
		# ===== WHITE PAWN =====
		if self.clicked_piece == "P":
			if self.board_state[row-1][col] == " ":
				self.moves.append((row-1,col))
				
				if row == 6 and self.board_state[row-2][col] == " ":
					self.moves.append((row-2,col))

			if  (row-1, col-1) in self.buttons and (self.board_state[row-1][col-1] in BLACK_PIECES):
				self.moves.append((row-1,col-1))
					
			if (row-1, col+1) in self.buttons and (self.board_state[row-1][col+1] in BLACK_PIECES):
				self.moves.append((row-1,col+1))
			
		
			if self.empasent_square is not None and row == 3:
				er, ec = self.empasent_square
				if ((row, col+1) in self.buttons and "p" == self.board_state[row][col+1] and col+1 == ec):
					self.moves.append((er, ec))
						
				if ((row, col-1) in self.buttons and "p" == self.board_state[row][col-1] and col-1 == ec):
					self.moves.append((er, ec))
				
				
				
				
		# ====== BLACK PAWN =======
		elif self.clicked_piece == "p":
			if row+1 <= 7 and self.board_state[row+1][col] == " ":
				self.moves.append((row+1,col))
				
				if row == 1 and self.board_state[row+2][col] == " ":
					self.moves.append((row+2,col))
				
			
			if  (row+1, col-1) in self.buttons and (self.board_state[row+1][col-1] in WHITE_PIECES):
				self.moves.append((row+1,col-1))
					
			if  (row+1, col+1) in self.buttons and (self.board_state[row+1][col+1] in WHITE_PIECES):
				self.moves.append((row+1,col+1))
		
		
			if self.empasent_square is not None and row == 4:
				er, ec = self.empasent_square
				if ((row, col+1) in self.buttons and "P" == self.board_state[row][col+1] and col+1 == ec):
					self.moves.append((er, ec))
					
				if ((row, col-1) in self.buttons and "P" == self.board_state[row][col-1] and col-1 == ec):
					self.moves.append((er, ec))
		
		
		
		
		# ===== KNIGHT ======
		elif self.clicked_piece in ("N", "n"):
			knight_moves = [(row-2,col+1),(row-2,col-1),(row+2,col+1),(row+2,col-1),
										(row-1,col+2),(row+1,col+2),(row-1,col-2),(row+1,col-2)]
			
			for k in knight_moves:
				r, c = k[0], k[1]
				if k in self.buttons and self.board_state[r][c] not in color_piece:
					self.moves.append(k)
		
		
		
		
		# ==== (ROOK -- BISHOP -- QUEEN)=======
		elif self.clicked_piece in("R","r","B","b","Q","q"):
			directions = (1, 0),(0, 1),(-1, 0),(0, -1)
			if self.clicked_piece in ("B","b"):
				directions = (1, -1),(1, 1),(-1, 1),(-1, -1)
			if self.clicked_piece in ("Q","q"):
				directions = (1,0),(-1,0),(0,-1),(0,1),(1, -1),(1, 1),(-1, 1),(-1, -1)
			
			for dr, dc in directions:
				r, c = row+dr, col+dc
				while (r, c) in self.buttons:
					if self.board_state[r][c] in color_piece:
						break
					self.moves.append((r,c))
					if self.board_state[r][c] in opponent_piece:
						break
					r += dr
					c += dc
					

	
		
		#===== KING =====
		elif self.clicked_piece in ("K","k"):
			self.bsw = self.blocked_squares_by_white
			self.bsb = self.blocked_squares_by_black
			
			king_moves = [(row+1,col+1), (row+1,col-1), (row+1,col), (row, col+1),
									(row,col-1), (row-1, col), (row-1, col-1), (row-1, col+1)]
							
			for k in king_moves:
				r, c = k[0], k[1]
				if k in self.buttons and self.board_state[r][c] not in color_piece:
					if self.clicked_piece == "K":
						if k not in self.bsb:
							self.moves.append(k)
					
					else:
						if k not in self.bsw:
							self.moves.append(k)
			
			
			
			if not self.king_in_check:
				if self.clicked_piece == "K":
					if self.board_state[7][4] != "K":
						self.King_move = True
					if not self.King_move:
						if not self.Rook2_move:
							if ((row,col+1) not in self.bsb) and (self.board_state[row][col+1] == " "):
								if ((row,col+2) not in self.bsb) and (self.board_state[row][col+2] == " "):
									self.moves.append((row,col+2))
						
						if not self.Rook1_move:
							if ((row,col-1) not in self.bsb) and (self.board_state[row][col-1] == " "):
								if ((row,col-2) not in self.bsb) and (self.board_state[row][col-2] == " "):
									if (self.board_state[row][col-3] == " "):
										self.moves.append((row,col-2))
							
				else:
					if self.board_state[0][4] != "k":
						self.king_move = True
					if not self.king_move:
						if not self.rook2_move:		
							if ((row,col+1) not in self.bsw) and (self.board_state[row][col+1] == " "):
								if ((row,col+2) not in self.bsw) and (self.board_state[row][col+2] == " "):
									self.moves.append((row,col+2))
					
						if not self.rook1_move:
							if ((row,col-1) not in self.bsw) and (self.board_state[row][col-1] == " "):
								if ((row,col-2) not in self.bsw) and (self.board_state[row][col-2] == " "):
									if (self.board_state[row][col-3] == " "):
										self.moves.append((row,col-2))
		
		
		if self.testing:
			return
			
		for i in self.moves:
			self.buttons[(i)].config(bg = self.highlight_color)
		
		
	def blocked_square(self):
		self.blocked_squares_by_white = set( )
		self.blocked_squares_by_black = set( )
		for row in range(8):
			for col in range(8):
				
				
				# FOR PAWN
				if self.board_state[row][col] == "P":
					if (row-1, col+1) in self.buttons:
						self.blocked_squares_by_white.add((row-1, col+1))
					if (row-1, col-1) in self.buttons:
						self.blocked_squares_by_white.add((row-1, col-1))

				if self.board_state[row][col] == "p":
					if (row+1, col+1) in self.buttons:
						self.blocked_squares_by_black.add((row+1, col+1))
					if (row+1, col-1) in self.buttons:
						self.blocked_squares_by_black.add((row+1, col-1))
		
				
				# FOR KNIGHT
				if self.board_state[row][col] in ("N","n"):
					knight_moves = [(row-2,col+1),(row-2,col-1),(row+2,col+1),(row+2,col-1),
												(row-1,col+2),(row+1,col+2),(row-1,col-2),(row+1,col-2)]
					
					for i in knight_moves:
						if i in self.buttons:
							if self.board_state[row][col] == "N":
								self.blocked_squares_by_white.add(i)
							else:
								self.blocked_squares_by_black.add(i)
			
			
				# FOR ---- ROOK - BISHOP - QUEEN  ----
				if self.board_state[row][col] in ("R","B","Q","r","b","q"):
					if self.board_state[row][col] in ("R","r"):
						directions = (1, 0),(0, 1),(-1, 0),(0, -1)
					if self.board_state[row][col] in ("B","b"):
						directions = (1, -1),(1, 1),(-1, 1),(-1, -1)
					if self.board_state[row][col] in ("Q","q"):
						directions = (1,0),(-1,0),(0,-1),(0,1),(1, -1),(1, 1),(-1, 1),(-1, -1)
			
					for dr, dc in directions:
						r, c = row+dr, col+dc
						while (r, c) in self.buttons:
							if self.board_state[row][col].isupper( ):
								self.blocked_squares_by_white.add((r,c))
								if self.board_state[r][c] not in (" ", "k"):
									break
								
							else:
								self.blocked_squares_by_black.add((r,c))
								if self.board_state[r][c] not in (" ", "K"):
									break
									
							r += dr
							c += dc
				
				
				# FOR KING
				if self.board_state[row][col] in ("K", "k"):
					king_moves = [(row+1,col+1), (row+1,col-1), (row+1,col), (row, col+1),
											(row,col-1), (row-1, col), (row-1, col-1), (row-1, col+1)]
					
					for i in king_moves:
						if i in self.buttons:
							if self.board_state[row][col] == "K":
								self.blocked_squares_by_white.add(i)
							else:
								self.blocked_squares_by_black.add(i)
	
	
	
	def check_king(self):
		self.king_in_check = False
		self.King = None
		own = "K" if self.player_turn == WHITE_PIECES else "k"
		attacked = self.blocked_squares_by_black if own == "K" else self.blocked_squares_by_white
		
		if self.inboard[own] in attacked:
			self.king_in_check = True
			self.King = "White" if own == "K" else "Black"
			if not self.testing:
				self.buttons[self.inboard[own]].config(bg = "red")
		
		if not self.testing:
			self.find_legal_move( )
			
		if self.legal_move is None:	
			if self.win_label is None:
				if self.king_in_check:
					winner = "Black" if self.King == "White" else "White"
					text = winner + " Wins"
				
				else:
					text = "   it's Draw"
					
				self.action_frame.pack_forget( )
				
				win_frame = Frame(bg = "black")
				win_frame.pack(expand = True, fill = "both")
				
				self.win_label = Label(win_frame, bg = "black", fg = "white",
										text = text, font = ("Arial", 35, "bold"),
										)
				self.win_label.place(x = 30, y = 700)
				
				btn = self.creat_btn(win_frame)
				btn.config(width = 450, bg = "#900000",
									fg = "white", text = "EXIT",
									command = lambda: (exit( )))
				btn.pack(expand = True, side = "left")
				
				btn2 = self.creat_btn(win_frame)
				btn2.config(fg = "white", bg = "#900AAA", width=450, text = "Play Again", command = self.root.destroy)
				btn2.pack(expand=True, side="left")
			
	
	
	
	
	
	def delete_buttons(self, text):
		for i in self.pieces:
			if text not in ("ok"):
				self.promotion_btns[i].config(highlightbackground = "black")
				if INVERTED_PIECES[self.promotion_btns[i]["text"]] == text:
					self.promotion_btns[i].config(highlightbackground = "gold")
					self.selected_piece = text
			
				if self.promotion_btns[i]["text"] == "ok":
					self.promotion_btns[i].config(state = "normal")
				
			else:
				self.action_frame.pack(fill = "both", side = "bottom")
				r, c = self.promoting_square
				self.board_state[r][c] = self.selected_piece
				self.promotion_btns["bg"].destroy( )
				self.promotion_btns.clear( )
				self.draw_pieces( )
				return
	
	
	def pawn_promotion(self):
		self.promotion_btns = {}
		if self.promoting_color == "white":
			fg = "white"
			self.pieces = "N","B","R","Q","ok"
		else:
			self.pieces = "n","b","r","q","ok"
			fg = "black"
		
		self.action_frame.pack_forget( )
		promotion_frame = Frame(bg = "#000000")
		promotion_frame.pack( fill = "both", expand = True)
		
		self.promotion_btns["bg"] = promotion_frame
		
		for i in self.pieces:
			bgcolor = "#BBDEFB" if self.moved_piece == "p" else "#300FAF"
			btn = self.creat_btn(promotion_frame)
			btn.config(text = PIECES[i],
							width = 220,
							fg = fg,
							highlightthickness = 15,
							font=("Arial",-int(200*0.7)),
							bg = bgcolor,
							command = lambda t=i: self.delete_buttons(t))
			
			
			btn.pack(expand = True, side = "left")
			if i == "ok":
				btn.config(bg = "#900AAA",width = 400, font =("Arial", -int(200*0.5)), state = "disable")
				btn.place(x = 300, y = 1200)
			self.promotion_btns[i] = btn
	
	
	
	
	def actions(self, text):
		if text == "⟲":
			frame = Frame(bg = "black")
			frame.pack(fill = "both", expand = True)
			self.action_frame.pack_forget( )
			
			for i in range(2):
				label = Label(frame,bg = "black", fg = "white",
										text = "Do You Really Want To Restart The Game?",
										font = ("Arial",8,"bold"),
										highlightbackground = "white")
				label.place(x = 100, y = 880)
			
			label.config(text = "  ARE YOU SURE?", font = ("Arial",18,"bold"))
			label.place(x = 100, y = 750)
			
			btn = self.creat_btn(frame)
			btn.config(width = 400, bg = "#900000",
								fg = "white", text = "No",
								command = lambda: (frame.destroy( ), self.action_frame.pack(fill = "both", side = "bottom")))
			btn.pack(expand = True, side = "left")
			
			btn2 = self.creat_btn(frame)
			btn2.config(fg = "white", bg = "#900AAA", width=400, text = "YES", command = self.root.destroy)
			btn2.pack(expand=True, side="left")
		
		if text == "⤺":
			self.selected_btn = None
			if len(self.history) > 1:
				self.board_state = self.history[-1][0]
				
				self.King_move = self.history[-1][1]
				self.Rook1_move = self.history[-1][2]
				self.Rook2_move = self.history[-1][3]
				self.king_move = self.history[-1][4]
				self.rook1_move = self.history[-1][5]
				self.rook2_move = self.history[-1][6]
				self.king_in_check = self.history[-1][7]
				self.empasent_square = self.history[-1][8]
				
				self.player_turn = BLACK_PIECES if self.player_turn == WHITE_PIECES else WHITE_PIECES
				self.history.pop( )
				
				if self.win_label is not None:
					self.win_label.destroy( )
					self.win_label = None
				self.draw_pieces( )
				
			
	def action_btns(self):
		self.action_btns = {}
		
		self.action_frame = Frame(self.root, bg="black", height=100)
		self.action_frame.pack(side = "bottom", pady = 100, fill = "x")
		
		symbols = "⟲" ,"⤺"
		for i in symbols:
			btn = self.creat_btn(self.action_frame)
			btn.config(text = i,
								bg = "#900000",
								fg = "gold",
								font = ("Arial",-int(self.size)),
								bd = 15,
								width = 160,
								height = 150,
								highlightbackground = "gold",
								command = lambda t=i : self.actions(t))
			btn.pack(expand = True,side = "left")
			self.action_btns[i] = btn
	
	
	
	
	
	def find_legal_move(self):
		self.testing = True
		self.legal_move = None
		saved_board = self.board_state
		saved_piece = getattr(self, "clicked_piece", " ")
		saved_moves = getattr(self, "moves", [])
		saved_check = self.king_in_check
		own = "K" if self.player_turn == WHITE_PIECES else "k"
		
		try:
			for row in range(8):
				for col in range(8):
					piece = saved_board[row][col]
					if piece not in self.player_turn:
						continue
					
					self.board_state = saved_board
					self.clicked_piece = piece
					self.blocked_square( )
					self.Pieces_Movements(row, col)
					
					for r, c in list(self.moves):
						self.board_state = [x[:] for x in saved_board]
						self.board_state[r][c] = piece
						self.board_state[row][col] = " "
						self.blocked_square( )
						self.update_inboard( )
						
						attacked = self.blocked_squares_by_black if own == "K" else self.blocked_squares_by_white
						if self.inboard[own] not in attacked:
							self.legal_move = (piece, (r, c))
							return
		finally:
			self.board_state = saved_board
			self.blocked_square( )
			self.update_inboard( )
			self.clicked_piece = saved_piece
			self.moves = saved_moves
			self.king_in_check = saved_check
			self.testing = False
		
	
	
	

	
while True:
	root = Tk()
	root.config(bg="black")
	board = CHESS(root)
	mainloop() 
	