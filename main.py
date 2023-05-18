import tkinter
import customtkinter as ctk
import openai
import configparser
import json

config = configparser.ConfigParser()
config.read('config.ini')

openai.api_key = config.get('OpenAI', 'API_KEY')

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

# function to handle question asking
def ask_gpt3():
    question = user_question.get()
    topic = research_topic.get()
    combined_question = f"In the field of {topic}, {question}"
    
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": f"You are an expert and helpful research assistant in the field of {topic}."},
            {"role": "user", "content": combined_question}
        ]
    )
    response_content = response['choices'][0]['message']['content']
    
    # insert the response at the end of the text box
    response_box.insert(tkinter.END, response_content)


app = ctk.CTk()
app.title("Research Assistant")

# create an OptionMenu for research topics
research_topics = ["Physics", "Mathematics", "Computer Science", "Economics", "Biology", "Chemistry"]
research_topic = tkinter.StringVar(app)
research_topic.set(research_topics[0])  # default value
dropdown_menu = tkinter.OptionMenu(app, research_topic, *research_topics)
dropdown_menu.grid(row=0, column=0)

def add_topic_window():
    add_topic_window = ctk.CTkToplevel(app)
    add_topic_window.title("Add Research Topic")
    add_topic_window.resizable(False, False)
    #add_topic_window.geometry("300x300")

    window_title = ctk.CTkLabel(add_topic_window, text="Add Research Topic")
    window_title.grid(row=0, column=0, columnspan=2)

    new_topic_entry = ctk.CTkEntry(add_topic_window)
    new_topic_entry.grid(row=1, column=1)
    new_topic_label = ctk.CTkLabel(add_topic_window, text="New Research Topic:")
    new_topic_label.grid(row=1, column=0)

    def add_topic():
        new_topic = new_topic_entry.get()
        research_topics.append(new_topic)
        dropdown_menu['menu'].add_command(label=new_topic, command=tkinter._setit(research_topic, new_topic))
        add_topic_window.destroy()

    add_topic_button = ctk.CTkButton(add_topic_window, text="Add", command=add_topic)
    add_topic_button.grid(row=2, column=0)
    
    
    add_topic_window.grab_set()
    add_topic_window.mainloop()
# create an entry field for the question
user_question = tkinter.Entry(app)
user_question.grid(row=1, column=0)

add_research_topic_button = ctk.CTkButton(app, text="Add Research Topic", command=add_topic_window)
add_research_topic_button.grid(row=0, column=1)
# create a button to submit the question
submit_button = ctk.CTkButton(app, text="Ask", command=ask_gpt3)
submit_button.grid(row=2, column=0)

# create a text box for the response
response_box = tkinter.Text(app)
response_box.grid(row=4, column=0, columnspan=4)

app.mainloop()
