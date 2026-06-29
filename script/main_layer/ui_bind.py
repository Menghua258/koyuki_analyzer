# -*- coding: utf-8 -*-
"""
主界面功能绑定脚本 - 全权负责粘合内外
只包含主界面相关的功能绑定（视频播放、页面导航、打赏等）
音乐控制完全由模组的MusicController处理
支持动态切换模组，从模组管理器获取当前模组的资源和功能
"""

from script.utils_layer.import_config import *
from script.main_layer import MainWindowUI
from script.main_layer.ui_func_main import MainFunc
from script.analyzer_layer.scRNAseq_layer.initial_analysis_layer.ui_bind_initial_analysis import InitialAnalysisBind
from script.analyzer_layer.scRNAseq_layer.violin_layer.ui_bind_violin import ViolinBind
from script.analyzer_layer.scRNAseq_layer.diff_layer.ui_bind_diff import DiffBind
from script.analyzer_layer.bulk_layer.bulk_expr_layer.ui_bind_bulk_expr import BulkExprBind
from script.analyzer_layer.bulk_layer.bulk_cox_layer.ui_bind_bulk_cox import BulkCoxBind
from script.analyzer_layer.bulk_layer.bulk_corre_layer.ui_bind_bulk_corre import BulkCorreBind
from script.analyzer_layer.bulk_layer.bulk_km_layer.ui_bind_bulk_km import BulkKmBind
from script.analyzer_layer.bulk_layer.bulk_km_layer.bulk_km_r_layer.ui_bind_bulk_km_r import BulkKmRBind
from script.analyzer_layer.bulk_layer.wgcna_layer.ui_bind_wgcna import WgcnaBind
from script.main_layer.settings_layer.ui_bind_settings import SettingsBind
from script.mods_layer.mod_manager import global_mod_manager
from script.mods_layer.emoji_function_for_mods import happy, attention, wrong
from script.utils_layer.music_controller_fix import (
    sync_all_volume_sliders,
    get_all_music_controllers,
    update_music_button_icon,
    validate_music_controller_state,
    sync_all_music_buttons,
    fix_music_controller_bindings
)


