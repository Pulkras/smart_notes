from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QListWidget, QApplication, QWidget, QMessageBox, QHBoxLayout, QVBoxLayout, QGroupBox, QButtonGroup, QRadioButton, QPushButton, QLabel, QLineEdit, QTextEdit, QInputDialog)
import json
app = QApplication([])
notes = {
    "Добро пожаловать!": {
        "текст": "В этом приложении можно создавать теги с инструкциями...",
        "теги": ["Инструкция", "Умные заметки"]
    }
}
with open("notes_data.json", 'w', encoding='utf-8') as file:
    json.dump(notes, file)
'''Интерфейс приложения'''
# параметры окна приложения
window = QWidget()
window.setWindowTitle('Умные заметки')
window.resize(900, 600)

#виджеты окна приложения
list_notes = QListWidget()
list_notes_label = QLabel("Список заметок")

button_note_create = QPushButton("Создать заметку") # появляется окно с полем "введите заметку"
button_note_del = QPushButton("Удалить заметку")
button_note_save = QPushButton("Сохранить заметку")



field_tag = QLineEdit('')
field_tag.setPlaceholderText("Введите тег...")
field_text = QTextEdit()
button_tag_add = QPushButton("Добавить к заметке")
button_tag_del = QPushButton("Открепить от заметки")
button_tag_search = QPushButton("Искать заметку по тегу")
list_tags = QListWidget()
list_tags_label = QLabel("Список тегов")
note_layout = QVBoxLayout()
first_layout = QHBoxLayout()
error = QMessageBox()
second_layout = QHBoxLayout()
third_layout = QHBoxLayout()
fourth_layout = QHBoxLayout()
field_tag_layout = QHBoxLayout()
taglist_layout = QHBoxLayout()
listtags_layout = QHBoxLayout()
fifth_layout = QHBoxLayout()
sixth_layout = QHBoxLayout()
first_layout.addWidget(field_text)
second_layout.addWidget(list_notes)
third_layout.addWidget(button_note_create)
third_layout.addWidget(button_note_del)
third_layout.addWidget(button_note_save)
fourth_layout.addWidget(field_tag)
field_tag_layout.addWidget(field_tag)
taglist_layout.addWidget(list_tags_label)
listtags_layout.addWidget(list_tags)
fifth_layout.addWidget(button_tag_add)
fifth_layout.addWidget(button_tag_del)
sixth_layout.addWidget(button_tag_search)
note_layout.addLayout(first_layout)
note_layout.addWidget(list_notes_label)
note_layout.addLayout(second_layout)
note_layout.addLayout(third_layout)
note_layout.addLayout(field_tag_layout)
note_layout.addLayout(taglist_layout)
note_layout.addLayout(listtags_layout)
note_layout.addLayout(fifth_layout)
note_layout.addLayout(sixth_layout)
window.setLayout(note_layout)
def show_note():
    name = list_notes.selectedItems()[0].text()
    field_text.setText(notes[name]['текст'])
    list_tags.clear()
    list_tags.addItems(notes[name]['теги'])

def add_note():
    note_name, ok = QInputDialog.getText(window, "Добавить заметку", "Название заметки:")
    if ok and note_name != "":
        notes[note_name] = {"текст" : "", "теги" : []}
        list_notes.addItem(note_name)
        list_tags.addItems(notes[note_name]["теги"])
        print(notes)

def del_note():
    if list_notes.selectedItems():
        key = list_notes.selectedItems()[0].text()
        del notes[key]
        list_notes.clear()
        list_tags.clear()
        field_text.clear()
        list_notes.addItems(notes)
        with open("notes_data.json", "w", encoding='utf-8') as file:
            json.dump(notes, file, sort_keys=True)
        print(notes)
    else:
        error.setText("Заметка для удаления не выбрана")
        error.exec_()
def save_note():
    if list_notes.selectedItems():
        key = list_notes.selectedItems()[0].text()
        notes[key]["текст"] = field_text.toPlainText()
        with open("notes_data.json", "w") as file:
            json.dump(notes, file, sort_keys=True)
        print(notes)
    else:
        error.setText("Заметка для сохранения не выбрана!")
        error.exec_()
def add_tag():
    if list_notes.selectedItems():
        key = list_notes.selectedItems()[0].text()
        tag = field_tag.text()
        if not tag in notes[key]["теги"]:
            notes[key]["теги"].append(tag)
            list_tags.addItem(tag)
            field_tag.clear()
        with open("notes.data.json", 'w') as file:
            json.dump(notes, file, sort_keys=True)
    else:
        error.setText("Заметка для добавления тегов не выбрана")
        error.exec_()
def del_tag():
    if list_tags.selectedItems() and list_notes.selectedItems():
        key = list_notes.selectedItems()[0].text()
        tag = list_tags.selectedItems()[0].text()
        notes[key]['теги'].remove(tag)
        list_tags.clear()
        list_tags.addItems(notes[key]["теги"])
        with open("notes_data.json", "w") as file:
            json.dump(notes, file, sort_keys=True)
    else:
        error.setText("Тег для удаления не выбран!")
        error.exec_()
def search_tag():
    tag = field_tag.text()
    if button_tag_search.text() == "Искать заметку по тегу" and tag:
        notes_filtered = {} # тут будут заметки с выделенным тегом
        for note in notes:
            if tag in notes[note]["теги"]:
                notes_filtered[note] = notes[note]
        button_tag_search.setText("Сбросить поиск")
        list_notes.clear()
        list_tags.clear()
        list_notes.addItems(notes_filtered)
    elif button_tag_search.text() == "Сбросить поиск":
        button_tag_search.setText("Искать заметку по тегу")
        field_tag.clear()
        list_notes.clear()
        list_tags.clear()
        list_notes.addItems(notes)
    else:
        error.setText("Заметок с таким тегом нет")
        error.exec_()
list_notes.itemClicked.connect(show_note)
button_note_create.clicked.connect(add_note)
button_note_del.clicked.connect(del_note)
button_note_save.clicked.connect(save_note)
button_tag_add.clicked.connect(add_tag)
button_tag_del.clicked.connect(del_tag)
button_tag_search.clicked.connect(search_tag)
list_notes.addItems(notes)

window.show()
app.exec_()