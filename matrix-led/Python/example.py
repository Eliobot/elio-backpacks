import board
from matrix import MatrixLED

# Initialize the Matrix LED
matrix = MatrixLED(board.IO2)

# Display a message
while True:
    matrix.scroll_matrix_text("Hello World!", (255, 0, 0))
