# TODO UI
from game import Game

game = Game()
# game._send_data("jgiluguyvouibu")
if game.authorize("asdasdas", "asdadasdasd"):
	print('authorized')

if game.create_session():
	print('session created')

if game.ready_to_start_game():
	if game.turn:
		print('белые')
	else:
		print('черные')

game.play()