# ========================================
# 主窗口功能绑定类
# ========================================
class MainWindowBind(MainWindowUI):
    """主窗口功能绑定类 - 负责绑定主界面GUI控件与功能"""

    def __init__(self):
        super().__init__()
        self.func = MainFunc(self)
        self.init_bindings()
        self.init_variables()

    def init_bindings(self):
        """初始化所有绑定"""
        self.bind_mod_selection()
        self.bind_page_navigation()
        self.bind_general_tools()

        # 初始化音量：确保pygame音量与主界面滑块一致
        mod_instance = global_mod_manager.get_current_mod()
        if hasattr(mod_instance, 'global_music_player') and hasattr(self, 'volume_slider'):
            initial_volume = self.volume_slider.value()
            mod_instance.global_music_player.set_volume(initial_volume / 100.0)

        mod_instance = global_mod_manager.get_current_mod()
        ClickFilterClass = mod_instance.get_click_filter_class()
        self.click_filter = ClickFilterClass(mod_instance.global_sound_player)
        self.installEventFilter(self.click_filter)
        self._install_click_filter_recursively(self)

    def _install_click_filter_recursively(self, widget):
        """递归安装点击音效过滤器到所有子控件"""
        try:
            if widget and hasattr(widget, 'installEventFilter'):
                widget.installEventFilter(self.click_filter)
            if hasattr(widget, 'children'):
                for child in widget.children():
                    self._install_click_filter_recursively(child)
        except Exception as e:
            print(f"安装点击音效过滤器失败: {e}")

    def init_variables(self):
        """初始化变量"""
        paths = global_mod_manager.get_current_paths()
        VideoBackgroundClass = global_mod_manager.get_current_mod().get_video_background_class()
        self.video_bg = VideoBackgroundClass(
            self.home_page,
            self.screen_width,
            self.screen_height,
            startup_video=paths['STARTUP_VIDEO'],
            return_video=paths['STARTUP_RETURN_VIDEO'],
            remain_video=paths['STARTREMAIN_VIDEO']
        )

        QTimer.singleShot(100, self.init_video_background)

    def bind_mod_selection(self):
        """绑定模组选择"""
        if hasattr(self, 'mod_combo'):
            self.mod_combo.currentTextChanged.connect(self.switch_mod)

    def switch_mod(self, mod_name):
        """切换模组"""
        try:
            # 保存当前音乐播放状态
            old_mod_instance = global_mod_manager.get_current_mod()
            old_music_playing = False
            old_music_volume = 1.0
            if hasattr(old_mod_instance, 'global_music_player'):
                old_music_playing = old_mod_instance.global_music_player.is_playing
                old_music_volume = old_mod_instance.global_music_player.get_volume()

            if global_mod_manager.set_current_mod(mod_name):
                print(f"已切换到模组: {mod_name}")
                self.reload_mod_resources(old_music_playing, old_music_volume)
            else:
                print(f"切换模组失败: {mod_name}")
        except Exception as e:
            print(f"切换模组异常: {e}")

    def reload_mod_resources(self, old_music_playing=False, old_music_volume=1.0):
        """重新加载模组资源 - 业务编排：调用func更新UI + 处理音乐业务"""
        try:
            new_paths = global_mod_manager.get_current_paths()

            # 1. 应用UI样式（委托给func层）
            self.func.apply_mod_styles()

            # 2. 重新加载视频背景（委托给func层）
            self.func.reload_video_background()

            # 3. 更新子界面样式（委托给func层）
            self.func.update_subpage_styles()

            # 4. 更新音效资源和点击过滤器（业务层）
            mod_instance = global_mod_manager.get_current_mod()
            if hasattr(mod_instance, 'global_sound_player'):
                click_sound = new_paths.get('UI_CLICK_SOUND')
                if os.path.exists(click_sound):
                    mod_instance.global_sound_player.load_sound(click_sound, "click")

                # 重新创建点击过滤器
                ClickFilterClass = mod_instance.get_click_filter_class()
                self.click_filter = ClickFilterClass(mod_instance.global_sound_player)
                self.installEventFilter(self.click_filter)
                self._install_click_filter_recursively(self)

            # 5. 音乐播放状态恢复（业务层）
            if hasattr(mod_instance, 'global_music_player'):
                # 先停止当前播放的音乐，避免切换时播放一小下
                pygame.mixer.music.stop()

                # 加载新模组的音乐资源但不自动播放
                mod_instance.on_load(auto_play=False)

                # 再次确保停止播放（防止load_music内部触发播放）
                pygame.mixer.music.stop()

                # 恢复之前的音乐播放状态
                if old_music_playing:
                    mod_instance.global_music_player.play()
                    self.func.update_music_icon(True)
                else:
                    mod_instance.global_music_player.stop()
                    self.func.update_music_icon(False)

                # 恢复之前的音量
                mod_instance.global_music_player.set_volume(old_music_volume)

            print("模组资源重新加载完成")
        except Exception as e:
            print(f"重新加载模组资源失败: {e}")

    def bind_page_navigation(self):
        """绑定页面导航"""
        if hasattr(self, 'btn_analysis'):
            self.btn_analysis.clicked.connect(self.go_to_analysis_page)
        if hasattr(self, 'btn_violin'):
            self.btn_violin.clicked.connect(self.go_to_violin_page)
        if hasattr(self, 'btn_bubble'):
            self.btn_bubble.clicked.connect(self.go_to_bubble_page)
        if hasattr(self, 'btn_gene_bubble'):
            self.btn_gene_bubble.clicked.connect(self.go_to_gene_bubble_page)
        if hasattr(self, 'btn_diff'):
            self.btn_diff.clicked.connect(self.go_to_diff_page)

        if hasattr(self, 'btn_bulk'):
            self.btn_bulk.clicked.connect(self.go_to_bulk_page)
        if hasattr(self, 'btn_bulk_cox'):
            self.btn_bulk_cox.clicked.connect(self.go_to_bulk_cox_page)
        if hasattr(self, 'btn_bulk_km'):
            self.btn_bulk_km.clicked.connect(self.go_to_bulk_km_page)
        if hasattr(self, 'btn_bulk_survival'):
            self.btn_bulk_survival.clicked.connect(self.go_to_bulk_survival_page)
        if hasattr(self, 'btn_bulk_wgcna'):
            self.btn_bulk_wgcna.clicked.connect(self.go_to_bulk_wgcna_page)

        if hasattr(self, 'btn_venn'):
            self.btn_venn.clicked.connect(self.go_to_venn_page)

        if hasattr(self, 'settings_btn'):
            self.settings_btn.clicked.connect(self.go_to_settings_page)

    def bind_general_tools(self):
        """绑定通用工具"""
        if hasattr(self, 'btn_donate'):
            self.btn_donate.clicked.connect(self.show_donate_message)

        self.bind_music_controls()

    def bind_music_controls(self):
        """绑定音乐控制"""
        if hasattr(self, 'music_btn'):
            self.music_btn.clicked.connect(self.toggle_music)

        if hasattr(self, 'volume_slider'):
            self.volume_slider.valueChanged.connect(self.set_volume)

    def toggle_music(self):
        """切换音乐播放状态"""
        mod_instance = global_mod_manager.get_current_mod()
        if hasattr(mod_instance, 'global_music_player'):
            is_playing = mod_instance.global_music_player.toggle()
            # 同步所有音乐按钮的图标状态（委托给func层）
            self.func.update_music_icon(is_playing)

    def set_volume(self, value):
        """设置音量"""
        mod_instance = global_mod_manager.get_current_mod()
        if hasattr(mod_instance, 'global_music_player'):
            mod_instance.global_music_player.set_volume(value / 100.0)

        # 更新子界面的音量滑块（委托给func层）
        self.func.sync_volume_sliders(value)

    # 从子界面同步音量滑块的外部接口
    _sync_all_volume_sliders_from_subinterface = lambda self, value: self.func.sync_volume_sliders(value)

    # ========================================
    # 视频背景相关方法
    # ========================================
    def init_video_background(self):
        """初始化视频背景"""
        self.video_bg.set_label(self.video_bg_label)
        self.video_bg.play()

    # ========================================
    # 页面导航方法
    # ========================================
    def go_to_home_page(self):
        """返回主页"""
        try:
            if hasattr(self, 'home_page') and self.home_page:
                self.stacked_widget.setCurrentWidget(self.home_page)
                if hasattr(self, 'video_bg'):
                    self.video_bg.play_return()
        except Exception as e:
            print(f"返回主页失败: {e}")

    def go_to_analysis_page(self):
        """跳转到初步分析页面"""
        try:
            if hasattr(self, 'initial_analysis_page') and self.initial_analysis_page:
                self.stacked_widget.setCurrentWidget(self.initial_analysis_page)

                if hasattr(self.analysis_ui, 'btn_back_analysis'):
                    self.analysis_ui.btn_back_analysis.clicked.connect(self.go_to_home_page)

                if not hasattr(self, 'analysis_bind'):
                    self.analysis_bind = InitialAnalysisBind(self, self.analysis_ui)
        except Exception as e:
            print(f"跳转到初步分析页面失败: {e}")
            attention(self, "初步分析功能正在开发中...")

    def go_to_violin_page(self):
        """跳转到自定义小提琴图页面"""
        try:
            if hasattr(self, 'violin_page') and self.violin_page:
                self.stacked_widget.setCurrentWidget(self.violin_page)

                if hasattr(self.violin_ui, 'btn_back_violin'):
                    self.violin_ui.btn_back_violin.clicked.connect(self.go_to_home_page)

                if not hasattr(self, 'violin_bind'):
                    self.violin_bind = ViolinBind(self, self.violin_ui)

                if hasattr(self, 'analysis_bind') and hasattr(self.analysis_bind, 'analysis'):
                    if self.analysis_bind.analysis.adata is not None:
                        self.violin_bind.set_adata(self.analysis_bind.analysis.adata)
                    if self.analysis_bind.analysis.dataset_output_dir is not None:
                        self.violin_bind.set_dataset_output_dir(self.analysis_bind.analysis.dataset_output_dir)
        except Exception as e:
            print(f"跳转到小提琴图页面失败: {e}")
            attention(self, "自定义小提琴图功能正在开发中...")

    def go_to_bubble_page(self):
        """跳转到自定义气泡图页面"""
        attention(self, "自定义气泡图功能正在开发中...")

    def go_to_gene_bubble_page(self):
        """跳转到基因集气泡图页面"""
        attention(self, "基因集气泡图功能正在开发中...")

    def go_to_diff_page(self):
        """跳转到差异分析页面"""
        try:
            if hasattr(self, 'diff_page') and self.diff_page:
                self.stacked_widget.setCurrentWidget(self.diff_page)

                if hasattr(self.diff_ui, 'btn_back_diff'):
                    self.diff_ui.btn_back_diff.clicked.connect(self.go_to_home_page)

                if not hasattr(self, 'diff_bind'):
                    self.diff_bind = DiffBind(self, self.diff_ui)

                if hasattr(self, 'analysis_bind') and hasattr(self.analysis_bind, 'analysis'):
                    if self.analysis_bind.analysis.adata is not None:
                        self.diff_bind.set_adata(self.analysis_bind.analysis.adata)
                        self.diff_bind.load_groups()  # 加载分组列表
                    if self.analysis_bind.analysis.dataset_output_dir is not None:
                        self.diff_bind.set_dataset_output_dir(self.analysis_bind.analysis.dataset_output_dir)
        except Exception as e:
            print(f"跳转到差异分析页面失败: {e}")
            attention(self, "差异分析功能正在开发中...")

    def go_to_bulk_page(self):
        """跳转到bulk表达量分析页面"""
        try:
            if hasattr(self, 'bulk_page') and self.bulk_page:
                self.stacked_widget.setCurrentWidget(self.bulk_page)

                if not hasattr(self, 'bulk_bind'):
                    self.bulk_bind = BulkExprBind(self, self.bulk_ui)

                if hasattr(self.bulk_ui, 'btn_back_bulk_expr') and not hasattr(self, '_bulk_back_bound'):
                    self.bulk_ui.btn_back_bulk_expr.clicked.connect(self.go_to_home_page)
                    self._bulk_back_bound = True
        except Exception as e:
            print(f"跳转到bulk表达量分析页面失败: {e}")

    def go_to_bulk_cox_page(self):
        """跳转到bulk Cox分析页面"""
        try:
            if hasattr(self, 'bulk_cox_page') and self.bulk_cox_page:
                self.stacked_widget.setCurrentWidget(self.bulk_cox_page)

                if not hasattr(self, 'bulk_cox_bind'):
                    self.bulk_cox_bind = BulkCoxBind(self, self.bulk_cox_ui)

                if hasattr(self.bulk_cox_ui, 'btn_back_bulk_cox') and not hasattr(self, '_bulk_cox_back_bound'):
                    self.bulk_cox_ui.btn_back_bulk_cox.clicked.connect(self.go_to_home_page)
                    self._bulk_cox_back_bound = True
        except Exception as e:
            print(f"跳转到bulk Cox分析页面失败: {e}")

    def go_to_bulk_km_page(self):
        """跳转到bulk KM曲线页面"""
        try:
            if hasattr(self, 'bulk_km_page') and self.bulk_km_page:
                self.stacked_widget.setCurrentWidget(self.bulk_km_page)

                if not hasattr(self, 'bulk_km_bind'):
                    self.bulk_km_bind = BulkKmBind(self, self.bulk_km_ui)

                if hasattr(self.bulk_km_ui, 'btn_back_bulk_km') and not hasattr(self, '_bulk_km_back_bound'):
                    self.bulk_km_ui.btn_back_bulk_km.clicked.connect(self.go_to_home_page)
                    self._bulk_km_back_bound = True
        except Exception as e:
            print(f"跳转到bulk KM曲线页面失败: {e}")

    def go_to_km_r_page(self):
        """跳转到bulk KM曲线R模式页面"""
        try:
            if not hasattr(self, 'bulk_km_r_page'):
                self.create_bulk_km_r_page()

            if hasattr(self, 'bulk_km_r_page') and self.bulk_km_r_page:
                self.stacked_widget.setCurrentWidget(self.bulk_km_r_page)

                if not hasattr(self, 'bulk_km_r_bind'):
                    self.bulk_km_r_bind = BulkKmRBind(self, self.bulk_km_r_ui)

                # 每次进入都同步数据（确保数据是最新的）
                self.bulk_km_r_bind.sync_data_from_km()

                if hasattr(self.bulk_km_r_ui, 'btn_back') and not hasattr(self, '_bulk_km_r_back_bound'):
                    self.bulk_km_r_ui.btn_back.clicked.connect(self.go_to_bulk_km_page)
                    self._bulk_km_r_back_bound = True
        except Exception as e:
            print(f"跳转到bulk KM曲线R模式页面失败: {e}")

    def go_to_bulk_survival_page(self):
        """跳转到bulk相关性分析页面"""
        try:
            if hasattr(self, 'bulk_corre_page') and self.bulk_corre_page:
                self.stacked_widget.setCurrentWidget(self.bulk_corre_page)

                if not hasattr(self, 'bulk_corre_bind'):
                    self.bulk_corre_bind = BulkCorreBind(self, self.bulk_corre_ui)

                if hasattr(self.bulk_corre_ui, 'btn_back_bulk_corre') and not hasattr(self, '_bulk_survival_back_bound'):
                    self.bulk_corre_ui.btn_back_bulk_corre.clicked.connect(self.go_to_home_page)
                    self._bulk_survival_back_bound = True
        except Exception as e:
            print(f"跳转到bulk相关性分析页面失败: {e}")

    def go_to_bulk_wgcna_page(self):
        """跳转到bulk WGCNA页面"""
        try:
            if hasattr(self, 'wgcna_page') and self.wgcna_page:
                self.stacked_widget.setCurrentWidget(self.wgcna_page)

                if not hasattr(self, 'wgcna_bind'):
                    self.wgcna_bind = WgcnaBind(self, self.wgcna_ui)

                if hasattr(self.wgcna_ui, 'btn_back_wgcna') and not hasattr(self, '_wgcna_back_bound'):
                    self.wgcna_ui.btn_back_wgcna.clicked.connect(self.go_to_home_page)
                    self._wgcna_back_bound = True
        except Exception as e:
            print(f"跳转到bulk WGCNA页面失败: {e}")

    def go_to_venn_page(self):
        """跳转到韦恩图交集页面"""
        attention(self, "韦恩图交集功能正在开发中...")

    def go_to_settings_page(self):
        """跳转到Settings页面"""
        try:
            if not hasattr(self, 'settings_page'):
                self.create_settings_page()

            if hasattr(self, 'settings_page') and self.settings_page:
                self.stacked_widget.setCurrentWidget(self.settings_page)

                if not hasattr(self, 'settings_bind'):
                    self.settings_bind = SettingsBind(self, self.settings_ui)
        except Exception as e:
            print(f"跳转到Settings页面失败: {e}")

    # ========================================
    # 通用工具方法
    # ========================================
    def show_donate_message(self):
        """显示打赏信息（委托给func层）"""
        self.func.show_donate_message()
