from win10toast import ToastNotifier

def NotifyMe(message):
    Notifi = ToastNotifier()  
    Notifi.show_toast("DZRT", message)