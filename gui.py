# GUI to communicate with runscribe device over bluetooth
# I'm so sorry, it's a mess

from btle import BTLE
from fork import fork
import sys
import threading

def main(bt, child):
    devicelist = {}
    scribe = None
    print 'test'

    def update_list(devices):
        for device in devices:
            devicelist[device.name] = device
        names = [device.name for device in devices]
        child.writeobj("names")
        child.writeobj(names)

    bt.scan(update_list)
    while True:
        cmd = child.readobj()
        if cmd == "q":
            break
        elif cmd == "connect":
            name = child.readobj()
            device = devicelist[name]
            scribe = bt.connect_to(device)
        elif cmd == "light":
            scribe.write_packet("L" + chr(13) + "\x01\x00\xff\x00")
            scribe.read()
    bt.end()

child, parent = fork()
if child:
    bt = BTLE()
    threading.Thread(target=main, args=(bt, child)).start()
    bt.launch()
    child.close()
    sys.exit()

# Child Process
import Tkinter

class Application(Tkinter.Frame):
    def __init__(self, parent, master=None):
        Tkinter.Frame.__init__(self, master=master)
        self.parent = parent

        self.pack()
        quit = Tkinter.Button(self, text="Quit", command=self.quit_button)
        quit.pack()
        self.listbox = Tkinter.Listbox(self)
        self.listbox.pack()
        connect = Tkinter.Button(self, text="Connect", command=self.connect)
        connect.pack()

        self.names = []
        self.access_gui_built = False
        master.after(500, self.check_cmd)

    def quit_button(self):
        self.parent.writeobj("q")
        self.parent.close()
        self.quit()

    def connect(self):
        sel = self.listbox.curselection()
        if sel:
            name = self.names[sel[0]]
            self.parent.writeobj("connect")
            self.parent.writeobj(name)
            self.build_access_gui()

    def build_access_gui(self):
        if not self.access_gui_built:
            light = Tkinter.Button(self, text="Light LED", command=lambda: self.parent.writeobj("light"))
            light.pack()
            self.access_gui_built = True

    def check_cmd(self):
        try:
            cmd = self.parent.readobj(block=False)
            if cmd == "names":
                self.names = self.parent.readobj()
                self.listbox.delete(0, Tkinter.END)
                for name in self.names:
                    self.listbox.insert(Tkinter.END, name)
        except OSError: pass
        self.master.after(500, self.check_cmd)

root = Tkinter.Tk()
app = Application(parent, master=root)
app.mainloop()
root.destroy()