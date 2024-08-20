# MatrixLED

The matrix backpack is a simple 5x5 LED matrix.

## Python

It need the matrix library to work.

This matrix is using the GPIO protocol.

### Usage

Python example:

```python
import board # Import the board module
from matrix import MatrixLED # Import the matrix module

matrix = MatrixLED(board.IO2) # Create the matrix object

matrix.set_matrix_logo(matrix.logoHeart, (255, 0, 0)) # Set the heart logo with red color
```
