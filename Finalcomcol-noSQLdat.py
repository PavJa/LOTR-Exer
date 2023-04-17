import colour
import numpy as np
from collections import Counter

import pandas as pd
import wx
import matplotlib
import seaborn as sns
import re
import wx.adv
import mysql.connector
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
matplotlib.use('WXAgg')

# the program takes an input (e.g., in RGB) and uses several functions to compare the input to colours in one's databese.
# Each function has one vote, and the colour with the highest number of votes wins.

# the code still needs polishing (but the project is on hold right now)

# connection to sql!! - create your own SQL database of RGB colours to compare the inputs properly.

# !! I hardcoded a small catalogue (catalogue 1) just for a presentation (catalogue 2 does not work in this demo)


#mydb = mysql.connector.connect(
#  host="",
#  port="",
#  database = '',
#  user="",
#  password=""
#)

#cursor = mydb.cursor()
#cursor.execute("select database();")

#record = cursor.fetchone()
#print("You're connected to database: ", record)

#sql_select_Query = "select * from pandas_to_excel"
#cursor.execute(sql_select_Query)
#records = cursor.fetchall()

#sql_concat = "select concat(R,',',G,',',B) as 'RGB' from pandas_to_excel"
#cursor.execute(sql_concat)
#records2 = cursor.fetchall()

#sql_concat_small = "select concat(R,',',G,',',B) as 'RGB' from cat2_sall"
#cursor.execute(sql_concat_small)
#records3 = cursor.fetchall()

#lk_pokus = [[j.split(',', 3) for j in i] for i in records2]
#lk_pokus_flat = [i for j in lk_pokus for i in j]
#Catalogue1_big = [[int(x) for x in j] for j in lk_pokus_flat]

#lk_pokus_small = [[j.split(',', 3) for j in i] for i in records3]
#lk_pokus_flat_small = [i for j in lk_pokus_small for i in j]
#Catalogue2_small = [[int(x) for x in j] for j in lk_pokus_flat_small]
#sns.set()

Catalogue1_big = [[0, 165, 227], [255, 205, 31], [255, 203, 5], [254, 191, 51], [139, 0, 0], [165, 42, 42],
                      [178, 34, 34],
                      [220, 20, 60], [255, 0, 0], [255, 99, 71], [255, 127, 80], [205, 92, 92], [240, 128, 128],
                      [233, 150, 122],
                      [250, 128, 114], [255, 160, 122], [255, 69, 0], [255, 140, 0], [255, 165, 0], [255, 215, 0],
                      [184, 134, 11],
                      [218, 165, 32], [238, 232, 170], [189, 183, 107], [240, 230, 140], [128, 128, 0], [255, 255, 0],
                      [154, 205, 50],
                      [85, 107, 47], [107, 142, 35], [124, 252, 0], [127, 255, 0], [173, 255, 47], [0, 100, 0],
                      [0, 128, 0], [34, 139, 34],
                      [0, 255, 0], [50, 205, 50], [144, 238, 144], [152, 251, 152], [143, 188, 143], [0, 250, 154],
                      [0, 255, 127], [46, 139, 87], [102, 205, 170], [60, 179, 113], [32, 178, 170], [47, 79, 79],
                      [0, 128, 128],
                      [0, 139, 139], [0, 255, 255], [224, 255, 255], [0, 206, 209], [64, 224, 208], [72, 209, 204],
                      [175, 238, 238],
                      [127, 255, 212], [176, 224, 230], [95, 158, 160], [70, 130, 180], [100, 149, 237], [0, 191, 255],
                      [30, 144, 255],
                      [173, 216, 230], [135, 206, 235], [135, 206, 250], [25, 25, 112], [0, 0, 128], [0, 0, 139],
                      [0, 0, 205], [0, 0, 255],
                      [65, 105, 225], [138, 43, 226], [75, 0, 130], [72, 61, 139], [106, 90, 205], [123, 104, 238],
                      [147, 112, 219],
                      [139, 0, 139], [148, 0, 211], [153, 50, 204], [186, 85, 211], [128, 0, 128], [216, 191, 216],
                      [221, 160, 221],
                      [238, 130, 238], [255, 0, 255], [218, 112, 214], [199, 21, 133], [219, 112, 147], [255, 20, 147],
                      [255, 105, 180],
                      [255, 182, 193], [255, 192, 203], [250, 235, 215], [245, 245, 220], [255, 228, 196],
                      [255, 235, 205], [245, 222, 179],
                      [255, 248, 220], [255, 250, 205], [250, 250, 210], [255, 255, 224], [139, 69, 19], [160, 82, 45],
                      [210, 105, 30],
                      [205, 133, 63], [244, 164, 96], [222, 184, 135], [210, 180, 140], [188, 143, 143],
                      [255, 228, 181], [255, 222, 173],
                      [255, 218, 185], [255, 228, 225], [255, 240, 245], [250, 240, 230], [253, 245, 230],
                      [255, 239, 213],
                      [255, 245, 238], [245, 255, 250], [112, 128, 144], [119, 136, 153], [176, 196, 222],
                      [230, 230, 250], [255, 250, 240],
                      [240, 248, 255], [248, 248, 255], [240, 255, 240], [255, 255, 240], [240, 255, 255],
                      [255, 250, 250], [0, 0, 0],
                      [105, 105, 105], [128, 128, 128], [169, 169, 169], [192, 192, 192], [211, 211, 211],
                      [220, 220, 220], [245, 245, 245],
                      [255, 255, 255]]



class ColoursFrame(wx.Frame):
    def __init__(self, parent, title):
        super(ColoursFrame, self).__init__(parent, title=title, size=(605, 505), style = wx.MINIMIZE_BOX
        |wx.SYSTEM_MENU|wx.CAPTION|wx.CLOSE_BOX|wx.CLIP_CHILDREN)

        self.panel = ColoursPanel(self)
        #icon = wx.Icon("C://Users//pavel//PycharmProjects//pythonv10_2Colours//Cwheel.ico", wx.BITMAP_TYPE_ICO)
        #self.SetIcon(icon)

# there are some icons that I ddeleted in this demo

