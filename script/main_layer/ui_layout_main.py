# -*- coding: utf-8 -*-
"""
主界面UI布局脚本 - 只负责创建控件、规划窗口布局、摆放按钮/输入框/画布、设置样式尺寸
完全不写按钮点击、触发逻辑

使用 5 函数模组开发模型：主界面组件使用 gui_styles(variant='main')
"""

from script.utils_layer.import_config import *
from script.utils_layer.utils_tools import ScalableLabel
from script.utils_layer.gui_styles import create_styled_button, create_styled_combo_box, create_styled_slider
from script.analyzer_layer.scRNAseq_layer.initial_analysis_layer.ui_layout_initial_analysis import InitialAnalysisPageUI
from script.analyzer_layer.scRNAseq_layer.violin_layer.ui_layout_violin import ViolinPageUI
from script.analyzer_layer.scRNAseq_layer.diff_layer.ui_layout_diff import DiffPageUI
from script.analyzer_layer.bulk_layer.bulk_expr_layer.ui_layout_bulk_expr import BulkExprPageUI
from script.analyzer_layer.bulk_layer.bulk_cox_layer.ui_layout_bulk_cox import BulkCoxPageUI
from script.analyzer_layer.bulk_layer.bulk_corre_layer.ui_layout_bulk_corre import BulkCorrePageUI
from script.analyzer_layer.bulk_layer.bulk_km_layer.ui_layout_bulk_km import BulkKmPageUI
from script.analyzer_layer.bulk_layer.bulk_km_layer.bulk_km_r_layer.ui_layout_bulk_km_r import BulkKmRPageUI
from script.analyzer_layer.bulk_layer.wgcna_layer.ui_layout_wgcna import WgcnaPageUI
from script.main_layer.settings_layer.ui_layout_settings import SettingsPageUI
from script.mods_layer.mod_manager import global_mod_manager

class MainWindowUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
    
    def initUI(self):
        styles = global_mod_manager.get_current_styles()
        
        self.setWindowTitle(styles.get('window_title', "小雪生信工具箱"))
        # 固定窗口大小为1920x1040，确保完整显示在1080P屏幕上（含标题栏）
        self.screen_width = 1920
        self.screen_height = 1000
        self.setFixedSize(self.screen_width, self.screen_height)
        self.move(0, 0)
        
        paths = global_mod_manager.get_current_paths()
        icon_path = os.path.join(paths['GUI_PATH'], "koyuki_machine.ico")
        if os.path.exists(icon_path):
            self.setWindowIcon(QIcon(icon_path))
        
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        
        self.stacked_widget = QStackedWidget()
        main_layout.addWidget(self.stacked_widget)
        
        self.create_home_page()
        self.create_analysis_page()
        self.create_violin_page()
        self.create_diff_page()
        self.create_bulk_page()
        self.create_bulk_cox_page()
        self.create_bulk_survival_page()
        self.create_bulk_km_page()
        self.create_bulk_km_r_page()
        self.create_wgcna_page()
        self.create_settings_page()
        
        self.stacked_widget.setCurrentWidget(self.home_page)
    
    def create_styled_button(self, text, parent=None, font_size=16, color_style='blue'):
        """
        创建主界面按钮 - 使用统一样式函数
        注意：粉色按钮(pink)是特殊样式，需要单独处理
        """
        # 粉色按钮特殊处理 - 使用突变色
        if color_style == 'pink':
            btn = QPushButton(text, parent)
            btn.setFont(QFont("幼圆", font_size, QFont.Bold))
            styles = global_mod_manager.get_current_styles()
            mutant_color = styles.get('main_mutant_color', styles.get('mutant_color', '#FF6B35'))
            btn.setStyleSheet(f"""
                QPushButton {{
                    color: {styles.get('main_text_color', '#FFB6C1')};
                    background: {styles.get('main_fill_color', 'rgba(233, 30, 99, 0.2)')};
                    border: 2px solid {mutant_color};
                    border-radius: 5px;
                    padding: 8px 20px;
                    min-width: 180px;
                    min-height: 60px;
                }}
                QPushButton:hover {{
                    background: {styles.get('main_hover_color', styles.get('main_fill_alt', 'rgba(233, 30, 99, 0.3)'))};
                }}
                QPushButton:pressed {{
                    background: {styles.get('main_active_color', 'rgba(233, 30, 99, 0.4)')};
                }}
            """)
            return btn
        
        # 普通按钮使用统一样式函数（variant='main'）
        return create_styled_button(
            text=text,
            parent=parent,
            font_size=font_size,
            variant='main'
        )
    
    def create_home_page(self):
        styles = global_mod_manager.get_current_styles()
        self.home_page = QWidget()
        self.home_page.setGeometry(0, 0, self.screen_width, self.screen_height)
        
        self.video_bg_label = QLabel(self.home_page)
        self.video_bg_label.setGeometry(0, 0, self.screen_width, self.screen_height)
        self.video_bg_label.setStyleSheet(f"background-color: {styles.get('main_fill_color', '#1a1a2e')};")
        self.video_bg_label.lower()
        
        # 使用新的主界面样式 key
        border_color = styles.get('main_border_color', '#1E3A5F')
        text_color = styles.get('main_text_color', '#87CEEB')
        fill_color = styles.get('main_fill_color', 'rgba(30, 58, 95, 0.3)')
        fill_alt = styles.get('main_fill_alt', 'rgba(30, 58, 95, 0.5)')
        gui_font = styles.get('main_gui_font', '幼圆')
        text_font = styles.get('main_text_font', '微软雅黑')
        combo_radius = '3px'
        button_radius = '5px'
        
        # 副标题样式
        subtitle_font = text_font
        subtitle_font_size = styles.get('subtitle_font_size', 14)
        subtitle_color = text_color
        subtitle_background = 'transparent'
        subtitle_bold = True
        
        mod_container = QWidget(self.home_page)
        mod_container.setGeometry(
            styles.get('mod_container_x', 15),
            styles.get('mod_container_y', 15),
            styles.get('mod_container_width', 250),
            styles.get('mod_container_height', 50)
        )
        mod_container.setStyleSheet(f"background: transparent;")
        
        self.mod_label = QLabel("模式选择:", mod_container)
        self.mod_label.setFont(QFont(text_font, styles.get('mod_label_font_size', 12), QFont.Bold))
        self.mod_label.setStyleSheet(f"color: {text_color}; background: transparent;")
        self.mod_label.move(0, 10)
        
        # 使用统一样式函数创建下拉框
        self.mod_combo = create_styled_combo_box(mod_container, variant='main')
        self.mod_combo.move(
            styles.get('mod_combo_x', 70),
            styles.get('mod_combo_y', 5)
        )
        self.mod_combo.setFixedSize(
            styles.get('mod_combo_width', 170),
            styles.get('mod_combo_height', 30)
        )
        
        available_mods = global_mod_manager.get_available_mods()
        self.mod_combo.addItems(available_mods)
        
        current_mod = global_mod_manager.get_current_mod()
        index = self.mod_combo.findText(current_mod.mod_name)
        if index >= 0:
            self.mod_combo.setCurrentIndex(index)
        
        music_container = QWidget(self.home_page)
        music_container.setGeometry(
            int(self.screen_width * styles.get('music_container_x', 0.9)),
            styles.get('music_container_y', 15),
            styles.get('music_container_width', 280),
            styles.get('music_container_height', 50)
        )
        
        # 使用统一样式函数创建音量滑块
        self.volume_slider = create_styled_slider(Qt.Horizontal, music_container, variant='main')
        self.volume_slider.setGeometry(
            styles.get('volume_slider_x', 5),
            styles.get('volume_slider_y', 25),
            styles.get('volume_slider_width', 100),
            styles.get('volume_slider_height', 25)
        )
        self.volume_slider.setRange(0, 100)
        self.volume_slider.setValue(100)
        
        self.music_btn = QPushButton(music_container)
        self.music_btn.setFixedSize(
            styles.get('music_button_width', 40),
            styles.get('music_button_height', 40)
        )
        self.music_btn.move(
            styles.get('music_button_x', 155),
            styles.get('music_button_y', 0)
        )
        paths = global_mod_manager.get_current_paths()
        if os.path.exists(paths['MUSIC_STOP_ICON']):
            self.music_btn.setIcon(QIcon(paths['MUSIC_STOP_ICON']))
        self.music_btn.setIconSize(QSize(32, 32))
        self.music_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {fill_color};
                border: 1px solid {border_color};
                border-radius: {button_radius};
            }}
            QPushButton:hover {{
                background-color: {fill_alt};
            }}
        """)
        
        # Settings按钮 - 独立widget，位于music_container正右方
        self.settings_btn = QPushButton(self.home_page)
        self.settings_btn.setFixedSize(
            styles.get('settings_button_width', 40),
            styles.get('settings_button_height', 40)
        )
        # 位置在music_container右侧，垂直位置与music_container相同
        container_x = int(self.screen_width * styles.get('music_container_x', 0.9))
        container_y = styles.get('music_container_y', 15)
        container_width = styles.get('music_container_width', 200)
        self.settings_btn.move(
            container_x + container_width + 5,
            container_y
        )
        settings_icon_path = os.path.join(paths['GUI_PATH'], "settings.ico")
        if os.path.exists(settings_icon_path):
            self.settings_btn.setIcon(QIcon(settings_icon_path))
        self.settings_btn.setIconSize(QSize(32, 32))
        self.settings_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {fill_color};
                border: 1px solid {border_color};
                border-radius: {button_radius};
            }}
            QPushButton:hover {{
                background-color: {fill_alt};
            }}
        """)
        
        self.title_label = QLabel(styles.get('main_title', "生信工具一览"), self.home_page)
        self.title_label.setFont(QFont(text_font, styles.get('title_font_size', 20), QFont.Bold))
        self.title_label.setStyleSheet(f"color: {styles.get('title_color', text_color)}; background: transparent;")
        self.title_label.setAlignment(Qt.AlignCenter)
        self.title_label.setGeometry(
            int(self.screen_width * styles.get('title_x', 0.65)),
            int(self.screen_height * styles.get('title_y', 0.18)),
            int(self.screen_width * styles.get('title_width', 0.3)),
            styles.get('title_height', 50)
        )
        
        self.left_title_label = QLabel(styles.get('single_cell_title', "单细胞分析"), self.home_page)
        self.left_title_label.setFont(QFont(subtitle_font, subtitle_font_size, QFont.Bold if subtitle_bold else QFont.Normal))
        self.left_title_label.setStyleSheet(f"color: {subtitle_color}; background: {subtitle_background};")
        self.left_title_label.setAlignment(Qt.AlignCenter)
        self.left_title_label.setGeometry(
            int(self.screen_width * styles.get('left_title_x', 0.68)),
            int(self.screen_height * styles.get('left_title_y', 0.28)),
            styles.get('left_title_width', 180),
            styles.get('left_title_height', 30)
        )
        
        self.right_title_label = QLabel(styles.get('bulk_title', "bulk分析"), self.home_page)
        self.right_title_label.setFont(QFont(subtitle_font, subtitle_font_size, QFont.Bold if subtitle_bold else QFont.Normal))
        self.right_title_label.setStyleSheet(f"color: {subtitle_color}; background: {subtitle_background};")
        self.right_title_label.setAlignment(Qt.AlignCenter)
        self.right_title_label.setGeometry(
            int(self.screen_width * styles.get('right_title_x', 0.78)),
            int(self.screen_height * styles.get('right_title_y', 0.28)),
            styles.get('right_title_width', 180),
            styles.get('right_title_height', 30)
        )
        
        btn_w = styles.get('button_width', 180)
        btn_h = styles.get('button_height', 60)
        btn_font_size = styles.get('button_font_size', 16)
        btn_start_x = int(self.screen_width * styles.get('button_start_x', 0.68))
        btn_start_y = int(self.screen_height * styles.get('button_start_y', 0.32))
        row_gap = int(self.screen_height * styles.get('button_row_gap', 0.08))
        
        self.btn_analysis = self.create_styled_button("初步分析", parent=self.home_page, font_size=btn_font_size)
        self.btn_analysis.move(btn_start_x, btn_start_y)
        
        self.btn_violin = self.create_styled_button("自定义小提琴图", parent=self.home_page, font_size=btn_font_size)
        self.btn_violin.move(btn_start_x, btn_start_y + row_gap)
        
        self.btn_bubble = self.create_styled_button("自定义气泡图", parent=self.home_page, font_size=btn_font_size)
        self.btn_bubble.move(btn_start_x, btn_start_y + row_gap * 2)
        
        self.btn_gene_bubble = self.create_styled_button("基因集气泡图", parent=self.home_page, font_size=btn_font_size)
        self.btn_gene_bubble.move(btn_start_x, btn_start_y + row_gap * 3)
        
        self.btn_diff = self.create_styled_button("差异分析", parent=self.home_page, font_size=btn_font_size)
        self.btn_diff.move(btn_start_x, btn_start_y + row_gap * 4)
        
        right_start_x = int(self.screen_width * styles.get('right_title_x', 0.78))
        self.btn_bulk = self.create_styled_button("bulk表达量分析", parent=self.home_page, font_size=btn_font_size)
        self.btn_bulk.move(right_start_x, btn_start_y)

        self.btn_bulk_cox = self.create_styled_button("bulk Cox分析", parent=self.home_page, font_size=btn_font_size)
        self.btn_bulk_cox.move(right_start_x, btn_start_y + row_gap)
        
        self.btn_bulk_km = self.create_styled_button("bulk KM曲线", parent=self.home_page, font_size=btn_font_size)
        self.btn_bulk_km.move(right_start_x, btn_start_y + row_gap * 2)
        
        self.btn_bulk_survival = self.create_styled_button("bulk相关性分析", parent=self.home_page, font_size=btn_font_size)
        self.btn_bulk_survival.move(right_start_x, btn_start_y + row_gap * 3)
        
        self.btn_bulk_wgcna = self.create_styled_button("bulk WGCNA", parent=self.home_page, font_size=btn_font_size)
        self.btn_bulk_wgcna.move(right_start_x, btn_start_y + row_gap * 4)
        
        tools_start_x = int(self.screen_width * styles.get('tools_title_x', 0.88))
        self.tools_title_label = QLabel(styles.get('tools_title', "通用小工具"), self.home_page)
        self.tools_title_label.setFont(QFont(subtitle_font, subtitle_font_size, QFont.Bold if subtitle_bold else QFont.Normal))
        self.tools_title_label.setStyleSheet(f"color: {subtitle_color}; background: {subtitle_background};")
        self.tools_title_label.setAlignment(Qt.AlignCenter)
        self.tools_title_label.setGeometry(
            tools_start_x,
            int(self.screen_height * styles.get('tools_title_y', 0.28)),
            styles.get('tools_title_width', 180),
            styles.get('tools_title_height', 30)
        )
        
        self.btn_venn = self.create_styled_button("韦恩图交集", parent=self.home_page, font_size=btn_font_size)
        self.btn_venn.move(tools_start_x, btn_start_y)
        
        self.btn_donate = QPushButton("打赏作者", self.home_page)
        self.btn_donate.setFont(QFont(styles.get('label_font', "微软雅黑"), 14, QFont.Bold))
        donate_color = styles.get('main_mutant_color', styles.get('mutant_color', '#FF6B35'))
        btn_radius = styles.get('button_border_radius', '5px')
        self.btn_donate.setStyleSheet(f"""
            QPushButton {{
                color: white;
                background: {donate_color};
                border: 3px solid {donate_color};
                border-radius: {btn_radius};
                min-width: 150px;
                min-height: 40px;
            }}
            QPushButton:hover {{
                background: {styles.get('main_hover_color', '#D62839')};
            }}
        """)
        self.btn_donate.move(
            int(self.screen_width * styles.get('donate_button_x', 0.725)),
            int(self.screen_height * styles.get('donate_button_y', 0.80))
        )
        
        self.stacked_widget.addWidget(self.home_page)
    
    def create_analysis_page(self):
        self.analysis_ui = InitialAnalysisPageUI(self, self.screen_width, self.screen_height)
        self.initial_analysis_page = self.analysis_ui.analysis_page
        
        self.stacked_widget.addWidget(self.initial_analysis_page)
    
    def create_violin_page(self):
        self.violin_ui = ViolinPageUI(self, self.screen_width, self.screen_height)
        self.violin_page = self.violin_ui.violin_page
        
        self.stacked_widget.addWidget(self.violin_page)
    
    def create_diff_page(self):
        self.diff_ui = DiffPageUI(self, self.screen_width, self.screen_height)
        self.diff_page = self.diff_ui.diff_page
        
        self.stacked_widget.addWidget(self.diff_page)
    
    def create_bulk_page(self):
        self.bulk_ui = BulkExprPageUI(self, self.screen_width, self.screen_height)
        self.bulk_page = self.bulk_ui.bulk_expr_page
        
        self.stacked_widget.addWidget(self.bulk_page)
    
    def create_bulk_cox_page(self):
        self.bulk_cox_ui = BulkCoxPageUI(self, self.screen_width, self.screen_height)
        self.bulk_cox_page = self.bulk_cox_ui.bulk_cox_page
        
        self.stacked_widget.addWidget(self.bulk_cox_page)

    def create_bulk_survival_page(self):
        self.bulk_corre_ui = BulkCorrePageUI(self, self.screen_width, self.screen_height)
        self.bulk_corre_page = self.bulk_corre_ui.bulk_corre_page
        
        self.stacked_widget.addWidget(self.bulk_corre_page)

    def create_bulk_km_page(self):
        self.bulk_km_ui = BulkKmPageUI(self, self.screen_width, self.screen_height)
        self.bulk_km_page = self.bulk_km_ui.bulk_km_page
        
        self.stacked_widget.addWidget(self.bulk_km_page)

    def create_bulk_km_r_page(self):
        self.bulk_km_r_ui = BulkKmRPageUI(self, self.screen_width, self.screen_height)
        self.bulk_km_r_page = self.bulk_km_r_ui.bulk_km_r_page
        
        self.stacked_widget.addWidget(self.bulk_km_r_page)

    def create_wgcna_page(self):
        self.wgcna_ui = WgcnaPageUI(self, self.screen_width, self.screen_height)
        self.wgcna_page = self.wgcna_ui.wgcna_page
        
        self.stacked_widget.addWidget(self.wgcna_page)

    def create_settings_page(self):
        self.settings_ui = SettingsPageUI(self, self.screen_width, self.screen_height)
        self.settings_page = self.settings_ui.settings_page
        
        self.stacked_widget.addWidget(self.settings_page)

    def go_to_home_page(self):
        """返回主页"""
        if hasattr(self, 'home_page') and self.home_page:
            self.stacked_widget.setCurrentWidget(self.home_page)