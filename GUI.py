import tkinter
import tkinter.filedialog
import webbrowser
from os import path

from bs4 import BeautifulSoup
import requests
from tensorflow.keras.applications.vgg16 import VGG16, preprocess_input, decode_predictions
from tensorflow.keras.preprocessing import image
import numpy as np
import PIL.Image
import PIL.ImageTk


class Application(tkinter.Tk):
    empty_list = ["", "", "", "", ""]
    tag_list = ["0", "1", "2", "3", "4", "5"]

    def __init__(self):
        super().__init__()

        self.str = ""

        # キャンバスのサイズ
        self.canvas_width = 400
        self.canvas_height = 400

        # アプリのウィンドウのサイズ設定
        self.geometry("1000x430")

        # キャンバスの作成と配置
        self.before_canvas = tkinter.Canvas(
            self,
            width=self.canvas_width,
            height=self.canvas_height,
            bg="gray"
        )
        self.before_canvas.grid(row=1, column=1)

        # テキストボックスの作成と配置
        # 説明
        self.txt1 = tkinter.Text(self, width=72, height=10)
        self.txt1.insert(tkinter.END,
                         "\n"
                         " 使い方  * 実行にはしばらく時間がかかります。連打しないでください。\n\n"
                         " 1、最初に、画像選択をクリックして画像を選んでください。\n\n"
                         " 2、次に、実行をクリックしたら画像認識が始まります。\n"
                         " 　　実行すると一致率が％表示で上位５つ出ます。\n\n"
                         " 3、最後に、実行した後に各色にあった下のボタンを押すと検索ができます。"
                         )
        self.txt1.grid(row=1, column=3)
        self.txt1.place(x=480, y=0)

        # テキストボックスの作成と配置
        # 結果
        self.txt2 = tkinter.Text(self, width=72, height=12, relief=tkinter.SOLID, bd=3, font=("MS 明朝", 10))
        self.txt2.insert(tkinter.END, "\n"" ここに色付きで結果が表示されます")
        self.txt2.grid(row=1, column=3)
        self.txt2.place(x=480, y=137)

        # ボタンを配置するフレームの作成と配置
        self.button_frame = tkinter.Frame()
        self.button_frame.grid(row=1, column=2)
        self.button_frame.place(x=410, y=170)

        # ファイル読み込みボタンの作成と配置
        self.load_button = tkinter.Button(
            self.button_frame,
            borderwidth="5",
            text="画像選択",
            command=self.push_load_button

        )
        self.load_button.pack()

        # 画像実行ボタンの作成と配置
        self.zoom_button = tkinter.Button(
            self.button_frame,
            borderwidth="5",
            text="実行",
            command=self.push_zoom_button
        )
        self.zoom_button.pack()

        self.button_search = tkinter.Frame()
        self.button_search.grid(row=2, column=3)

        # -------------------------------------------------------------------------------
        self.search_button = tkinter.Button(
            text="No.1",
            borderwidth="5",
            font=("", "9", "bold"),
            width=10,
            height=5,
            bg="yellow",
            command=lambda: self.push_search_button(0)
        )
        self.search_button.place(x=495, y=310)
        # -------------------------------------------------------------------------------
        self.search_button2 = tkinter.Button(
            text="No.2",
            borderwidth="5",
            font=("", "9", "bold"),
            width=10,
            height=5,
            bg="turquoise1",
            command=lambda: self.push_search_button(1)
        )
        self.search_button2.place(x=595, y=310)
        # -------------------------------------------------------------------------------
        self.search_button3 = tkinter.Button(
            text="No.3",
            borderwidth="5",
            font=("", "9", "bold"),
            bg="green2",
            width=10,
            height=5,
            command=lambda: self.push_search_button(2)
        )
        self.search_button3.place(x=695, y=310)
        # -------------------------------------------------------------------------------
        self.search_button4 = tkinter.Button(
            text="No.4",
            borderwidth="5",
            font=("", "9", "bold"),
            bg="maroon1",
            width=10,
            height=5,
            command=lambda: self.push_search_button(3)
        )
        self.search_button4.place(x=795, y=310)
        # -------------------------------------------------------------------------------
        self.search_button5 = tkinter.Button(
            text="No.5",
            borderwidth="5",
            font=("", "9", "bold"),
            bg="purple2",
            width=10,
            height=5,
            command=lambda: self.push_search_button(4)
        )
        self.search_button5.place(x=895, y=310)

        # 画像オブジェクトの設定（初期はNone）
        self.before_image = None

        # キャンバスに描画中の画像（初期はNone）
        self.before_canvas_obj = None

    def push_load_button(self):
        # 'ファイル選択ボタンが押された時の処理'

        iDir = path.dirname("C:\bunnkasai\imagefile")
        # ファイル選択画面を表示
        file_path = tkinter.filedialog.askopenfilename(
            initialdir=iDir
        )

        if len(file_path) != 0:

            # Tkinter用画像オブジェクトの作成
            self.before_image = PIL.ImageTk.PhotoImage(file=file_path)
            self.str = file_path
            image2 = PIL.Image.open(file_path)
            xt = image2.width
            yt = image2.height
            while xt >= 300 and yt >= 300:
                    xt = xt/1.5
                    yt = yt/1.5

            #  画像の比率をそのままで合わせる
            resized_image = image2.resize((int(xt), int(yt)))
            self.before_image = PIL.ImageTk.PhotoImage(resized_image)

            # 画像の描画位置を調節
            x = int(self.canvas_width / 2)
            y = int(self.canvas_height / 2)

            # キャンバスに描画中の画像を削除
            if self.before_canvas_obj is not None:
                self.before_canvas.delete(self.before_canvas_obj)

            # 画像キャンバスに描画
            self.before_canvas_obj = self.before_canvas.create_image(
                x, y,
                image=self.before_image

            )

    #  対応した実行結果の画像を検索する

    def push_search_button(self, index):

        self.n = self.empty_list[index]
        ur = f'https://www.google.com/search?q={self.n}&rlz=1C1AGAK_jaJP963JP964&source=lnms&tbm=isch&sa=X&ved=2ahUKEwjfx5vOur34AhUPnFYBHfCeBeMQ_AUoAXoECAIQAw&biw=1366&bih=625&dpr=1'
        webbrowser.open(ur, new=0, autoraise=True)

    def push_zoom_button(self):
        i = 0
        self.txt2.delete("1.0", "end")
        model = VGG16(weights='imagenet')
        selectimage = self.str
        img = image.load_img(selectimage, target_size=(224, 224))
        array = image.img_to_array(img)
        array = np.expand_dims(array, axis=0)
        preds = model.predict(preprocess_input(array))
        results = decode_predictions(preds, top=5)[0]
        for result in results:
            num = result[1].replace('_', '-')
            self.empty_list[i] = num
            i += 1
            url = f'https://ejje.weblio.jp/content/{num}'
            # r = requests.get(url)
            # soup = BeautifulSoup(r.text, "html.parser")
            # elems = soup.select('body>#contentWrp>#contentBodyWrp>#contentBody>#main> '
            #                     'div.mainBlock.non-member.hlt_SUMRY > div.summaryM.descriptionWrp >'
            #                     ' p > span.content-explanation.ej')
            # st = elems[0].text
            # st2 = st.replace(' ', '')
            # st4 = st2.replace('\n', '')
            st3 = "・・・" + ('{:.4}'.format(float(result[2]) * 100)) + "%\n"
            self.txt2.insert(tkinter.END, "\n", '999')
            self.txt2.insert(tkinter.END, num, self.tag_list[i])
            self.txt2.insert(tkinter.END, st3, self.tag_list[i])
            self.txt2.tag_config('1', background="yellow")
            self.txt2.tag_config('2', background="turquoise1")
            self.txt2.tag_config('3', background="green2")
            self.txt2.tag_config('4', background="maroon1")
            self.txt2.tag_config('5', background="purple1")
            self.txt2.tag_config('999', background="white")


app = Application()
app.title('画像認識プログラム')
app.mainloop()