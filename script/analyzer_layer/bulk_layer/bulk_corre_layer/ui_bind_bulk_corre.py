class BulkCorreBind:
    def __init__(self, main_window, bulk_corre_ui):
        self.main_window = main_window
        self.bulk_corre_ui = bulk_corre_ui
        self.bind_signals()

    def bind_signals(self):
        self.bulk_corre_ui.btn_back_bulk_corre.clicked.connect(self.go_to_home_page)
        # 音乐控件由MusicController自动处理

    def go_to_home_page(self):
        self.main_window.go_to_home_page()