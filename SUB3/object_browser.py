from tkinter import *

# Takes a dictionary of items and creates a listbox for them
class Browser(Listbox):
    def __init__(self, frame, height, items, browser_type="Session", child_browser=None):

        # Create parent and check if a trial browser
        super().__init__(frame, selectmode=SINGLE if browser_type in
                         ["Session", "Block"] else MULTIPLE, height=height)
        self.items = items
        self.child_browser = child_browser

        self._load_items
        self.browser_type = browser_type


    def callback(self):
        selection = self.curselection()
        if selection:
            # Update our child with the newest data
            if self.browser_type == "Session":
                self.child_browser.update_items(
                    self.items[int(self.get(selection).split()[1])])

            elif self.browser_type == "Block":
                self.child_browser.update_items(
                    self.items[int(self.get(selection).split()[1])].trials)


    def update_items(self,new_items):
        if isinstance(new_items, list):
            new_items = {i: item for i, item in enumerate(new_items)}
        self.items = new_items
        self._load_items()

    def _load_items(self):
        self.delete(0, END)
        for key, _ in self.items.items():
            self.insert(key, f'{self.browser_type} {key}')


