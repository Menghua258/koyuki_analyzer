class WgcnaBind:
    def __init__(self, main_window, wgcna_ui):
        self.main_window = main_window
        self.wgcna_ui = wgcna_ui
        self.bind_signals()

    def bind_signals(self):
        self.wgcna_ui.btn_back_wgcna.clicked.connect(self.go_to_home_page)
        # 音乐控件由MusicController自动处理

    def go_to_home_page(self):
        self.main_window.go_to_home_page()