import time
from ctypes import windll
import pyautogui
import aircv
import cv2
import numpy as np
import ckcz


# 读取客户端配置文件并实例化客户端配置文件类，输入为存储客户端名称的文本
class ReadClient:
    """客户端基类"""
    ClientCount = 0  # 客户端计数
    ClientStr = ""  # 客户端名称
    Clienthandles = []  # 客户端句柄,文本有几个存几个

    def __init__(self, file):  # 传入参数为文件名称（用文本记录客户端名称，客户端名称为窗口的标题名）
        self.file = file
        fo = open(self.file, "r", encoding='utf-8')  # 打开文件
        str1 = open(self.file, "r", encoding='utf-8').read()  # 以utf-8编码格式读取文件的内容
        str2 = str1.split(",")  # 将读取文件的内容以都逗号作为分隔符对字符串进行切片，每一个分割出来的客户端名称为一个项目
        fo.close()  # 关闭文件
        self.ClientCount = len(str2)  # 统计以
        self.ClientStr = str2
        for i in range(1, self.ClientCount + 1):  # range（1，3）为1，2 RP.PositionCount为实际数量，所以+1
            handle = windll.user32.FindWindowW(None, self.ClientStr[i - 1])  # 获取第i-1个客户端的句柄
            ckcz.move_window(handle, 0, 0)
            ckcz.resize_window(handle, 1285, 745)
            self.Clienthandles.append(handle)  # 将每一个客户端的句柄存入Clienthandles列表


# 前台截图并找图，输入为句柄和待找图片
class FindPicAndDoSomething:
    """找图和做事基类"""
    FindPicCont = 0

    def __init__(self, handle, image):  # 传入参数为文件名称（用文本记录客户端名称，客户端名称为窗口的标题名）
        self.bmp = None  # 临时截图
        self.handle = handle  # 传入的句柄
        self.image = image  # 传入的图片
        FindPicAndDoSomething.FindPicCont += 1  # 每增加一个对比图片的类就将计数加1
        self.confidence = 0  # 默认置信度为0
        self.dic = None  # 默认找图返回字典为空
        self.center = 0  # 默认找图中心点为0

    def ReScreenshot(self):  # 重新截图并找原图
        ckcz.set_top(self.handle)  # 置顶窗口（必需前台找图，所以置顶）
        ckcz.set_down(self.handle)  # 取消置顶窗口
        self.dic = None
        self.confidence = 0  # 默认置信度为0
        self.FindPic()

    def ReFindPic(self, newimage):  # 重新截图并找新图
        ckcz.set_top(self.handle)  # 置顶窗口（必需前台找图，所以置顶）
        ckcz.set_down(self.handle)  # 取消置顶窗口
        self.dic = None
        self.image = newimage  # 重新定义要查找的图片
        self.bmp = pyautogui.screenshot(region=[0, 0, 1285, 745])  # 前台截图
        self.bmp = cv2.cvtColor(np.asarray(self.bmp), cv2.COLOR_RGB2BGR)  # cvtColor用于在图像中不同的色彩空间进行转换,用于后续处理。
        self.FindPic()

    def FindPic(self):  # 找图
        ckcz.set_top(self.handle)  # 置顶窗口（必需前台找图，所以置顶）
        self.bmp = pyautogui.screenshot(region=[0, 0, 1285, 745])  # 前台截图
        self.bmp = cv2.cvtColor(np.asarray(self.bmp), cv2.COLOR_RGB2BGR)  # cvtColor用于在图像中不同的色彩空间进行转换,用于后续处理。
        self.dic = aircv.find_template(self.bmp, aircv.imread(self.image))  # 查找后台截图与前台输入图片进行对比
        ckcz.set_down(self.handle)  # 取消置顶窗口
        if self.dic:
            print("找到图片" + self.image)
            self.confidence = self.dic['confidence']
            print("图片" + self.image + "可信度为：", self.confidence)
            self.center = self.dic['result']
        else:
            print("未找到图片" + self.image)
        return self.dic

    def FindPicConfidence(self):  # 返回找图相似度
        return self.confidence

    def FindPicCenter(self):  # 返回找图中心点
        return self.center

    def ClickCenter(self, x, y):  # 点击找图中心点，x，y为中心点的偏移
        ckcz.set_top(self.handle)  # 置顶窗口（必需前台找图，所以置顶）
        ckcz.set_down(self.handle)  # 取消置顶窗口
        if self.confidence > 0.9:
            time.sleep(0.1)
            pyautogui.moveTo(self.center[0] + x, self.center[1] + y, duration=1)  # 鼠标漂移至中心
            time.sleep(0.1)
            pyautogui.click(self.center[0] + x, self.center[1] + y)  # 鼠标点击中心
            print("单击图片" + self.image)

    def NoPicClickCenter(self, x, y):  # 没有找到图点击某个点，x，y为中心点的偏移
        ckcz.set_top(self.handle)  # 置顶窗口（必需前台找图，所以置顶）
        ckcz.set_down(self.handle)  # 取消置顶窗口
        if self.confidence < 0.9:
            time.sleep(0.1)
            pyautogui.moveTo(self.center[0] + x, self.center[1] + y, duration=1)  # 鼠标漂移至中心
            time.sleep(0.1)
            pyautogui.click(self.center[0] + x, self.center[1] + y)  # 鼠标点击中心


