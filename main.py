from customtkinter import *
import tkinter as tk
import openai

openai.api_key = 'YOUR-API-KEY'

def ask_gpt3(question):
    response = openai.ChatCompletion.create(
      model="gpt-3.5-turbo",
      messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": question}
        ]
    )
    return response['choices'][0]['message']['content']

class ResearchAssistant(CTkFrame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.create_widgets()

    def create_widgets(self):
        self.fields = ['Physics', 'Mathematics', 'Computer Science', 'Biology', 'Chemistry', 'Literature', 'History']
        self.field_var = tk.StringVar()
        self.field_var.set(self.fields[0]) # default value
        self.field_dropdown = CTkOptionMenu(self, self.field_var, *self.fields)
        self.field_dropdown.grid(row=0, column=0)

        self.question_entry = CTkEntry(self)
        self.question_entry.grid(row=1, column=0)

        self.ask_button = CTkButton(self, text="Ask", command=self.ask)
        self.ask_button.grid(row=1, column=1)

        self.response_text = tk.Text(self)
        self.response_text.grid(row=2, column=0, columnspan=2)

    def ask(self):
        field = self.field_var.get()
        question = self.question_entry.get()
        # Prepend the selected field to the question
        full_question = f"In the field of {field}, {question}"
        response = ask_gpt3(full_question)
        # Display the response in the text field
        self.response_text.delete(1.0, tk.END)
        self.response_text.insert(tk.END, response)

root = tk.PanedWindow()
app = ResearchAssistant(master=root)
app.mainloop()



