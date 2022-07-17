import math


class Cell:
    def __init__(self, 
                 canvas, 
                 x: int, 
                 y: int, 
                 size: int, 
                 symbol: str):
        self.size = size
        self.canvas = canvas
        self.rect = self.canvas.create_rectangle(x, 
                                                 y, 
                                                 x + size, 
                                                 y + size, 
                                                 fill='white')

        font_size = math.ceil(size * 0.633)  # to fit inside the rectangle
        self.symbol = self.canvas.create_text(x + size // 2, 
                                              y + 3 * size // 5, 
                                              text=symbol, 
                                              font=('Helvetica', font_size), 
                                              fill='black')

    def move(self, x_amount: int, y_amount: int) -> None:
        """Move the Cell by x_amount (pixels) on the x axis 
        and y_amount (pixels) on the y axis. 
        """
        self.canvas.move(self.rect, x_amount, y_amount)
        self.canvas.move(self.symbol, x_amount, y_amount)

    def move_to(self, x: int, y: int) -> None:
        """Move the Cell to position (x, y). """
        self.canvas.coords(self.rect, 
                           x, 
                           y, 
                           x + self.size, 
                           y + self.size)

        self.canvas.coords(self.symbol, 
                           x + self.size // 2, 
                           y + 3 * self.size // 5)