# 省电模式类，包含退出省电模式和进入省电模式
class Sdms:
    """退出省电模式类"""

    def __init__(self, handle):  # 传入参数为handle
        self.handle = handle

    def Tcsdms(self):
        ckcz.set_top(self.handle)  # 置顶窗口（必需前台找图，所以置顶）
        ckcz.set_down(self.handle)  # 取消置顶窗口
        pyautogui.moveTo(520.0, 520.0, duration=1)
        pyautogui.mouseDown()  # 鼠标按下
        pyautogui.dragTo(740, 520, duration=1)  # 拖拽
        pyautogui.mouseUp()  # 鼠标释
        pyautogui.moveTo(640.0, 640.0, duration=1)  # 确认
        print("退出省电模式")
        time.sleep(0.1)
        pyautogui.click(640.0, 640.0)  # 确认
        pyautogui.press('esc')  # 按下并释放esc
        time.sleep(0.1)
        pyautogui.press('esc')  # 按下并释放esc
        time.sleep(0.1)
        pyautogui.press('esc')  # 按下并释放esc
        time.sleep(0.1)
        pyautogui.press('esc')  # 按下并释放esc
        time.sleep(0.1)
        pyautogui.press('esc')  # 按下并释放esc
        time.sleep(0.1)

    def Jrsdms(self):  # 进入省电模式
        ckcz.set_top(self.handle)  # 置顶窗口（必需前台找图，所以置顶）
        ckcz.set_down(self.handle)  # 取消置顶窗口
        pyautogui.press('esc')  # 按下并释放esc
        time.sleep(0.1)
        pyautogui.press('esc')  # 按下并释放esc
        time.sleep(0.1)
        pyautogui.press('esc')  # 按下并释放esc
        time.sleep(0.1)
        print("进入省电模式")
        pyautogui.moveTo(1240.0, 60.0, duration=1)  # 加号
        time.sleep(0.1)
        pyautogui.click(1240.0, 60.0)  # 加号
        print("点击加号")
        time.sleep(0.1)
        pyautogui.moveTo(150.0, 560.0, duration=1)  # 省电模式
        time.sleep(0.1)
        pyautogui.click(150.0, 560.0)  # 省电模式
        print("点击省电模式")
        time.sleep(0.1)


# 进入魔方阵待确认窗口，也就是没点进入的时候
def mfz(handle):  # 进入魔方阵
    ckcz.set_top(handle)  # 置顶窗口（必需前台找图，所以置顶）
    ckcz.set_down(handle)  # 取消置顶窗口
    pyautogui.moveTo(1240, 60, duration=1.3)  # 1240,60加号
    time.sleep(0.1)
    pyautogui.click(1240, 60)  # 1240,60加号
    print("点击右上角大加号")
    time.sleep(0.1)
    pyautogui.moveTo(950, 485, duration=1.2)  # 950，485次元门
    time.sleep(0.1)
    pyautogui.click(950, 485)  # 950，485次元门
    print("点击次元门")
    time.sleep(0.1)
    pyautogui.moveTo(950, 580, duration=1.2)  # 950，580魔方阵
    time.sleep(0.1)
    pyautogui.click(950, 580)  # 950，580魔方阵
    time.sleep(0.1)
    print("点击魔方阵")
    pyautogui.moveTo(405, 602, duration=1.2)  # 405，602魔方阵第4层
    time.sleep(0.1)
    pyautogui.click(405, 602)  # 405，602魔方阵第4层
    time.sleep(0.1)
    print("点击魔方阵第4层")
    # pyautogui.moveTo(945, 700, duration=1.2)  # 945，700进入魔方阵
    # time.sleep(0.1)
    # pyautogui.click(945, 700)  # 945，700进入魔方阵
    # pyautogui.press('esc')  # 按下并释放esc
    # time.sleep(0.1)
    # pyautogui.press('esc')  # 按下并释放esc
    # time.sleep(0.1)
    # pyautogui.press('esc')  # 按下并释放esc
    # time.sleep(0.1)
    # pyautogui.press('esc')  # 按下并释放esc
    # time.sleep(0.1)
    # pyautogui.press('esc')  # 按下并释放esc
    # time.sleep(0.1)
    # pyautogui.moveTo(190, 290, duration=1)  # 1240,60加号950，485次元门，950，580魔方阵405，602 第4层 945，700进入
    # time.sleep(0.1)
    # pyautogui.click(190, 290)  # 道观

    # pyautogui.click(190, 290)  # 道观


