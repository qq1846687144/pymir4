from ctypes import windll, byref
from ctypes.wintypes import RECT, HWND
import win32con
import win32gui

SetWindowPos = windll.user32.SetWindowPos
GetClientRect = windll.user32.GetClientRect
GetWindowRect = windll.user32.GetWindowRect
EnableWindow = windll.user32.EnableWindow

SWP_NOSIZE = 0x0001
SWP_NOMOVE = 0X0002
SWP_NOZORDER = 0x0004


def move_window(handle: HWND, x: int, y: int):
    """移动窗口到坐标(x, y)

    Args:
        handle (HWND): 窗口句柄
        x (int): 横坐标
        y (int): 纵坐标
    """
    SetWindowPos(handle, 0, x, y, 0, 0, SWP_NOSIZE | SWP_NOZORDER)


def resize_window(handle: HWND, width: int, height: int):
    """设置窗口大小为width × height

    Args:
        handle (HWND): 窗口句柄
        width (int): 宽
        height (int): 高
    """
    SetWindowPos(handle, 0, 0, 0, width, height, SWP_NOMOVE | SWP_NOZORDER)


def move_windowa(handle: HWND, x: int, y: int):
    """移动窗口到坐标(x, y)

    Args:
        handle (HWND): 窗口句柄
        x (int): 横坐标
        y (int): 纵坐标
    """
    SetWindowPos(handle, -1, x, y, 0, 0, SWP_NOSIZE | SWP_NOZORDER)


def resize_windowa(handle: HWND, width: int, height: int):
    """设置窗口大小为width × height

    Args:
        handle (HWND): 窗口句柄
        width (int): 宽
        height (int): 高
    """
    SetWindowPos(handle, -1, 0, 0, width, height, SWP_NOMOVE | SWP_NOZORDER)


def resize_client(handle: HWND, width: int, height: int):
    """设置客户区大小为width × height

    Args:
        handle (HWND): 窗口句柄
        width (int): 宽
        height (int): 高
    """
    client_rect = RECT()
    GetClientRect(handle, byref(client_rect))
    delta_w = width - client_rect.right
    delta_h = height - client_rect.bottom
    window_rect = RECT()
    GetWindowRect(handle, byref(window_rect))
    current_width = window_rect.right - window_rect.left
    current_height = window_rect.bottom - window_rect.top
    resize_window(handle, current_width + delta_w, current_height + delta_h)


def lock_window(handle: HWND):
    """锁定窗口

    Args:
        handle (HWND): 窗口句柄
    """
    EnableWindow(handle, 0)


def unlock_window(handle: HWND):
    """解锁窗口

    Args:
        handle (HWND): 窗口句柄
    """
    EnableWindow(handle, 1)


def set_top(hwnd):
    """ 窗口置顶 """
    win32gui.SetWindowPos(hwnd, win32con.HWND_TOPMOST, 0, 0, 0, 0,
                          win32con.SWP_NOMOVE | win32con.SWP_NOACTIVATE | win32con.SWP_NOOWNERZORDER | win32con.SWP_SHOWWINDOW | win32con.SWP_NOSIZE)


def set_down(hwnd):
    """ 取消窗口置顶 """
    win32gui.SetWindowPos(hwnd, win32con.HWND_NOTOPMOST, 0, 0, 0, 0,
                          win32con.SWP_SHOWWINDOW | win32con.SWP_NOSIZE | win32con.SWP_NOMOVE)


def xianshi(hwnd):
    """ 显示窗口 """
    win32gui.ShowWindow(hwnd, win32con.SW_SHOW)


def yincang(hwnd):
    """ 隐藏窗口 """
    win32gui.ShowWindow(hwnd, win32con.SW_HIDE)


# if __name__ == "__main__":
#     # 需要和目标窗口同一权限，游戏窗口通常是管理员权限
#     import sys
#
#     if not windll.shell32.IsUserAnAdmin():
#         # 不是管理员就提权
#         windll.shell32.ShellExecuteW(
#             None, "runas", sys.executable, __file__, None, 1)
#
#     handle = windll.user32.FindWindowW(None, "Mir4G[1]")

