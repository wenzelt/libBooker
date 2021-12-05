from xvfbwrapper import Xvfb


def start_virtual_displays():
    vdisplay = Xvfb()
    vdisplay.start()
    return vdisplay


def stop_virtual_displays(vdisplay: Xvfb):
    vdisplay.stop()
    return None
