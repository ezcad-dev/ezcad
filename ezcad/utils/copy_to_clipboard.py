# -*- coding: utf-8 -*-
# Copyright (c) Ezcad Development Team. All Rights Reserved.
"""
Write image to clipboard in Windows OS.
"""

from io import BytesIO
try:
    import win32clipboard
except ImportError:
    print("WARNING: win32clipboard not found")
try:
    from PIL import Image
except ImportError:
    print("WARNING: PIL not found")


def send_to_clipboard(clip_type, data):
    win32clipboard.OpenClipboard()
    win32clipboard.EmptyClipboard()
    win32clipboard.SetClipboardData(clip_type, data)
    win32clipboard.CloseClipboard()


def copy_to_clipboard(filepath):
    image = Image.open(filepath)
    output = BytesIO()
    image.convert("RGB").save(output, "BMP")
    data = output.getvalue()[14:]
    output.close()
    send_to_clipboard(win32clipboard.CF_DIB, data)
