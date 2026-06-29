class BulkCoxBind:
    def __init__(self, main_window, bulk_cox_ui):
        self.main_window = main_window
        self.bulk_cox_ui = bulk_cox_ui
        self.bind_signals()

    def bind_signals(self):
        self.bulk_cox_ui.btn_back_bulk_cox.clicked.connect(self.go_to_home_page)
        # 音乐控件由MusicController自动处理

    def go_to_home_page(self):
        self.main_window.go_to_home_page()