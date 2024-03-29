import interface
import wrappers


def example_callback(channel):
    channel = wrappers.ChannelWrapper(channel)
    n = channel.chinput("What's your name? ")
    print(f"[*] Their name is {n}")
    channel.chprint(f"Hello, {n}!")

intf = interface.SSHInterface("localhost", 5555, example_callback)
intf.start()
