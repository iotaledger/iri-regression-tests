from threading import Thread


def make_thread(target_method, *options):
    t = Thread(target=target_method, args=options)
    t.daemon = True
    t.start()
