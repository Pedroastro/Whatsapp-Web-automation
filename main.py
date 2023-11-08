import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
import whatsapp_sender
import os

class WhatsappSenderGUI:
    def __init__(self, master):
        self.master = master
        master.title("WhatsApp Sender")

        # create a list to store the message and video entries
        self.message_entries = []
        self.video_n_image_entries = []
        self.document_entries = []
        self.actions = []

        # create label and button for adding message entries
        self.add_message_button = tk.Button(master, text="Add Message", command=self.add_message_entry, bg="#4CAF50",
                                            fg="white", font=("Helvetica", 12))
        self.add_message_button.pack(pady=10)

        # create label and button for adding video entries
        self.add_video_button = tk.Button(master, text="Add Video", command=self.add_video_entry, bg="#4CAF50",
                                          fg="white", font=("Helvetica", 12))
        self.add_video_button.pack(pady=10)

        # create label and button for adding video entries
        self.add_image_button = tk.Button(master, text="Add Image", command=self.add_image_entry, bg="#4CAF50",
                                          fg="white", font=("Helvetica", 12))
        self.add_image_button.pack(pady=10)

        # create label and button for adding video entries
        self.add_document_button = tk.Button(master, text="Add Document", command=self.add_document_entry, bg="#4CAF50",
                                          fg="white", font=("Helvetica", 12))
        self.add_document_button.pack(pady=10)

        # create label and button for removing actions
        self.remove_actions_button = tk.Button(master, text="Remove Action", command=self.remove_action, bg="#4CAF50",
                                             fg="white", font=("Helvetica", 12))
        self.remove_actions_button.pack(pady=10)

        # create label and button for selecting file
        self.file_label = tk.Label(master, text="Select file:", font=("Helvetica", 14))
        self.file_label.pack(pady=10)
        self.file_button = tk.Button(master, text="Choose Contacts File", command=self.select_file,
                                     font=("Helvetica", 12))
        self.file_button.pack(pady=10)

        # create button for sending messages
        self.send_button = tk.Button(master, text="Send Messages", command=self.send_messages, bg="#4CAF50", fg="white",
                                     font=("Helvetica", 14))
        self.send_button.pack(pady=20)

        # add a label for actions
        self.actions_label = tk.Label(master, text="Order of messages to send: ", font=("Helvetica", 14)).pack(pady=10)

    def remove_action(self):
        if len(self.actions) == 0:
            messagebox.showwarning("Warning", "No more actions included")
            return
        elif self.actions[-1] == "message":
            self.message_entries.pop()
            self.actions.pop()
            self.master.pack_slaves()[-1].pack_forget()
        elif self.actions[-1] == "video":
            self.video_n_image_entries.pop()
            self.actions.pop()
            self.master.pack_slaves()[-1].pack_forget()
        elif self.actions[-1] == "image":
            self.video_n_image_entries.pop()
            self.actions.pop()
            self.master.pack_slaves()[-1].pack_forget()
        elif self.actions[-1] == "document":
            self.document_entries.pop()
            self.actions.pop()
            self.master.pack_slaves()[-1].pack_forget()
        else:
            messagebox.showwarning("Warning", "Actions error")
            return

    def select_file(self):
        # open file dialog and get file path
        filepath = filedialog.askopenfilename(initialdir="/", title="Select File",
                                              filetypes=(("CSV files", "*.csv"), ("all files", "*.*")))
        # check if file is CSV
        if os.path.splitext(filepath)[1].lower().strip() != ".csv":
            messagebox.showwarning("Warning", "Please select a CSV file containing contacts.")
            return
        else:
            # update label with selected file path
            self.file_label.config(text="Selected file: " + filepath)

    def add_message_entry(self):
        # create a new message entry and pack it into the window
        message_entry = tk.Entry(self.master)
        message_entry.pack(pady=5)
        # add the new message entry to the list of message entries
        self.message_entries.append(message_entry)
        # add the new message entry to the list of actions
        self.actions.append("message")

    def add_video_entry(self):
        # open file dialog and get file path
        videopath = filedialog.askopenfilename(initialdir="/", title="Select File",
                                              filetypes=(("mp4 files", "*.mp4"), ("all files", "*.*")))
        # check if file is CSV
        if os.path.splitext(videopath)[1].lower().strip() != ".mp4":
            messagebox.showwarning("Warning", "Please select an mp4 file containing contacts.")
            return
        else:
            # create a new video entry and pack it into the window
            video_entry = tk.Label(self.master, text="Video: " + videopath, font=("Helvetica", 12))
            video_entry.pack(pady=5)
            # add the new video entry to the list of video entries
            self.video_n_image_entries.append(video_entry)
            # add the new video entry to the list of actions
            self.actions.append("video")

    def add_image_entry(self):
        # open file dialog and get file path
        imagepath = filedialog.askopenfilename(initialdir="/", title="Select File",
                                              filetypes=(("png files", "*.png"), ("jpeg files", "*.jpeg"), ("jpeg files", "*.jpg"), ("gif files", "*.gif"), ("pdf files", "*.pdf"), ("all files", "*.*")))
        # check if file is CSV
        imagetype = os.path.splitext(imagepath)[1].lower().strip()
        image_types = [".png", ".jpeg", ".jpg", ".gif", ".pdf"]
        if imagetype not in image_types:
            messagebox.showwarning("Warning", "Please select an image file containing contacts.")
            return
        else:
            # create a new video entry and pack it into the window
            image_entry = tk.Label(self.master, text="Image: " + imagepath, font=("Helvetica", 12))
            image_entry.pack(pady=5)
            # add the new video entry to the list of video entries
            self.video_n_image_entries.append(image_entry)
            # add the new video entry to the list of actions
            self.actions.append("image")

    def add_document_entry(self):
        # open file dialog and get file path
        filepath = filedialog.askopenfilename(initialdir="/", title="Select File",
                                               filetypes=(("all files", '*.*'), ))
        if filepath == "":
            messagebox.showwarning("Warning", "No file selected.")
            return
        else:
            # create a new video entry and pack it into the window
            document_entry = tk.Label(self.master, text="Document: " + filepath, font=("Helvetica", 12))
            document_entry.pack(pady=5)
            # add the new video entry to the list of video entries
            self.document_entries.append(document_entry)
            # add the new video entry to the list of actions
            self.actions.append("document")

    def send_messages(self):
        # check if file has been selected
        if self.file_label.cget("text") == "Select file:":
            messagebox.showwarning("Warning", "Please select a CSV file containing contacts.")
            return
        else:
            # get file path
            filepath = self.file_label.cget("text")[15:]
            # check if file is CSV
            if os.path.splitext(filepath)[1].lower() != ".csv":
                messagebox.showwarning("Warning", "Please select a CSV file containing contacts.")
                return
            else:
                # get messages and videos from entries
                messages = [entry.get() for entry in self.message_entries]
                videos = [entry.cget("text")[7:] for entry in self.video_n_image_entries]
                documents = [entry.cget("text")[10:] for entry in self.document_entries]
                actions = self.actions
                # call send_whatsapp_messages function with messages, videos, and file path
                whatsappBot = whatsapp_sender.whatsappBot()
                whatsappBot.send_messages(filepath, messages, videos, documents, actions)
                messagebox.showinfo("Success", "Messages sent successfully.")

root = tk.Tk()
root.geometry("800x600")
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x = (screen_width // 2) - (800 // 2)
y = (screen_height // 2) - (600 // 2)
root.geometry("+{}+{}".format(x, y))
app = WhatsappSenderGUI(root)
root.mainloop()