class ColoursPanel(wx.Panel):
    def __init__(self, parent):
        super(ColoursPanel, self).__init__(parent)

        #bmp_del = wx.Bitmap("C://Users//pavel//PycharmProjects//pythonv10_2Colours//bin.png")
        #bmp_exp = wx.Bitmap("C://Users//pavel//PycharmProjects//pythonv10_2Colours//export.png")
        #bmp_con = wx.Bitmap("C://Users//pavel//PycharmProjects//pythonv10_2Colours//convert.png")
        #bmp_find = wx.Bitmap("C://Users//pavel//PycharmProjects//pythonv10_2Colours//search.png")
        #bmp_sall = wx.Bitmap("C://Users//pavel//PycharmProjects//pythonv10_2Colours//selectall.png")
        #bmp_comp = wx.Bitmap("C://Users//pavel//PycharmProjects//pythonv10_2Colours//iwheel.png")

        self.tipRGB = wx.ToolTip("Use commas to separate three numbers between 0 and 255.")
        self.tipCMYK = wx.ToolTip("Use commas to separate four numbers between 0 and 100.")
        self.tipHEX = wx.ToolTip("Write code without #")
        self.tipCompare = wx.ToolTip("Compares all found colours with the input colour in one palette.")
        self.tipComparePair = wx.ToolTip("Compares all found colours with the input colour in pairs.")

        self.cb1 = wx.RadioButton(self, label='RGB')
        self.cb1.SetToolTip(self.tipRGB)
        self.cb1.Bind(wx.EVT_RADIOBUTTON, self.onChecked_cb1)

        self.cb2 = wx.RadioButton(self, label='CMYK')
        self.cb2.SetToolTip(self.tipCMYK)
        self.cb2.Bind(wx.EVT_RADIOBUTTON, self.onChecked_cb2)

        self.cb3 = wx.RadioButton(self, label='HEX')
        self.cb3.SetToolTip(self.tipHEX)
        self.cb3.Bind(wx.EVT_RADIOBUTTON, self.onChecked_cb3)

        self.st_CaLtype = wx.StaticText(self, label='Choose an Input Type : ')

        distros = ['Catalogue1', 'Catalogue2']
        self.Cat_Choice = wx.ComboBox(self, choices=distros, style=wx.CB_READONLY)
        self.Cat_Choice.Bind(wx.EVT_COMBOBOX, self.OnSelect_cat)

        self.st_Cat = wx.StaticText(self, label='Select a Catalogue : ')

        self.nameLabel = wx.StaticText(self, label="Input Colour Code :")

        self.text_ctrl = wx.TextCtrl(self, size=(140, -1))

        self.nameLabelGraph = wx.StaticText(self, label="Compare Results Graphically:")

        self.my_btn = wx.Button(self, label='Find Closest Colour(s)')
        #self.my_btn.SetBitmap(bmp_find)
        self.my_btn.Bind(wx.EVT_BUTTON, self.on_press)

        self.my_btn_convert = wx.Button(self, label='Convert Input Colour')
        #self.my_btn_convert.SetBitmap(bmp_con)
        self.my_btn_convert.Bind(wx.EVT_BUTTON, self.on_press_convert)

        self.compare_colour_picture = wx.CheckBox(self, label='One Palette')
        self.compare_colour_picture.SetToolTip(self.tipCompare)
        self.compare_colour_picture.Bind(wx.EVT_CHECKBOX, self.onChecked_compare_colour_picture)

        self.compare_colour_picture_pair = wx.CheckBox(self, label='Pair by Pair')
        self.compare_colour_picture_pair.SetToolTip(self.tipComparePair)
        self.compare_colour_picture_pair.Bind(wx.EVT_CHECKBOX, self.onChecked_compare_colour_picture_pair)

        self.st_options = wx.StaticText(self, label='Show only the highest-voted colour')

        self.only_highest_vote = wx.CheckBox(self, label='')
        self.only_highest_vote.Bind(wx.EVT_CHECKBOX, self.onChecked_only_highest_vote)

        self.list_ctrl = wx.ListCtrl(
            self, size=(-1, 240),
            style=wx.LC_REPORT | wx.BORDER_SUNKEN
        )

        listfont = self.list_ctrl.GetFont()
        headfont = listfont.MakeBold()
        headAttr = wx.ItemAttr((0, 0, 0), (240, 240, 240), headfont)

        self.list_ctrl.SetHeaderAttr(headAttr)

        self.list_ctrl.EnableCheckBoxes(True)
        self.list_ctrl.InsertColumn(0, 'Votes (Max=11)', width=100)
        self.list_ctrl.InsertColumn(1, 'Hex', width=75)
        self.list_ctrl.InsertColumn(2, 'RGB', width=90)
        self.list_ctrl.InsertColumn(3, 'CMYK', width=115)
        self.list_ctrl.InsertColumn(4, 'Catalogue', width=85)
        self.list_ctrl.InsertColumn(5, 'Catalogue Number', width=120)

        self.my_btn_compsel = wx.Button(self, label='Compare Selected Items')
        #self.my_btn_compsel.SetBitmap(bmp_comp)
        self.my_btn_compsel.Bind(wx.EVT_BUTTON, self.on_press_compsel)

        #self.btn = wx.Button(self, id=1, label="Delete All Results")
        #self.btn.SetBitmap(bmp_del)
        #self.btn.Bind(wx.EVT_BUTTON, self.on_press_del)

        self.list_ctrl.Bind(wx.EVT_LIST_ITEM_CHECKED, self.onItemChecked)

        self.list_ctrl.Bind(wx.EVT_LIST_ITEM_UNCHECKED, self.onItemUnChecked)

        self.btn_delItem = wx.Button(self, id=1, label="Delete Selected Item(s)")
        #self.btn_delItem.SetBitmap(bmp_del)
        self.btn_delItem.Bind(wx.EVT_BUTTON, self.on_press_delItem)

        self.btn_export = wx.Button(self, label='Export Selected Data')
        #self.btn_export.SetBitmap(bmp_exp)
        self.btn_export.Bind(wx.EVT_BUTTON, self.on_press_export)

        self.selectall_btn = wx.Button(self, label='(De)Select All')
        #self.selectall_btn.SetBitmap(bmp_sall)
        self.selectall_btn.Bind(wx.EVT_BUTTON, self.on_press_selectall)

        # set font

        font = wx.Font(10, wx.FONTFAMILY_DEFAULT, 0, 90, underline=False,
                       faceName="")

        self.my_btn_convert.SetFont(font)
        self.my_btn.SetFont(font)
        self.btn_delItem.SetFont(font)
        self.btn_export.SetFont(font)
        self.selectall_btn.SetFont(font)
        self.my_btn_compsel.SetFont(font)
        self.cb1.SetFont(font)
        self.cb2.SetFont(font)
        self.cb3.SetFont(font)
        self.st_CaLtype.SetFont(font)
        self.only_highest_vote.SetFont(font)
        self.st_options.SetFont(font)
        self.compare_colour_picture.SetFont(font)
        self.compare_colour_picture_pair.SetFont(font)
        self.nameLabel.SetFont(font)
        self.st_CaLtype.SetFont(font)
        self.Cat_Choice.SetFont(font)
        self.st_Cat.SetFont(font)
        self.nameLabelGraph.SetFont(font)
        self.text_ctrl.SetFont(font)

        # sizers layout

        topSizer = wx.BoxSizer(wx.VERTICAL)
        CatalogueSizer = wx.BoxSizer(wx.HORIZONTAL)
        CheckBoxSizer = wx.BoxSizer(wx.HORIZONTAL)
        LabelSizerandInput = wx.BoxSizer(wx.HORIZONTAL)
        GraphColourSizer = wx.BoxSizer(wx.HORIZONTAL)
        ButtonSizer = wx.BoxSizer(wx.HORIZONTAL)
        ButtonSizer2 = wx.BoxSizer(wx.HORIZONTAL)
        checkhighest = wx.BoxSizer(wx.HORIZONTAL)
        OutputSizer = wx.BoxSizer(wx.HORIZONTAL)

        CatalogueSizer.Add(self.st_Cat, 0, wx.ALL, 5)
        CatalogueSizer.Add(self.Cat_Choice, 0, wx.ALL, 5)
        CheckBoxSizer.Add(self.st_CaLtype, 0, wx.ALL, 5)
        CheckBoxSizer.Add(self.cb1, 0, wx.ALL, 5)
        CheckBoxSizer.Add(self.cb2, 0, wx.ALL, 5)
        CheckBoxSizer.Add(self.cb3, 0, wx.ALL, 5)
        LabelSizerandInput.Add(self.nameLabel, 0, wx.ALL, 5)
        LabelSizerandInput.Add(self.text_ctrl, 0, wx.ALL, 5)
        GraphColourSizer.Add(self.nameLabelGraph, 0, wx.ALL, 5)
        GraphColourSizer.Add(self.compare_colour_picture, 0, wx.ALL, 5)
        GraphColourSizer.Add(self.compare_colour_picture_pair, 0, wx.ALL, 5)
        checkhighest.Add(self.st_options, 0, wx.ALL, 5)
        checkhighest.Add(self.only_highest_vote, 0, wx.ALL, 5)
        ButtonSizer.Add(self.my_btn, 0, wx.ALL, 5)
        ButtonSizer.Add(self.my_btn_convert, 0, wx.ALL, 5)
        ButtonSizer.Add(self.my_btn_compsel, 0, wx.ALL, 5)
        ButtonSizer2.Add(self.selectall_btn, 0, wx.ALL, 5)
        ButtonSizer2.Add(self.btn_delItem, 0, wx.ALL, 5)
        #ButtonSizer2.Add(self.btn, 0, wx.ALL, 5)
        ButtonSizer2.Add(self.btn_export, 0, wx.ALL, 5)
        OutputSizer.Add(self.list_ctrl, 0, wx.ALL, 5)

        topSizer.Add(CatalogueSizer, 0)
        topSizer.Add(CheckBoxSizer, 0)
        topSizer.Add(LabelSizerandInput, 0)
        topSizer.Add(GraphColourSizer, 0)
        topSizer.Add(checkhighest, 0)
        topSizer.Add(ButtonSizer, 0)
        topSizer.Add(ButtonSizer2, 0)
        topSizer.Add(OutputSizer, 0)

        self.SetSizer(topSizer)
        topSizer.Fit(self)

    def onItemChecked(self, e):
        check = e.GetEventObject()
        yellow = [i for i in range(self.list_ctrl.GetItemCount()) if self.list_ctrl.IsItemChecked(i)]

        for i in reversed(yellow):
            self.list_ctrl.SetItemBackgroundColour(i,"yellow")

    def onItemUnChecked(self, e):
        uncheck = e.GetEventObject()
        white = [i for i in range(self.list_ctrl.GetItemCount()) if self.list_ctrl.IsItemChecked(i) == False]
        for i in reversed(white):
            self.list_ctrl.SetItemBackgroundColour(i,"white")

    def on_press_delItem(self,e):
        delete = [i for i in range(self.list_ctrl.GetItemCount()) if self.list_ctrl.IsItemChecked(i)]

        for i in reversed(delete):
            self.list_ctrl.DeleteItem(i)

    def on_press_selectall(self, e):
        checked = [i for i in range(self.list_ctrl.GetItemCount()) if self.list_ctrl.IsItemChecked(i)]

        rows = [i for i in range(self.list_ctrl.GetItemCount())]

        for i in range(self.list_ctrl.GetItemCount()):
            if len(checked) == len(rows):
                self.list_ctrl.CheckItem(i, check = False)
            else:
                self.list_ctrl.CheckItem(i)

    #def on_press_del(self, e):
        # delete all
        #self.list_ctrl.DeleteAllItems()

    def OnSelect_cat(self,e):
        cat = e.GetString()

    def onChecked_cb1(self, e):
        cb1 = e.GetEventObject()

    def onChecked_cb2(self, e):
        cb2 = e.GetEventObject()

    def onChecked_cb3(self, e):
        cb3 = e.GetEventObject()

    def onChecked_compare_colour_picture(self, e):
        compare_colour_picture = e.GetEventObject()

    def onChecked_compare_colour_picture_pair(self, e):
        compare_colour_picture = e.GetEventObject()

    def onChecked_only_highest_vote(self,e):
        only_highest_vote = e.GetEventObject()

    def hex_to_rgb(self,hex_value):
        h = hex_value.lstrip('#')
        return tuple(int(h[i:i + 2], 16) / 255.0 for i in (0, 2, 4))

    def rgb_to_hex(self, rgb):  # function hex to rgb
        return '%02x%02x%02x' % rgb

    rgb_scale = 255
    cmyk_scale = 100

    def rgb_to_cmyk(self, r, g, b):
        if (r, g, b) == (0, 0, 0):
            # black
            return 0, 0, 0, self.cmyk_scale

        # rgb [0,255] -> cmy [0,1]
        c = 1 - r / self.rgb_scale
        m = 1 - g / self.rgb_scale
        y = 1 - b / self.rgb_scale

        # extract out k [0, 1]
        min_cmy = min(c, m, y)
        c = (c - min_cmy) / (1 - min_cmy)
        m = (m - min_cmy) / (1 - min_cmy)
        y = (y - min_cmy) / (1 - min_cmy)
        k = min_cmy

        # rescale to the range [0,cmyk_scale]
        return c * self.cmyk_scale, m * self.cmyk_scale, y * self.cmyk_scale, k * self.cmyk_scale

    def cmyk_to_rgb(self, c, m, y, k, cmyk_scale=100, rgb_scale=255):  # cmyk to rgb, general function
        r = rgb_scale * (1.0 - c / float(cmyk_scale)) * (1.0 - k / float(cmyk_scale))
        g = rgb_scale * (1.0 - m / float(cmyk_scale)) * (1.0 - k / float(cmyk_scale))
        b = rgb_scale * (1.0 - y / float(cmyk_scale)) * (1.0 - k / float(cmyk_scale))
        return r, g, b

    def rgb_to_hex(self,rgb):  # function hex to rgb
        return '%02x%02x%02x' % rgb

    def add_hastag(self, hexlist): # add hastag to elemnt sof a list
        return [re.sub(rf'\b(?:{"|".join(hexlist)})\b', r'#\g<0>', elem) for elem in hexlist]

    def lum(self, colour):
        return np.sqrt(0.299 * colour[0] + 0.587 * colour[1] + 0.114 * colour[2])

    def on_press_convert(self, event):
        if self.cb3.GetValue() == True:  # input is hex
            hex_input = self.text_ctrl.GetValue()  # hex input

            list_hex_input = [hex_input]

            def add_hastag(hexlist):
                return [re.sub(rf'\b(?:{"|".join(hexlist)})\b', r'#\g<0>', elem) for elem in hexlist]

            input_add_hash = add_hastag(list_hex_input)

            hex_input_RGB = tuple(int(hex_input[i:i + 2], 16) for i in (0, 2, 4))  # turn hex input into rgb

            cmyk_value = self.rgb_to_cmyk(hex_input_RGB[0], hex_input_RGB[1], hex_input_RGB[2])

            cmyk_final_round = [np.round(float(i), 0) for i in cmyk_value]
            cmyk_final_round_int = [int(i) for i in cmyk_final_round]
            cmyk_final_round_int_tuple = tuple(cmyk_final_round_int)

            list_input = [["Input", input_add_hash[0], hex_input_RGB, cmyk_final_round_int_tuple, "Input"]]

            def app_lines(self):
                data = list_input
                for j in data:
                    self.list_ctrl.Append((j[0], j[1], j[2], j[3], j[4]))

            app_lines(self)

        elif self.cb2.GetValue() == True:
            cmyk_input = self.text_ctrl.GetValue() #cmyk input
            cmyk_input_list = [int(x) for x in cmyk_input.split(",")]
            cmyk_input_tuple = tuple(int(x) for x in cmyk_input.split(","))

            from_cmyk_to_rgb = self.cmyk_to_rgb(cmyk_input_list[0], cmyk_input_list[1], cmyk_input_list[2],
                                           cmyk_input_list[3])

            from_cmyk_to_rgb_rounded = tuple(map(lambda x: isinstance(x, float) and round(x, 0) or x, from_cmyk_to_rgb))
            from_cmyk_to_rgb_int = tuple(int(x) for x in from_cmyk_to_rgb_rounded)

            input_rgb_to_hex = [self.rgb_to_hex(from_cmyk_to_rgb_int)]

            input_add_hash = self.add_hastag(input_rgb_to_hex)

            list_input = [["Input", input_add_hash[0], from_cmyk_to_rgb_int, cmyk_input_tuple,"Input"]]

            def app_lines(self):
                data = list_input
                for j in data:
                    self.list_ctrl.Append((j[0], j[1], j[2], j[3], j[4]))

            app_lines(self)

        elif self.cb1.GetValue() == True:
            rgb_input = self.text_ctrl.GetValue() # rgb input
            rgb_input_list = [int(x) for x in rgb_input.split(",")]
            rgb_input_tuple = tuple(rgb_input_list)

            input_rgb_to_hex = [self.rgb_to_hex(rgb_input_tuple)]

            input_add_hash = self.add_hastag(input_rgb_to_hex)

            cmyk_value = self.rgb_to_cmyk(rgb_input_list[0], rgb_input_list[1], rgb_input_list[2])

            cmyk_final_round = [np.round(float(i), 0) for i in cmyk_value]
            cmyk_final_round_int = [int(i) for i in cmyk_final_round]
            cmyk_final_round_int_tuple = tuple(cmyk_final_round_int)

            list_input = [["Input", input_add_hash[0], rgb_input_tuple, cmyk_final_round_int_tuple, "Input"]]

            def app_lines(self):
                data = list_input
                for j in data:
                    self.list_ctrl.Append((j[0], j[1], j[2], j[3], j[4]))

            app_lines(self)

    def on_press(self, event):

        if self.cb3.GetValue() == True:  # input is hex
            try:
                hex_input = self.text_ctrl.GetValue()  # hex input
                hex_input_RGB = tuple(int(hex_input[i:i + 2], 16) for i in (0, 2, 4))  # turn hex input into rgb
                colour_input = hex_input_RGB
            except ValueError:
                wx.MessageBox('Hex code input is in a wrong format', 'Error', wx.OK | wx.ICON_ERROR)

        elif self.cb2.GetValue() == True:

            cmyk_input = self.text_ctrl.GetValue()  #cmyk Input

            cmyk_input_list = [int(x) for x in cmyk_input.split(",")]

            try:
                from_cmyk_to_rgb = self.cmyk_to_rgb(cmyk_input_list[0], cmyk_input_list[1], cmyk_input_list[2],
                                           cmyk_input_list[3])
            except IndexError:
                wx.MessageBox('CMYK input is in a wrong format.', 'Error', wx.OK | wx.ICON_ERROR)

            from_cmyk_to_rgb_rounded = tuple(map(lambda x: isinstance(x, float) and round(x, 0) or x, from_cmyk_to_rgb))
            from_cmyk_to_rgb_int = tuple(int(x) for x in from_cmyk_to_rgb_rounded)

            colour_input = from_cmyk_to_rgb_int

        elif self.cb1.GetValue() == True:

            rgb_input = self.text_ctrl.GetValue()
            rgb_input_list = [int(x) for x in rgb_input.split(",")]
            rgb_input_tuple = tuple(rgb_input_list)
            colour_input = rgb_input_tuple

        try:
            self.rgb_to_hex(colour_input)
        except TypeError:
            wx.MessageBox('RGB input is in a wrong format.', 'Error', wx.OK | wx.ICON_ERROR)

        colour_input_hex = self.rgb_to_hex(colour_input)

        # original lists before put to MySql
        # list_of_colors1 = []
        # list_of_colors2 = []

        if self.Cat_Choice.GetStringSelection() == "Catalogue1":
            list_of_colors = Catalogue1_big
            list_cat = ["Catalogue1"]
        elif self.Cat_Choice.GetStringSelection() == "Catalogue2":
            list_of_colors = Catalogue2_small
            list_cat = ["Catalogue2"]
        else:
            wx.MessageBox('Select a Catalogue', 'Info', wx.OK | wx.ICON_INFORMATION)

        list_of_colors = [[0, 165, 227], [255, 205, 31], [255, 203, 5], [254, 191, 51], [139, 0, 0], [165, 42, 42],
                          [178, 34, 34],
                          [220, 20, 60], [255, 0, 0], [255, 99, 71], [255, 127, 80], [205, 92, 92], [240, 128, 128],
                          [233, 150, 122],
                          [250, 128, 114], [255, 160, 122], [255, 69, 0], [255, 140, 0], [255, 165, 0], [255, 215, 0],
                          [184, 134, 11],
                          [218, 165, 32], [238, 232, 170], [189, 183, 107], [240, 230, 140], [128, 128, 0],
                          [255, 255, 0],
                          [154, 205, 50],
                          [85, 107, 47], [107, 142, 35], [124, 252, 0], [127, 255, 0], [173, 255, 47], [0, 100, 0],
                          [0, 128, 0], [34, 139, 34],
                          [0, 255, 0], [50, 205, 50], [144, 238, 144], [152, 251, 152], [143, 188, 143], [0, 250, 154],
                          [0, 255, 127], [46, 139, 87], [102, 205, 170], [60, 179, 113], [32, 178, 170], [47, 79, 79],
                          [0, 128, 128],
                          [0, 139, 139], [0, 255, 255], [224, 255, 255], [0, 206, 209], [64, 224, 208], [72, 209, 204],
                          [175, 238, 238],
                          [127, 255, 212], [176, 224, 230], [95, 158, 160], [70, 130, 180], [100, 149, 237],
                          [0, 191, 255],
                          [30, 144, 255],
                          [173, 216, 230], [135, 206, 235], [135, 206, 250], [25, 25, 112], [0, 0, 128], [0, 0, 139],
                          [0, 0, 205], [0, 0, 255],
                          [65, 105, 225], [138, 43, 226], [75, 0, 130], [72, 61, 139], [106, 90, 205], [123, 104, 238],
                          [147, 112, 219],
                          [139, 0, 139], [148, 0, 211], [153, 50, 204], [186, 85, 211], [128, 0, 128], [216, 191, 216],
                          [221, 160, 221],
                          [238, 130, 238], [255, 0, 255], [218, 112, 214], [199, 21, 133], [219, 112, 147],
                          [255, 20, 147],
                          [255, 105, 180],
                          [255, 182, 193], [255, 192, 203], [250, 235, 215], [245, 245, 220], [255, 228, 196],
                          [255, 235, 205], [245, 222, 179],
                          [255, 248, 220], [255, 250, 205], [250, 250, 210], [255, 255, 224], [139, 69, 19],
                          [160, 82, 45],
                          [210, 105, 30],
                          [205, 133, 63], [244, 164, 96], [222, 184, 135], [210, 180, 140], [188, 143, 143],
                          [255, 228, 181], [255, 222, 173],
                          [255, 218, 185], [255, 228, 225], [255, 240, 245], [250, 240, 230], [253, 245, 230],
                          [255, 239, 213],
                          [255, 245, 238], [245, 255, 250], [112, 128, 144], [119, 136, 153], [176, 196, 222],
                          [230, 230, 250], [255, 250, 240],
                          [240, 248, 255], [248, 248, 255], [240, 255, 240], [255, 255, 240], [240, 255, 255],
                          [255, 250, 250], [0, 0, 0],
                          [105, 105, 105], [128, 128, 128], [169, 169, 169], [192, 192, 192], [211, 211, 211],
                          [220, 220, 220], [245, 245, 245],
                          [255, 255, 255]]
        colours_ar = np.array(list_of_colors)

        values_cmc = []
        values_din99 = []
        values_itp = []
        values_euclidean = []
        values_redmean = []
        values_cam16ucs = []
        values_cam16scd = []
        values_cam16lcd = []
        values_cie1976b = []
        values_cie1994b = []
        values_cie2000b = []

        for k in list_of_colors:
            # CMC
            cmc = colour.delta_E(k, colour_input, 'cmc')
            values_cmc.append(cmc)
            values_cmc_array = np.asarray(values_cmc)
            index_of_smallest_cmc = np.where(values_cmc_array == min(values_cmc_array))
            smallest_distance_cmc_rgb= list_of_colors[index_of_smallest_cmc[0][0]]

            # din99
            din99 = colour.delta_E(k, colour_input, 'din99')
            values_din99.append(din99)
            values_din99_array = np.asarray(values_din99)
            index_of_smallest_din99 = np.where(values_din99_array == min(values_din99_array))
            smallest_distance_din99_rgb = list_of_colors[index_of_smallest_din99[0][0]]

            # itp
            itp = colour.delta_E(k, colour_input, 'itp')
            values_itp.append(itp)
            values_itp_array = np.asarray(values_itp)
            index_of_smallest_itp = np.where(values_itp_array == min(values_itp_array))
            smallest_distance_itp_rgb = list_of_colors[index_of_smallest_itp[0][0]]

            # Euclidean
            colours_k_ar = np.array(k)
            colour_input_ar = np.array(colour_input)
            distances_euclidean = np.sqrt(np.sum((colours_k_ar - colour_input_ar) ** 2))
            values_euclidean.append(distances_euclidean)
            values_euclidean_array = np.asarray(values_euclidean)
            index_of_smallest_euclidean = np.where(values_euclidean_array == np.amin(values_euclidean_array))
            smallest_distance_euclidean_rgb = list_of_colors[index_of_smallest_euclidean[0][0]]

            # redmean (weighted Euclidean)
            r_index = (1 / 2) * (k[0] + colour_input_ar[0])
            distances_redmean = np.sqrt(
                (2 + (r_index / 256)) * (k[0] - colour_input_ar[0]) ** 2 + 4 * (k[1] - colour_input_ar[1]) ** 2 +
                (2 + ((255 - r_index) / 256)) * (k[2] - colour_input_ar[2]) ** 2)
            values_redmean.append(distances_redmean)
            values_redmean_array = np.asarray(values_redmean)
            index_of_smallest_redmean = np.where(values_redmean_array == np.amin(values_redmean_array))
            smallest_distance_redmean_rgb = list_of_colors[index_of_smallest_redmean[0][0]]

            # CAM16-UCS
            cam16ucs = colour.delta_E(k, colour_input, 'CAM16-UCS')
            values_cam16ucs.append(cam16ucs)
            values_cam16ucs_array = np.asarray(values_cam16ucs)
            index_of_smallest_cam16ucs = np.where(values_cam16ucs_array == min(values_cam16ucs_array))
            smallest_distance_cam16ucs_rgb = list_of_colors[index_of_smallest_cam16ucs[0][0]]

            # CAM16-SCD
            cam16scd = colour.delta_E(k, colour_input, 'CAM16-SCD')
            values_cam16scd.append(cam16scd)
            values_cam16scd_array = np.asarray(values_cam16scd)
            index_of_smallest_cam16scd = np.where(values_cam16scd_array == min(values_cam16scd_array))
            smallest_distance_cam16scd_rgb = list_of_colors[index_of_smallest_cam16scd[0][0]]

            # CAM16-LCD
            cam16lcd = colour.delta_E(k, colour_input, 'CAM16-LCD')
            values_cam16lcd.append(cam16lcd)
            values_cam16lcd_array = np.asarray(values_cam16lcd)
            index_of_smallest_cam16lcd = np.where(values_cam16lcd_array == min(values_cam16lcd_array))
            smallest_distance_cam16lcd_rgb = list_of_colors[index_of_smallest_cam16lcd[0][0]]

            # CIE 1976
            cie1976b = colour.delta_E(k, colour_input, 'CIE 1976')
            values_cie1976b.append(cie1976b)
            values_cie1976b_array = np.asarray(values_cie1976b)
            index_of_smallest_cie1976b = np.where(values_cie1976b_array == min(values_cie1976b_array))
            smallest_distance_cie1976b_rgb = list_of_colors[index_of_smallest_cie1976b[0][0]]

            # CIE 1994
            cie1994b = colour.delta_E(k, colour_input, 'CIE 1994')
            values_cie1994b.append(cie1994b)
            values_cie1994b_array = np.asarray(values_cie1994b)
            index_of_smallest_cie1994b = np.where(values_cie1994b_array == min(values_cie1994b_array))
            smallest_distance_cie1994b_rgb = list_of_colors[index_of_smallest_cie1994b[0][0]]

            # CIE 2000
            cie2000b = colour.delta_E(k, colour_input, 'CIE 2000')
            values_cie2000b.append(cie2000b)
            values_cie2000b_array = np.asarray(values_cie2000b)
            index_of_smallest_cie2000b = np.where(values_cie2000b_array == min(values_cie2000b_array))
            smallest_distance_cie2000b_rgb = list_of_colors[index_of_smallest_cie2000b[0][0]]

        def convert_list_to_tuple(list):
            return tuple(i for i in list)

        smallest_distance_cmc_rgb_tuple = convert_list_to_tuple(smallest_distance_cmc_rgb)
        smallest_distance_din99_rgb_tuple = convert_list_to_tuple(smallest_distance_din99_rgb)
        smallest_distance_itp_rgb_tuple = convert_list_to_tuple(smallest_distance_itp_rgb)

        smallest_distance_euclidean_rgb_tuple = convert_list_to_tuple(smallest_distance_euclidean_rgb)
        smallest_distance_redmean_rgb_tuple = convert_list_to_tuple(smallest_distance_redmean_rgb)

        smallest_distance_cam16ucs_rgb_tuple = convert_list_to_tuple(smallest_distance_cam16ucs_rgb)
        smallest_distance_cam16scd_rgb_tuple = convert_list_to_tuple(smallest_distance_cam16scd_rgb)
        smallest_distance_cam16lcd_rgb_tuple = convert_list_to_tuple(smallest_distance_cam16lcd_rgb)

        smallest_distance_cie1976b_rgb_tuple = convert_list_to_tuple(smallest_distance_cie1976b_rgb)
        smallest_distance_cie1994b_rgb_tuple = convert_list_to_tuple(smallest_distance_cie1994b_rgb)
        smallest_distance_cie2000b_rgb_tuple = convert_list_to_tuple(smallest_distance_cie2000b_rgb)

        closest_hex_cmc = self.rgb_to_hex(smallest_distance_cmc_rgb_tuple)
        closest_hex_din99 = self.rgb_to_hex(smallest_distance_din99_rgb_tuple)
        closest_hex_itp = self.rgb_to_hex(smallest_distance_itp_rgb_tuple)

        closest_hex_Euclidean = self.rgb_to_hex(smallest_distance_euclidean_rgb_tuple)
        closest_hex_redmean = self.rgb_to_hex(smallest_distance_redmean_rgb_tuple)

        closest_hex_cam16ucs = self.rgb_to_hex(smallest_distance_cam16ucs_rgb_tuple)
        closest_hex_cam16scd = self.rgb_to_hex(smallest_distance_cam16scd_rgb_tuple)
        closest_hex_cam16lcd = self.rgb_to_hex(smallest_distance_cam16lcd_rgb_tuple)

        closest_hex_cie1976b = self.rgb_to_hex(smallest_distance_cie1976b_rgb_tuple)
        closest_hex_cie1994b = self.rgb_to_hex(smallest_distance_cie1994b_rgb_tuple)
        closest_hex_cie2000b = self.rgb_to_hex(smallest_distance_cie2000b_rgb_tuple)

        # summary of recommendations

        hex_list = [closest_hex_cmc, closest_hex_din99,
                    closest_hex_itp, closest_hex_Euclidean, closest_hex_redmean, closest_hex_cam16ucs,
                    closest_hex_cam16scd,
                    closest_hex_cam16lcd, closest_hex_cie1976b, closest_hex_cie1994b, closest_hex_cie2000b]

        rgb_list = [smallest_distance_cmc_rgb_tuple, smallest_distance_din99_rgb_tuple,
                    smallest_distance_itp_rgb_tuple, smallest_distance_euclidean_rgb_tuple,
                    smallest_distance_redmean_rgb_tuple, smallest_distance_cam16ucs_rgb_tuple,
                    smallest_distance_cam16lcd_rgb_tuple,
                    smallest_distance_cie1976b_rgb_tuple, smallest_distance_cie1994b_rgb_tuple,
                    smallest_distance_cie2000b_rgb_tuple]

        rgb_nodup = list(dict.fromkeys(rgb_list))
        
        # dictionary for our catalogue with calatogue's codes
        colour_dict = {"00a5e3": "534/5306", "ffcd1f": "112/3540", "ffcb05": "114/6660", "febf33": "209/3640"}

        # count and print summary in hex
        count_hex = dict(Counter(hex_list))
        count_num_votes_list = list(count_hex.values())
        count_rgb = dict(Counter(rgb_list))
        count_hex_count = list(count_hex.keys())
        count_rgb_count = list(count_rgb.keys())

        CMYK_final = []
        for i in count_rgb_count:
            k = self.rgb_to_cmyk(i[0], i[1], i[2])
            CMYK_final.append(k)

        cmyk_final_round = [[np.round(float(i), 0) for i in nested] for nested in CMYK_final]
        cmyk_final_round_int = [[int(i) for i in nested] for nested in cmyk_final_round]
        cmyk_final_round_int_tuple = [tuple(i) for i in cmyk_final_round_int]

        count_hex_count_hash = self.add_hastag(count_hex_count)

        cat_count = len(count_hex_count_hash)
        list_cat_improved = list_cat*cat_count

        combined_list = [[g, i, j, p, l] for g, i, j, p, l in zip(count_num_votes_list, count_hex_count_hash,
                                                      count_rgb_count,cmyk_final_round_int_tuple,list_cat_improved)]

        # sort the list descending by number of votes
        def Sort(sub_li):
            sub_li.sort(key=lambda x: x[0], reverse=True)
            return sub_li

        combined_list_sorted = Sort(combined_list)

        def app_lines(self):
            if self.only_highest_vote.GetValue() == True:
                data = combined_list_sorted[0]
                self.list_ctrl.Append((data[0], data[1], data[2], data[3], data[4]))
            else:
                data = combined_list_sorted
                for j in data:
                    self.list_ctrl.Append((j[0], j[1], j[2], j[3], j[4]))

        app_lines(self)

        # global prep for graphical

        if self.compare_colour_picture.GetValue() == True:

            res = list(zip(*combined_list_sorted))
            ordered_list = list(res[1])
            list_hex_input = [colour_input_hex]

            list_hex_input_hastag = self.add_hastag(list_hex_input)
            hex_list_input_final = list_hex_input_hastag + ordered_list

            count_num_votes_list.sort(reverse=True)

            if self.only_highest_vote.GetValue() == True:
                hastag_list = hex_list_input_final[0:2]  # hastag list is a list of strings
            else:
                hastag_list = hex_list_input_final

            count_num_votes_list_wordVotes = [", Votes: " + str(s) for s in count_num_votes_list]

            count_num_votes_list_wordVotes.insert(0, ", User's Input")

            k = list(zip(hastag_list, count_num_votes_list_wordVotes))

            # make string out of a list
            outlst = [''.join([str(c) for c in lst]) for lst in k]

            sns.palplot(hastag_list, size=3)

            ax = plt.gca()
            ax.set_title("Graphical Comparison of Closest Colours in One Palette")
            ax.set_xticklabels(outlst, multialignment='left', ha='left', fontsize=10)

            hastag_list_in_rgb = [self.hex_to_rgb(i) for i in hastag_list]

            for rgb, enu in zip(hastag_list_in_rgb, enumerate(hastag_list)):
                if self.lum(rgb) > 12.5:
                    ax.text(enu[0], 0, enu[1], fontsize=17.0, c="black", verticalalignment="baseline",
                            horizontalalignment="center")
                else:
                    ax.text(enu[0], 0, enu[1], fontsize=17.0, c="white", verticalalignment="baseline",
                            horizontalalignment="center")
            plt.show()

        if self.compare_colour_picture_pair.GetValue() == True:
            res = list(zip(*combined_list_sorted))
            ordered_list = list(res[1])
            list_hex_input = [colour_input_hex]

            def my_palplot(pal, size=1, ax=None):

                n = len(pal)
                if ax is None:
                    f, ax = plt.subplots(1, 1, figsize=(n * size, size))
                ax.imshow(np.arange(n).reshape(1, n),
                          cmap=mpl.colors.ListedColormap(list(pal)),
                          interpolation="nearest", aspect="auto")
                ax.set_xticks(np.arange(n) - .5)
                ax.set_yticks([-.5, .5])
                # Ensure nice border between colors
                ax.set_xticklabels(["" for _ in range(n)])
                # The proper way to set no ticks
                ax.yaxis.set_major_locator(ticker.NullLocator())

            list_hex_input_hastag = self.add_hastag(list_hex_input)
            hex_list_input_final = list_hex_input_hastag + ordered_list
            count_num_votes_list.sort(reverse=True)
            hastag_list = hex_list_input_final

            if self.only_highest_vote.GetValue() == True:
                hastag_list = hex_list_input_final[0:2]  # hastag list is a list of strings

                ordered_list_abv = [ordered_list[0]]

                ordered_list_hastag = ordered_list_abv # plotting uses ordered_list_hastag so I have to define it

                inputhex_list = list(colour_input_hex)

                count_num_votes_list_wordVotes = [", Votes: " + str(s) for s in count_num_votes_list]

                hastag_string_colour_in = '#' + colour_input_hex

                colour_input_hex_hastag = [hastag_string_colour_in]

                input_hastag_list_text = [hastag_string_colour_in + ", User's Input"]

                pairs = list(zip(colour_input_hex_hastag, ordered_list_abv))

                k2 = list(zip(ordered_list_abv, count_num_votes_list_wordVotes))

                hu = list(zip(input_hastag_list_text, k2))

                overall_list = list(zip(pairs, enumerate(hastag_list), hu))

            else:
                hastag_list = hex_list_input_final

                count_num_votes_list_wordVotes = [", Votes: " + str(s) for s in count_num_votes_list]

                n = len(ordered_list)
                lst_hex_input_n = [colour_input_hex] * n

                lst_hex_input_n_hastag = self.add_hastag(lst_hex_input_n)

                ordered_list_hastag = self.add_hastag(ordered_list)

                input_hastag_list_text = [str(i) + ", User's Input" for i in lst_hex_input_n_hastag]

                pairs = list(zip(lst_hex_input_n_hastag,ordered_list_hastag))

                k2 = list(zip(ordered_list_hastag, count_num_votes_list_wordVotes))

                hu = list(zip(input_hastag_list_text, k2))

                overall_list = list(zip(pairs,enumerate(hastag_list),hu))

            if len(ordered_list_hastag) == 1:
                count_num_votes_list_wordVotes.insert(0, ", User's Input")
                one_colour = list(zip(hastag_list, count_num_votes_list_wordVotes))
                sns.palplot(hastag_list, size=3)
                outlst = [''.join([str(c) for c in lst]) for lst in one_colour]
                ax = plt.gca()
                ax.set_title("Graphical Comparison of Closest Colours in Pairs")
                ax.set_xticklabels(outlst, multialignment='left', ha='left', fontsize=10)

                hastag_list_in_rgb = [self.hex_to_rgb(i) for i in hastag_list]

                for rgb, enu in zip(hastag_list_in_rgb, enumerate(hastag_list)):
                    if self.lum(rgb) > 12.5:
                        ax.text(enu[0], 0, enu[1], fontsize=17.0, c="black", verticalalignment="baseline",
                                horizontalalignment="center")
                    else:
                        ax.text(enu[0], 0, enu[1], fontsize=17.0, c="white", verticalalignment="baseline",
                                horizontalalignment="center")

            else:
                fig, axes = plt.subplots(1, len(ordered_list_hastag), figsize=(17, 3), sharey=True)
                fig.suptitle('Graphical Comparison of Closest Colours in Pairs')
                for i, o, j in overall_list:
                    outlst = [''.join([str(c) for c in lst]) for lst in j]
                    my_palplot(i, size=3, ax=axes[o[0]])
                    axes[o[0]].set_xticklabels(outlst, multialignment='left', ha='left', fontsize=10)

            plt.show()

    def on_press_compsel(self, e):
        compare = [i for i in range(self.list_ctrl.GetItemCount()) if self.list_ctrl.IsItemChecked(i)]

        chosen_list_hash = [self.list_ctrl.GetItemText(item = i, col =1) for i in compare]
        chosen_list_cat = [self.list_ctrl.GetItemText(item=i, col=4) for i in compare]

        sns.palplot(chosen_list_hash, size=3)

        ax = plt.gca()
        ax.set_title("Graphical Comparison of Selected Colours")
        ax.set_xticklabels(chosen_list_cat, multialignment='left', ha='left', fontsize=10)

        hastag_list_in_rgb = [self.hex_to_rgb(i) for i in chosen_list_hash]

        for rgb, enu in zip(hastag_list_in_rgb, enumerate(chosen_list_hash)):
            if self.lum(rgb) > 12.5:
                ax.text(enu[0], 0, enu[1], fontsize=17.0, c="black", verticalalignment="baseline",
                        horizontalalignment="center")
            else:
                ax.text(enu[0], 0, enu[1], fontsize=17.0, c="white", verticalalignment="baseline",
                        horizontalalignment="center")

        plt.show()

    def on_press_export(self, e):

        export = [i for i in range(self.list_ctrl.GetItemCount()) if self.list_ctrl.IsItemChecked(i)]

        df = pd.DataFrame()

        df['Votes'] = [self.list_ctrl.GetItemText(item=i, col=0) for i in export]
        df['Hex'] = [self.list_ctrl.GetItemText(item=i, col=1) for i in export]
        df['RGB'] = [self.list_ctrl.GetItemText(item=i, col=2) for i in export]
        df['CMYK'] = [self.list_ctrl.GetItemText(item=i, col=3) for i in export]
        df['Catalogue'] = [self.list_ctrl.GetItemText(item=i, col=4) for i in export]
        df['Catalogue Number'] = [self.list_ctrl.GetItemText(item=i, col=5) for i in export]

        fdlg = wx.FileDialog(self, "Input setting file path", "", "",
                             wildcard = "CSV files (*.csv)|*.csv|EXCEL files(*.xlsx)|*.xlsx",
                             style = wx.FD_SAVE|wx.FD_OVERWRITE_PROMPT)

        if fdlg.ShowModal() == wx.ID_OK:
                self.save_path = fdlg.GetPath() # saves path
        else:
            return

        if '.csv' in fdlg.GetPath():
            df.to_csv(self.save_path ,index=False)
        elif '.xlsx' in fdlg.GetPath():
            df.to_excel(self.save_path, index=False)

class ColoursApp(wx.App):
    def OnInit(self):
        self.frame = ColoursFrame(parent = None, title = "Closest Colour App")
        self.frame.Show()
        return True

if __name__ == "__main__":
    app = ColoursApp()
    app.MainLoop()












