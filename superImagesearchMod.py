import cv2
import numpy as np
import pyautogui
import random
import time
import platform
import subprocess
import sys
import win32gui
import win32ui
import win32api
import win32con
from ctypes import windll
from PIL import Image
import win32com.client as comctl

is_retina = False
if platform.system() == "Darwin":
    is_retina = subprocess.call("system_profiler SPDisplaysDataType | grep 'retina'", shell=True)

MAIN_HWND = 0
def is_win_ok(hwnd, starttext):
    s = win32gui.GetWindowText(hwnd)
    if s.startswith(starttext):
            print(s)
            global MAIN_HWND
            MAIN_HWND = hwnd
            return None
    return 1
def find_main_window(starttxt):
    global MAIN_HWND
    win32gui.EnumChildWindows(0, is_win_ok, starttxt)
    return MAIN_HWND
def buscarElJuego(main_app):
    hwnd = win32gui.FindWindow(main_app)
    #print(hwnd)
    if hwnd < 1:
        hwnd = find_main_window(main_app)
    #print(hwnd)
    if hwnd:
        #win32gui.EnumChildWindows(hwnd, winfun, None)
        return hwnd

def buscarValorant(clase, nombre):
    return win32gui.FindWindow(clase, nombre)

def imagesearch(hwnd, image, precision=0.9):
    left, top, right, bot = win32gui.GetWindowRect(hwnd)
    w = right - left
    h = bot - top

    hwndDC = win32gui.GetWindowDC(hwnd)
    mfcDC = win32ui.CreateDCFromHandle(hwndDC)
    saveDC = mfcDC.CreateCompatibleDC()

    saveBitMap = win32ui.CreateBitmap()
    saveBitMap.CreateCompatibleBitmap(mfcDC, w, h)

    saveDC.SelectObject(saveBitMap)

    result = windll.user32.PrintWindow(hwnd, saveDC.GetSafeHdc(), 2)

    bmpinfo = saveBitMap.GetInfo()
    bmpstr = saveBitMap.GetBitmapBits(True)

    im = Image.frombuffer(
        'RGB',
        (bmpinfo['bmWidth'], bmpinfo['bmHeight']),
        bmpstr, 'raw', 'BGRX', 0, 1)
    if is_retina:
        im.thumbnail((round(im.size[0] * 0.5), round(im.size[1] * 0.5)))
    #im.save('testarea.png') #useful for debugging purposes, this will save the captured region as "testarea.png"
    img_rgb = np.array(im)
    img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
    template = cv2.imread(image, 0)
    template.shape[::-1]

    res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)

    win32gui.DeleteObject(saveBitMap.GetHandle())
    saveDC.DeleteDC()
    mfcDC.DeleteDC()
    win32gui.ReleaseDC(hwnd, hwndDC)

    if max_val < precision:
        return [-1, -1]
    return max_loc

def imagesearch_loop(hwnd, image, timesample, precision=0.9):
    # print("Finding " + image + " ... ", end="", flush=True)
    pos = imagesearch(hwnd, image, precision)
    while pos[0] == -1:
        time.sleep(timesample)
        pos = imagesearch(hwnd, image, precision)
        if pos[0] > -1:
            # print("OK")
            pass
    return pos

def presionarTecla(hwnd, keyType, key):
    if (keyType == "SYSKEY"):
        win32api.PostMessage(hwnd, win32con.WM_SYSKEYDOWN, key, 0)
        win32api.PostMessage(hwnd, win32con.WM_SYSKEYUP, key, 0)
    elif (keyType == "CHAR"):
        win32api.PostMessage(hwnd, win32con.WM_SYSKEYDOWN, ord(key), 0)
        win32api.PostMessage(hwnd, win32con.WM_SYSKEYUP, ord(key), 0)