# 确认进入魔方阵，也就是点一下进入
def mfzqr(handle):
    time.sleep(0.1)
    pyautogui.moveTo(945, 700, duration=1.2)  # 945，700进入魔方阵
    time.sleep(0.1)
    pyautogui.click(945, 700)  # 945，700进入魔方阵
    print("点击进入魔方阵")
    time.sleep(1)
    esc4()


# 按四次esc
def esc4():
    pyautogui.press('esc')  # 按下并释放esc
    time.sleep(0.1)
    pyautogui.press('esc')  # 按下并释放esc
    time.sleep(0.1)
    pyautogui.press('esc')  # 按下并释放esc
    time.sleep(0.1)
    pyautogui.press('esc')  # 按下并释放esc
    time.sleep(0.1)
    pyautogui.press('esc')  # 按下并释放esc
    time.sleep(0.1)


# 进入自动延时界面，并点击一下
def zdys(handle):  # 自动延时确认界面
    ckcz.set_top(handle)  # 置顶窗口（必需前台找图，所以置顶）
    ckcz.set_down(handle)  # 取消置顶窗口
    pyautogui.moveTo(1024, 188, duration=1.3)  # 小加号
    time.sleep(0.1)
    pyautogui.click(1024, 188)  # 小加号
    time.sleep(0.1)
    pyautogui.moveTo(755, 210, duration=1.2)  # 755，210自动延长
    time.sleep(0.1)
    pyautogui.click(755, 210)  # 755，210自动延长
    time.sleep(0.1)
    pyautogui.moveTo(712, 333, duration=1.2)  # 712，333延时次数
    time.sleep(0.1)
    pyautogui.click(712, 333)  # 712，333延时次数第一次
    time.sleep(0.5)
    # pyautogui.click(712, 333)  # 712，333延时次数第二次
    # time.sleep(0.5)
    # pyautogui.moveTo(645, 600, duration=1.2)  # 自动延长
    # time.sleep(0.1)
    # pyautogui.click(645, 600)  # 自动延长
    # time.sleep(0.1)
    # pyautogui.press('esc')  # 按下并释放esc
    # time.sleep(0.1)
    # pyautogui.press('esc')  # 按下并释放esc
    # time.sleep(0.1)
    # pyautogui.press('esc')  # 按下并释放esc
    # time.sleep(0.1)
    # pyautogui.press('esc')  # 按下并释放esc
    # time.sleep(0.1)
    # pyautogui.press('esc')  # 按下并释放esc
    # time.sleep(0.1)
    # # pyautogui.moveTo(190, 290, duration=1)  # 1240,60加号950，485次元门，950，580魔方阵405，602 第4层 945，700进入
    # # time.sleep(0.1)
    # # pyautogui.click(190, 290)  # 道观


# 确认点击自动延时
def zdysqr(handle):
    time.sleep(0.5)
    pyautogui.moveTo(645, 600, duration=1.2)  # 自动延长
    time.sleep(0.1)
    pyautogui.click(645, 600)  # 自动延长
    time.sleep(0.1)
    esc4()


