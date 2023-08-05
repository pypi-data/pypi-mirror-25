# coding=utf-8

"""Test snntoolbox GUI."""


def test_gui():
    try:
        from snntoolbox.bin.gui.gui import tk, SNNToolboxGUI
    except ImportError:
        return
    import time

    root = tk.Tk()
    app = SNNToolboxGUI(root)
    root.update_idletasks()
    root.update()
    time.sleep(1)
    app.quit_toolbox()
