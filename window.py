import os
from tkinter import Button, Entry, Label, Tk, Menu, Frame, LabelFrame, Toplevel
from tkinter import N, S, W, E, END
from tkinter.constants import INSERT
from tkinter.ttk import Combobox, Style
from tkinter.scrolledtext import ScrolledText
from tkinter.filedialog import askopenfilename
from PIL import Image
from PIL.ImageDraw import Draw
from PIL.ImageTk import PhotoImage
from constants import *
from textprinter import *
from sys import exit



class Window ():

    def __init__(self):

        self.CT = CT
        self.__window = Tk()
        self.__set_window()
        self.__set_menu()
        self.__set_widgets()

    def run_window(self):

        self.__window.mainloop()
        
    def __set_window(self):

        #self.__window.attributes("-fullscreen", True)
        self.__window.title("Восхождение: Редактор Карт")
        self.__window.iconbitmap("icon.ico")
        x = 250
        self.__window.minsize(5 * x, 3 * x)

        self.__window.rowconfigure(0, weight = 2)
        self.__window.rowconfigure(1, weight = 1)

        self.__window.columnconfigure(0, weight = 1)
        self.__window.columnconfigure(1, weight = 5)

    def __set_menu(self):

        self.__menubar = Menu(self.__window)
        
        self.__file_menu = Menu(self.__menubar, tearoff = 0)
        # self.__file_menu.add_command(label = "Открыть...", underline = 1, accelerator = HK_OPEN, command = self.__window.destroy)
        # self.__window.bind_all(HK_OPEN_BIND, lambda e: <open new file>)
        self.__file_menu.add_command(label = "Открыть готовые карты", underline = 0, command = self.__open_directory)
        self.__file_menu.add_command(label = "Выход", underline = 1, accelerator = HK_EXIT, command = exit)
        self.__window.bind_all(HK_EXIT_BIND, lambda e: exit())
        self.__menubar.add_cascade(label = "Файл", underline = 0, menu = self.__file_menu)
        
        self.__edit_menu = Menu(self.__menubar, tearoff = 0)
        self.__edit_menu.add_command(label = "Ключевые слова...", underline = 0, command = self.__open_kw_insert)
        self.__menubar.add_cascade(label = "Правка", underline = 0, menu = self.__edit_menu)
        
        self.__about_menu = Menu(self.__menubar, tearoff = 0)
        # self.__about_menu.add_command()
        self.__menubar.add_cascade(label = "Справка", underline = 0, menu = self.__about_menu)

        self.__about_menu = Menu(self.__menubar, tearoff = 0)
        self.__about_menu.add_command(label = "Стандартная", underline = 0, command = lambda: self.__change_theme(0))
        self.__about_menu.add_command(label = "Фиолетовая", underline = 0, command = lambda: self.__change_theme(1))
        self.__about_menu.add_command(label = "Голубая", underline = 0, command = lambda: self.__change_theme(2))
        self.__about_menu.add_command(label = "Оливковая", underline = 0, command = lambda: self.__change_theme(3))
        self.__menubar.add_cascade(label = "Тема", underline = 0, menu = self.__about_menu)

        self.__window["menu"] = self.__menubar

    def __set_widgets(self):

        rows = 5

        self.__value_frame = LabelFrame(self.__window, background = "#a0a0a0")
        for i in range(rows):
            self.__value_frame.rowconfigure(i, weight = 1)
        self.__value_frame.columnconfigure(0, weight = 1)
        self.__value_frame.columnconfigure(1, weight = 1)
        self.__value_frame.columnconfigure(2, weight = 3)
        self.__value_frame.grid(row = 1, column = 0, columnspan = 2, padx = 10, pady = 10, sticky = N + W + S + E)

        self.__image_frame = LabelFrame(self.__window, background = "#a0a0a0")
        self.__image_frame.rowconfigure(0, weight = 1)
        self.__image_frame.columnconfigure(0, weight = 1)
        self.__image_frame.grid(row = 0, column = 0, padx = 10, pady = 10, sticky = N + W + S + E)

        self.__table_frame = LabelFrame(self.__window, background = "#a0a0a0")
        self.__table_frame.grid(row = 0, column = 1, padx = 10, pady = 10, sticky = N + W + S + E)

        self.__set_value_frame(rows)
        self.__set_image_frame()

        self.__change_theme(0)

    def __change_theme(self, color_index):

        self.CT = color_index
        
        ci = color_index
        cm = CT_MAIN[ci]
        cs = CT_SUB[ci]
        ce = CT_EXTRA[ci]
        ct = CT_TEXT[ci]
        
        self.__window.config(bg = cm)

        frame_list = [self.__value_frame, 
                      self.__table_frame, 
                      self.__image_frame,
                      self.__name_frame,
                      self.__cost_frame,
                      self.__type_frame,
                      self.__subtype_frame,
                      self.__color_frame,
                      self.__power_frame,
                      self.__artist_frame,
                      self.__artwork_frame,
                      self.__finish_frame,
                      self.__text_frame]

        for i in frame_list:
            i.config(bg = cs)

        frame_list = [self.__name_frame,
                      self.__cost_frame,
                      self.__type_frame,
                      self.__subtype_frame,
                      self.__color_frame,
                      self.__power_frame,
                      self.__artist_frame,
                      self.__artwork_frame,
                      self.__finish_frame,
                      self.__text_frame]
        for i in frame_list:
            i.config(fg = ct)

        widget_list = [self.__name_entry,
                      self.__cost_entry,
                      self.__power_entry,
                      self.__artist_entry,
                      self.__artwork_button,
                      self.__finish_button,
                      self.__text_text]
        for i in widget_list:
            i.config(bg = ce)
            i.config(fg = ct)

        self.__image_label.config(bg = cs)

    def __open_directory(self):

        os.startfile(os.path.realpath("results"))


    def __upload_image(self):

        filename = askopenfilename(title = "Выберите изображение для карты", filetypes = ((" Image files", "*.jpg"), (" Image files", "*.png")))

        if filename != "":

            print("IMAGE UPLOADED")

            Image.open(filename).save("temp/temp.png")

            self.__open_imagecut_window()

    def __open_kw_insert(self):

        self.__kw_window = Toplevel()
        self.__kw_set_window()
        self.__kw_set_widgets()

    def __kw_set_window(self):

        self.__kw_window.title("Вставка ключевых слов")
        x = 70
        self.__kw_window.minsize(4 * x, 1 * x)

        self.__kw_window.rowconfigure(0, weight = 1)
        self.__kw_window.rowconfigure(1, weight = 3)

        self.__kw_window.columnconfigure(0, weight = 1)

    def __kw_set_widgets(self):

        self.__kw_text_frame = LabelFrame(self.__kw_window)
        self.__kw_text_frame.rowconfigure(0, weight = 1)
        self.__kw_text_frame.columnconfigure(0, weight = 1)
        self.__kw_text_frame.grid(row = 0, column = 0, padx = 10, pady = 10, sticky = N + W + S + E)

        self.__kw_value_frame = LabelFrame(self.__kw_window)
        self.__kw_value_frame.rowconfigure(0, weight = 1)
        self.__kw_value_frame.rowconfigure(1, weight = 1)
        self.__kw_value_frame.rowconfigure(2, weight = 1)
        self.__kw_value_frame.columnconfigure(0, weight = 1)
        self.__kw_value_frame.grid(row = 1, column = 0, padx = 10, pady = 10, sticky = N + W + S + E)

        self.__kw_set_text_frame()
        self.__kw_set_value_frame()

        ci = self.CT
        cm = CT_MAIN[ci]
        cs = CT_SUB[ci]
        ce = CT_EXTRA[ci]
        ct = CT_TEXT[ci]

        self.__kw_window.config(bg = cm)

        frame_list = [self.__kw_text_frame,
                      self.__kw_value_frame]
        for i in frame_list:
            i.config(bg = cs)
            i.config(fg = ct)

        widget_list = [# self.__kw_keyword_combo,
                       self.__kw_text_label,
                       self.__kw_update_button,
                       self.__kw_insert_button]
        for i in widget_list:
            i.config(bg = ce)
            i.config(fg = ct)

        self.__kw_text_label["background"] = cs

    def __kw_set_text_frame(self):

        self.__kw_text_label = Label(self.__kw_text_frame, font = MAINFONT, text = "Выберите ключевое слово из предложенных ниже.")
        self.__kw_text_label.grid(row = 1, column = 0, padx = 5, pady = 5, sticky = N + W + S + E)

    def __kw_set_value_frame(self):

        kw = [*INSERTABLE_KEYWORDS.keys()]

        self.__kw_keyword_combo = Combobox(self.__kw_value_frame, values = kw)
        self.__kw_keyword_combo.grid(row = 0, column = 0, padx = 5, pady = 5, sticky = N + W + S + E)

        self.__kw_update_button = Button(self.__kw_value_frame, text = "Отобразить текст", command = self.__kw_update_text)
        self.__kw_update_button.grid(row = 1, column = 0, padx = 5, pady = 5, sticky = N + W + S + E)

        self.__kw_insert_button = Button(self.__kw_value_frame, text = "Добавить на карту", command = self.__kw_insert_text)
        self.__kw_insert_button.grid(row = 2, column = 0, padx = 5, pady = 5, sticky = N + W + S + E)

    def __kw_update_text(self):

        kw = [*INSERTABLE_KEYWORDS.keys()]

        keyword = kw[self.__kw_keyword_combo.current()]
        ruletext = INSERTABLE_KEYWORDS[keyword]
        self.__kw_text_label["text"] = ruletext

    def __kw_insert_text(self):

        kw = [*INSERTABLE_KEYWORDS.keys()]

        keyword = kw[self.__kw_keyword_combo.current()]
        ruletext = INSERTABLE_KEYWORDS[keyword]
        self.__text_text.insert(INSERT, ruletext + "\n")

    def __open_imagecut_window(self):

        self.__ic_window = Toplevel()
        self.__ic_set_window()
        # self.__ic_set_menu()
        self.__ic_set_widgets()

    def __ic_set_window(self):

        self.__ic_window.title("Обрезка изображения")
        x = 70
        self.__ic_window.minsize(5 * x, 9 * x)

        self.__ic_window.rowconfigure(0, weight = 7)
        self.__ic_window.rowconfigure(1, weight = 2)

        self.__ic_window.columnconfigure(0, weight = 1)

    def __ic_set_widgets(self):

        self.__ic_image_frame = LabelFrame(self.__ic_window, background = "#a0a0a0")
        self.__ic_image_frame.rowconfigure(0, weight = 1)
        self.__ic_image_frame.columnconfigure(0, weight = 1)
        self.__ic_image_frame.grid(row = 0, column = 0, padx = 10, pady = 10, sticky = N + W + S + E)

        self.__ic_value_frame = LabelFrame(self.__ic_window, background = "#a0a0a0")
        self.__ic_value_frame.rowconfigure(0, weight = 1)
        self.__ic_value_frame.rowconfigure(1, weight = 1)
        self.__ic_value_frame.columnconfigure(0, weight = 1)
        self.__ic_value_frame.columnconfigure(1, weight = 1)
        self.__ic_value_frame.columnconfigure(2, weight = 1)
        self.__ic_value_frame.grid(row = 1, column = 0, padx = 10, pady = 10, sticky = N + W + S + E)

        self.__ic_set_value_frame()
        self.__ic_set_image_frame()

        ci = self.CT
        cm = CT_MAIN[ci]
        cs = CT_SUB[ci]
        ce = CT_EXTRA[ci]
        ct = CT_TEXT[ci]

        self.__ic_window.config(bg = cm)

        frame_list = [self.__ic_image_frame,
                      self.__ic_value_frame,
                      self.__ic_xs_frame,
                      self.__ic_ys_frame,
                      self.__ic_scale_frame,
                      self.__ic_update_frame,
                      self.__ic_finish_frame]
        for i in frame_list:
            i.config(bg = cs)
            i.config(fg = ct)

        widget_list = [self.__ic_xs_entry,
                       self.__ic_ys_entry,
                       self.__ic_scale_entry,
                       self.__ic_update_button,
                       self.__ic_finish_button]
        for i in widget_list:
            i.config(bg = ce)
            i.config(fg = ct)

        self.__ic_image_label.config(bg = cs)

    def __ic_set_value_frame(self):

        # Характеристики изображения: Сдвиг по х

        self.__ic_xs_frame = LabelFrame(self.__ic_value_frame, background = "#d0d0d0", text = "Сдвиг по х")
        self.__ic_xs_frame.grid(row = 0, column = 0, padx = 5, pady = 5, sticky = N + W + S + E)
        self.__ic_xs_frame.rowconfigure(0, weight = 1)
        self.__ic_xs_frame.columnconfigure(0, weight = 1)

        self.__ic_xs_entry = Entry(self.__ic_xs_frame, font = MAINFONT)
        self.__ic_xs_entry.grid(row = 0, column = 0, padx = 5, pady = 5, sticky = N + W + S + E)
        self.__ic_xs_entry.insert(END, "0")

        # Характеристики изображения: Сдвиг по y

        self.__ic_ys_frame = LabelFrame(self.__ic_value_frame, background = "#d0d0d0", text = "Сдвиг по y")
        self.__ic_ys_frame.grid(row = 0, column = 1, padx = 5, pady = 5, sticky = N + W + S + E)
        self.__ic_ys_frame.rowconfigure(0, weight = 1)
        self.__ic_ys_frame.columnconfigure(0, weight = 1)

        self.__ic_ys_entry = Entry(self.__ic_ys_frame, font = MAINFONT)
        self.__ic_ys_entry.grid(row = 0, column = 0, padx = 5, pady = 5, sticky = N + W + S + E)
        self.__ic_ys_entry.insert(END, "0")

        # Характеристики изображения: Масштабирование

        self.__ic_scale_frame = LabelFrame(self.__ic_value_frame, background = "#d0d0d0", text = "Масштабирование, в %")
        self.__ic_scale_frame.grid(row = 1, column = 0, padx = 5, pady = 5, sticky = N + W + S + E)
        self.__ic_scale_frame.rowconfigure(0, weight = 1)
        self.__ic_scale_frame.columnconfigure(0, weight = 1)

        self.__ic_scale_entry = Entry(self.__ic_scale_frame, font = MAINFONT)
        self.__ic_scale_entry.grid(row = 0, column = 0, padx = 5, pady = 5, sticky = N + W + S + E)
        self.__ic_scale_entry.insert(END, "100")

        # Характеристики изображения: Обновление

        self.__ic_update_frame = LabelFrame(self.__ic_value_frame, background = "#d0d0d0", text = "Обрезка")
        self.__ic_update_frame.grid(row = 1, column = 1, padx = 5, pady = 5, sticky = N + W + S + E)
        self.__ic_update_frame.rowconfigure(0, weight = 1)
        self.__ic_update_frame.columnconfigure(0, weight = 1)

        self.__ic_update_button = Button(self.__ic_update_frame, font = MAINFONT, text = "Обновить", command = self.__update_ic_image)
        self.__ic_update_button.grid(row = 0, column = 0, padx = 5, pady = 5, sticky = N + W + S + E)

        # Характеристики изображения: Сохранение

        self.__ic_finish_frame = LabelFrame(self.__ic_value_frame, background = "#d0d0d0", text = "Завершение")
        self.__ic_finish_frame.grid(row = 2, column = 0, columnspan = 2, padx = 5, pady = 5, sticky = N + W + S + E)
        self.__ic_finish_frame.rowconfigure(0, weight = 1)
        self.__ic_finish_frame.columnconfigure(0, weight = 1)

        self.__ic_finish_button = Button(self.__ic_finish_frame, font = MAINFONT, text = "Применить", command = self.__close_ic)
        self.__ic_finish_button.grid(row = 0, column = 0, padx = 5, pady = 5, sticky = N + W + S + E)

    def __close_ic(self):

        self.__ic_window.destroy()
        self.__update_image()

    def __ic_set_image_frame(self):
        
        self.__ic_image_label = Label(self.__ic_image_frame)
        self.__ic_image_label.grid(row = 0, column = 0, padx = 5, pady = 5, sticky = N + W + S + E)

        self.__update_ic_image()

    def __update_ic_image(self):

        x = 60

        x_shift = int(self.__ic_xs_entry.get())
        y_shift = int(self.__ic_ys_entry.get())

        scale = int(self.__ic_scale_entry.get())

        pic = Image.open('temp/temp.png')
        frame = Image.open('data/FrameN.png')
        mask = Image.open('data/FrameMask.png').convert('L')

        h = (pic.height) * scale // 100
        w = (pic.width) * scale // 100

        pic = pic.resize((w, h), Image.ANTIALIAS)

        pic = pic.crop((x_shift, y_shift, x_shift + 744, y_shift + 1039))

        pic.save('temp/edited.png')

        pic.paste(frame, (0, 0), mask)

        self.ic_img = PhotoImage(pic.resize((5 * x, 7 * x), Image.ANTIALIAS))

        self.__ic_image_label["image"] = self.ic_img
        
    def __update_image(self):
        
        x = 60

        img = Image.open('temp/edited.png')
        
        CardColor(img, self.__color_combo.current())                # Флажок
        CardCost(img, self.__cost_entry.get())                      # Стоимость карты
        CardType(img, self.__type_combo.current())                  # Тип карты
        CardTitle(img, self.__name_entry.get())                     # Название карты
        CardSubtype(img, self.__subtype_combo.current())            # Подтип карты
        CardCredits(img, self.__artist_entry.get())                 # Автор арта
        CardPower(img, self.__power_entry.get())                    # Сила карты
        CardRuletext(img, self.__text_text.get("1.0", END)[0:-1])   # Текст карты
        CardCopyright(img)

        # Сохранение
        
        if self.__name_entry.get() == "":
            cardname = "results/untitled.png"
        else:
            cardname = 'results/' + self.__name_entry.get().replace(':', '') + '.png'
        img.save(cardname)

        self.img = PhotoImage(Image.open(cardname).resize((5 * x, 7 * x), Image.ANTIALIAS))
        self.__image_label["image"] = self.img

    def __set_image_frame(self):

        x = 60
        
        self.img = PhotoImage(Image.open('data/FrameW.png').resize((5 * x, 7 * x), Image.ANTIALIAS))
        self.__image_label = Label(self.__image_frame, image = self.img)
        self.__image_label.grid(row = 0, column = 0, padx = 5, pady = 5, sticky = N + W + S + E)
        # self.__update_image()

    def __set_value_frame(self, rows):

        # Характеристики карты: Название

        self.__name_frame = LabelFrame(self.__value_frame, background = "#d0d0d0", text = "Название карты")
        self.__name_frame.grid(row = 0, column = 0, padx = 5, pady = 5, sticky = N + W + S + E)
        self.__name_frame.rowconfigure(0, weight = 1)
        self.__name_frame.columnconfigure(0, weight = 1)

        self.__name_entry = Entry(self.__name_frame, font = MAINFONT)
        self.__name_entry.grid(row = 0, column = 0, padx = 5, pady = 5, sticky = N + W + S + E)

        # Характеристики карты: Стоимость

        self.__cost_frame = LabelFrame(self.__value_frame, background = "#d0d0d0", text = "Стоимость карты")
        self.__cost_frame.grid(row = 0, column = 1, padx = 5, pady = 5, sticky = N + W + S + E)
        self.__cost_frame.rowconfigure(0, weight = 1)
        self.__cost_frame.columnconfigure(0, weight = 1)

        self.__cost_entry = Entry(self.__cost_frame, font = MAINFONT)
        self.__cost_entry.grid(row = 0, column = 0, padx = 5, pady = 5, sticky = N + W + S + E)

        # Характеристики карты: Тип карты

        self.__type_frame = LabelFrame(self.__value_frame, background = "#d0d0d0", text = "Тип карты")
        self.__type_frame.grid(row = 1, column = 0, padx = 5, pady = 5, sticky = N + W + S + E)
        self.__type_frame.rowconfigure(0, weight = 1)
        self.__type_frame.columnconfigure(0, weight = 1)

        self.__type_combo = Combobox(self.__type_frame, values = CARDTYPES, font = MAINFONT)
        self.__type_combo.grid(row = 0, column = 0, padx = 5, pady = 5, sticky = N + W + S + E)
        self.__type_combo.current(4)

        # Характеристики карты: Подтип карты

        self.__subtype_frame = LabelFrame(self.__value_frame, background = "#d0d0d0", text = "Подтип карты")
        self.__subtype_frame.grid(row = 1, column = 1, padx = 5, pady = 5, sticky = N + W + S + E)
        self.__subtype_frame.rowconfigure(0, weight = 1)
        self.__subtype_frame.columnconfigure(0, weight = 1)

        self.__subtype_combo = Combobox(self.__subtype_frame, values = CARDSUBTYPES, font = MAINFONT)
        self.__subtype_combo.grid(row = 0, column = 0, padx = 5, pady = 5, sticky = N + W + S + E)
        self.__subtype_combo.current(0)
        

        # Характеристики карты: Цвет

        self.__color_frame = LabelFrame(self.__value_frame, background = "#d0d0d0", text = "Цвет карты")
        self.__color_frame.grid(row = 2, column = 0, padx = 5, pady = 5, sticky = N + W + S + E)
        self.__color_frame.rowconfigure(0, weight = 1)
        self.__color_frame.columnconfigure(0, weight = 1)

        self.__color_combo = Combobox(self.__color_frame, values = COLORS, font = MAINFONT)
        self.__color_combo.grid(row = 0, column = 0, padx = 5, pady = 5, sticky = N + W + S + E)
        self.__color_combo.current(4)

        # Характеристики карты: Сила

        self.__power_frame = LabelFrame(self.__value_frame, background = "#d0d0d0", text = "Сила карты")
        self.__power_frame.grid(row = 2, column = 1, padx = 5, pady = 5, sticky = N + W + S + E)
        self.__power_frame.rowconfigure(0, weight = 1)
        self.__power_frame.columnconfigure(0, weight = 1)

        self.__power_entry = Entry(self.__power_frame, font = MAINFONT)
        self.__power_entry.grid(row = 0, column = 0, padx = 5, pady = 5, sticky = N + W + S + E)

        # Характеристики карты: Художник

        self.__artist_frame = LabelFrame(self.__value_frame, background = "#d0d0d0", text = "Художник")
        self.__artist_frame.grid(row = 3, column = 0, padx = 5, pady = 5, sticky = N + W + S + E)
        self.__artist_frame.rowconfigure(0, weight = 1)
        self.__artist_frame.columnconfigure(0, weight = 1)

        self.__artist_entry = Entry(self.__artist_frame, font = MAINFONT)
        self.__artist_entry.grid(row = 0, column = 0, padx = 5, pady = 5, sticky = N + W + S + E)

        # Характеристики карты: Изображение

        self.__artwork_frame = LabelFrame(self.__value_frame, background = "#d0d0d0", text = "Арт карты")
        self.__artwork_frame.grid(row = 3, column = 1, padx = 5, pady = 5, sticky = N + W + S + E)
        self.__artwork_frame.rowconfigure(0, weight = 1)
        self.__artwork_frame.columnconfigure(0, weight = 1)

        self.__artwork_button = Button(self.__artwork_frame, font = MAINFONT, text = "Загрузить изображение...", command = self.__upload_image)
        self.__artwork_button.grid(row = 0, column = 0, padx = 5, pady = 5, sticky = N + W + S + E)

        # Характеристики карты: Текст

        self.__text_frame = LabelFrame(self.__value_frame, background = "#d0d0d0", text = "Текст карты")
        self.__text_frame.grid(row = 0, column = 2, rowspan = rows, padx = 5, pady = 5, sticky = N + W + S + E)
        self.__text_frame.rowconfigure(0, weight = 1)
        self.__text_frame.columnconfigure(0, weight = 1)

        self.__text_text = ScrolledText(self.__text_frame, width = 10, height = 5, font = SUBFONT)
        self.__text_text.grid(row = 0, column = 0, padx = 5, pady = 5, sticky = N + W + S + E)

        # Характеристики карты: Завершение

        self.__finish_frame = LabelFrame(self.__value_frame, background = "#d0d0d0", text = "Завершение работы")
        self.__finish_frame.grid(row = 4, column = 0, columnspan = 2, padx = 5, pady = 5, sticky = N + W + S + E)
        self.__finish_frame.rowconfigure(0, weight = 1)
        self.__finish_frame.columnconfigure(0, weight = 1)

        self.__finish_button = Button(self.__finish_frame, font = MAINFONT, text = "Обновить и сохранить карту", command = self.__update_image)
        self.__finish_button.grid(row = 0, column = 0, padx = 5, pady = 5, sticky = N + W + S + E)