def ys(handle):  # 点击延时2次
    ckcz.set_top(handle)  # 置顶窗口（必需前台找图，所以置顶）
    ckcz.set_down(handle)  # 取消置顶窗口
    pyautogui.moveTo(1024, 188, duration=1.3)  # 小加号
    time.sleep(0.1)
    pyautogui.click(1024, 188)  # 小加号
    time.sleep(0.1)
    pyautogui.moveTo(640, 600, duration=1.2)  # 755，210自动延长
    time.sleep(0.1)
    pyautogui.click(640, 600)  # 712，333延时次数第一次
    time.sleep(0.5)
    pyautogui.press('esc')  # 按下并释放esc
    time.sleep(0.1)
    pyautogui.press('esc')  # 按下并释放esc
    time.sleep(0.1)
    pyautogui.press('esc')  # 按下并释放esc
    time.sleep(0.1)
    pyautogui.press('esc')  # 按下并释放esc
    time.sleep(0.1)
    pyautogui.press('esc')  # 按下并释放esc
    time.sleep(0.1)
    # pyautogui.moveTo(190, 290, duration=1)  # 1240,60加号950，485次元门，950，580魔方阵405，602 第4层 945，700进入
    # time.sleep(0.1)
    # pyautogui.click(190, 290)  # 道观


# 点击复活按钮
def fh():
    """点复活"""
    pyautogui.moveTo(1140.0, 640.0, duration=0.5)  ##1140 640复活
    time.sleep(0.1)
    pyautogui.click(1140.0, 640.0)
    time.sleep(0.1)


