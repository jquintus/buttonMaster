from digitalio import DigitalInOut, Direction, Pull
import board
import rotaryio
import time

class WhiteBoxDriver:

    def __init__(self, commands):
        self.commands = commands

    def initialize(self):
        # Set up buttons
        button_top_red = DigitalInOut(board.D12)
        button_top_red.direction = Direction.INPUT
        button_top_red.pull = Pull.UP

        button_bot_red = DigitalInOut(board.D11)
        button_bot_red.direction = Direction.INPUT
        button_bot_red.pull = Pull.UP

        button_top_yel = DigitalInOut(board.D10)
        button_top_yel.direction = Direction.INPUT
        button_top_yel.pull = Pull.UP

        button_bot_yel = DigitalInOut(board.D9)
        button_bot_yel.direction = Direction.INPUT
        button_bot_yel.pull = Pull.UP

        button_bot_grn = DigitalInOut(board.D6)
        button_bot_grn.direction = Direction.INPUT
        button_bot_grn.pull = Pull.UP

        button_top_grn = DigitalInOut(board.D5)
        button_top_grn.direction = Direction.INPUT
        button_top_grn.pull = Pull.UP

        self.buttons = [
            button_top_red, 
            button_bot_red, 
            button_top_yel, 
            button_bot_yel, 
            button_top_grn,
            button_bot_grn, 
        ]

        # Set up rotary encoder
        self.encoder = rotaryio.IncrementalEncoder(board.A1, board.A0)
        self.last_position = self.encoder.position
    
    def sync(self):

        buttons = self.buttons
        commands = self.commands

        for idx in range(len(buttons)):
            button = buttons[idx]
            if not button.value:
                cmd = commands[idx]
                cmd.onPress()
                time.sleep(0.4)

        # Rotary encoder (volume knob)
        current_position = self.encoder.position
        position_change = current_position - self.last_position
        if position_change > 0:
            for _ in range(position_change):
                cmd = commands[-2]
                cmd.onPress()

            print(current_position)

        elif position_change < 0:
            for _ in range(-1 * position_change):
                cmd = commands[-1]
                cmd.onPress()
            print(current_position)

        self.last_position = current_position


