# Copyright (c) 2024 Aiden Bohlander aka TheTridentGuy
# Released under GPL v3.0: https://www.gnu.org/licenses/gpl-3.0

class ChannelWrapper:
    def __init__(self, channel) -> None:
        self.channel = channel

    def chinput(self, prompt=""):
        self.channel.send(prompt)
        input_buffer = ''
        while True:
            while not self.channel.recv_ready():
                pass
            char = self.channel.recv(1024).decode("utf-8")
            if char == "\r":
                char = "\n\r"
                self.channel.send(char)
                return input_buffer
            self.channel.send(char)
            input_buffer += char

    def chprint(self, *args, sep=" ", end="\n\r"):
        output_buffer = sep.join(args)
        output_buffer = output_buffer + end
        self.channel.send(output_buffer)