# 自动魔方阵
class Zdmfz:
    """自动进入魔方阵"""

    def __init__(self, handle, image):  # 传入参数为文件名称（用文本记录客户端名称，客户端名称为窗口的标题名）
        self.image = image  # 传入的图片
        self.handle = handle  # 传入的句柄
        self.Cl1Sdms = Sdms(self.handle)
        self.HTzw = FindPicAndDoSomething(self.handle, self.image)  # 创建判断是否在地图，判断是否找到相应地图的图片
        self.Cl1IsSdms = FindPicAndDoSomething(self.handle, "sdms.png")  # 判断是否在省电模式
        self.Cl1Mfz = FindPicAndDoSomething(self.handle, "mfz.png")  # 判断是否在魔方阵
        self.IsDie = FindPicAndDoSomething(self.handle, "fh.png")  # 创建判断是否死亡类，判断是否找到复活的图片
        self.Kyd = FindPicAndDoSomething(self.handle, "kyd.png")  # 判断是否可以移动
        self.MfzCs = FindPicAndDoSomething(self.handle, "wcs.png")  # 创建判断魔方阵次数类，判断是否找到无次数的图片
        self.SFzdwk = FindPicAndDoSomething(self.handle, "zdwk.png")  # 退回主界面后判断是否在自动挖矿
        self.QrZdys = FindPicAndDoSomething(self.handle, "mfzys.png")  # 判断是否有魔方阵免费次数
        self.MfzZw = FindPicAndDoSomething(self.handle, "mfzzw.png")  # 判断是否在魔方阵某个之屋内
        self.SFyys = FindPicAndDoSomething(self.handle, "yys.png")  # 判断是否在魔方阵某个之屋内

    # 自动进地图
    def zdjdt(self):
        self.HTzw.ReScreenshot()  # 重新截屏是否在想要的地图，重置可信度
        while self.HTzw.confidence < 0.9:  # 不在想要的地图
            print("不在想要的地图")
            time.sleep(0.5)
            self.Kyd.ClickCenter(0, -37)  # 点击移动按钮-37是其距离可移动三个字的距离
            print("移动中")
            time.sleep(0.1)
            self.Kyd.ReScreenshot()  # 重新截屏是否可以移动，重置可信度
            time.sleep(0.1)
            self.HTzw.ReScreenshot()  # 重新截屏是否在想要的地图，重置可信度
        self.SFzdwk.ReScreenshot()  # 实时截图判断是否自动挖矿
        if self.SFzdwk.confidence > 0.9:
            print("在自动挖矿")
        else:
            pyautogui.press('n')  # 按下快捷键自动挖矿
            print("已经在自动挖矿")

    def gogogo(self):
        self.Cl1IsSdms.ReScreenshot()
        print("正在判断是否在省电模式")
        # 在省电模式则退出省电模式，不在不干任何事情
        if self.Cl1IsSdms.confidence > 0.9:
            print("在省电模式")
            print("省电模式可信度:", self.Cl1IsSdms.confidence)
            self.Cl1Sdms.Tcsdms()  # 退出省电模式
        else:
            print("不在省电模式")

        self.Cl1Mfz.ReScreenshot()  # 重新截图找图，是否在魔方阵，重置可信度
        self.MfzZw.ReScreenshot()  # 重新截图找图，是否在魔方阵某个之屋内，重置可信度
        # 如果不在魔方阵
        if self.Cl1Mfz.confidence < 0.9 and self.MfzZw.confidence < 0.9:  # 如果不在魔方阵
            print("不在魔方阵++++++++")
            mfz(self.handle)  # 点击到魔方阵层数选择页面
            self.MfzCs.ReScreenshot()  # 判断魔方阵次数，判断是否找到无次数的图片，>0.9无次数，小于还有次数
            # 如果有次数
            if self.MfzCs.confidence < 0.9:  # 如果有次数
                print("有次数")
                mfzqr(self.handle)  # 确认进入魔方阵
                time.sleep(5)
                self.SFyys.ReScreenshot()  # 实时截图判断是否已经有延时
                if self.SFyys.confidence > 0.9:
                    print("已经自动延时中2222222")
                    esc4()
                    self.zdjdt()  # 自动进地图开挖
                else:
                    zdys(self.handle)  # 打开自动延时界面并点击+号一次
                    self.QrZdys.ReScreenshot()  # 实时截图判断是否有魔方阵免费次数
                    # 如果有免费的延时次数
                    if self.QrZdys.confidence > 0.9:  # 如果有免费次数
                        print("有免费延长次数222222222")
                        zdysqr(self.handle)  # 确认点击自动延时
                        self.zdjdt()  # 自动进地图开挖
                    # 如果无免费的延时次数
                    else:  # 如果无免费的延时次数
                        print("没有免费延长次数2222222")
                        esc4()
                        self.zdjdt()  # 自动进地图开挖
            # 如果没有次数
            else:
                print("没有次数")
                esc4()  # 退回主界面
                self.SFzdwk.ReScreenshot()  # 重新查看是否自动挖矿
                # 在自动挖矿
                if self.SFzdwk.confidence > 0.9:
                    print("在自动挖矿")
                    self.Cl1Sdms.Jrsdms()  # 进入省电模式
                # 不在自动挖矿，则点击自动挖矿
                else:
                    print("将要开始自动挖矿")
                    time.sleep(1)
                    pyautogui.press('n')  # 按下快捷键自动挖矿
                    self.Cl1Sdms.Jrsdms()  # 进入省电模式
            # 如果在魔方阵
        # 如果在魔方阵
        else:  # 如果在魔方阵
            esc4()
            print("在魔方阵++++++++")
            time.sleep(5)
            self.SFyys.ReScreenshot()  # 实时截图判断是否已经有延时
            if self.SFyys.confidence > 0.9:
                print("已经自动延时中2222222")
                esc4()
                self.zdjdt()  # 自动进地图开挖
            else:
                zdys(self.handle)  # 打开自动延时界面并点击+号一次
                self.QrZdys.ReScreenshot()  # 实时截图判断是否有魔方阵免费次数
                # 如果有免费的延时次数
                if self.QrZdys.confidence > 0.9:  # 如果有免费次数
                    print("有免费延时次数++++++++")
                    zdysqr(self.handle)  # 确认点击自动延时
                    self.zdjdt()  # 自动进地图开挖
                # 如果无免费的延时次数
                else:  # 如果无免费的延时次数
                    esc4()
                    print("无免费延时次数++++++++")
                    self.zdjdt()  # 自动进地图开挖




RC = ReadClient("client.txt")  # 读取客户端配置文件并实例化客户端配置文件类
Cl1Zdmfz = Zdmfz(RC.Clienthandles[0], "htzw.png")
i = 0
while i < 90:
    Cl1Zdmfz.gogogo()
    i = i + 1
    time.sleep(60)
# # # ddd = FindPicAndDoSomething(RC.Clienthandles[0], "kyd.png")
# qqq = FindPicAndDoSomething(RC.Clienthandles[1], "htzw.png")
# aaa = FindPicAndDoSomething(RC.Clienthandles[1], "kyd.png")
# while qqq.confidence < 0.9:
#     time.sleep(0.5)
#     aaa.ClickCenter(0, -37)
#     time.sleep(0.1)
#     aaa.ReScreenshot()
#     time.sleep(0.1)
#     qqq.ReScreenshot()
