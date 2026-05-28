import sys
import os

from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QTabWidget,
    QToolBar,
    QPushButton,
    QLineEdit,
    QDockWidget,
    QListWidget,
    QListWidgetItem,
    QLabel,
    QVBoxLayout,
    QHBoxLayout,
    QSplitter,
)

from PyQt6.QtWebEngineWidgets import (
    QWebEngineView,
)

from PyQt6.QtWebEngineCore import (
    QWebEnginePage,
    QWebEngineProfile,
)

from PyQt6.QtCore import (
    QUrl,
    Qt,
)

from PyQt6.QtGui import (
    QKeySequence,
    QShortcut,
)


# -----------------------------------
# Safe Browser Page
# -----------------------------------
class BrowserPage(QWebEnginePage):
    def __init__(self, controller, parent=None):
        super().__init__(parent)
        self.controller = controller

    def createWindow(self, _type):
        # Prevent popup tabs/windows
        return None


# -----------------------------------
# Browser Tab
# -----------------------------------
class Tab:
    def __init__(
        self,
        controller,
        url="https://google.com"
    ):
        self.controller = controller

        # Container
        self.container = QWidget()

        self.layout = QVBoxLayout(
            self.container
        )

        self.layout.setContentsMargins(
            0, 0, 0, 0
        )

        # Splitter
        self.splitter = QSplitter(
            Qt.Orientation.Vertical
        )

        self.layout.addWidget(
            self.splitter
        )

        # Main browser view
        self.view = QWebEngineView()

        self.page = BrowserPage(
            controller,
            self.view
        )

        self.view.setPage(self.page)

        self.view.setUrl(QUrl(url))

        self.splitter.addWidget(
            self.view
        )

        # DevTools
        self.devtools_view = QWebEngineView()

        self.devtools_page = QWebEnginePage(
            QWebEngineProfile.defaultProfile(),
            self.devtools_view
        )

        self.devtools_view.setPage(
            self.devtools_page
        )

        self.page.setDevToolsPage(
            self.devtools_page
        )

        self.devtools_view.hide()

        self.splitter.addWidget(
            self.devtools_view
        )

        self.splitter.setSizes(
            [700, 0]
        )

        self.devtools_visible = False

    # Toggle DevTools
    def toggle_devtools(self):

        if self.devtools_visible:

            self.devtools_view.hide()

            self.splitter.setSizes(
                [1, 0]
            )

            self.devtools_visible = False

        else:

            self.devtools_view.show()

            self.splitter.setSizes(
                [500, 300]
            )

            self.devtools_visible = True


# -----------------------------------
# Main Browser
# -----------------------------------
class SnowyBrowser(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle(
            "SnowyBrowser"
        )

        self.resize(1400, 900)

        self.tabs = []

        self.active_tab = None

        self.download_items = {}

        self.build_ui()

        self.setup_download_manager()

        # Start with ONE tab
        self.create_new_tab()

    # -----------------------------------
    # UI
    # -----------------------------------
    def build_ui(self):

        self.starting_up = True

        self.tab_widget = QTabWidget()

        self.tab_widget.setTabsClosable(
            True
        )

        self.tab_widget.tabCloseRequested.connect(
            self.close_tab
        )

        self.tab_widget.currentChanged.connect(
            self.on_tab_changed
        )

        self.setCentralWidget(
            self.tab_widget
        )

        # Toolbar
        toolbar = QToolBar()

        self.addToolBar(toolbar)

        self.back_btn = QPushButton("←")

        self.forward_btn = QPushButton("→")

        self.reload_btn = QPushButton("⟳")

        self.downloads_btn = QPushButton(
            "↓"
        )

        self.devtools_btn = QPushButton(
            "🛠"
        )

        self.url_bar = QLineEdit()

        toolbar.addWidget(
            self.back_btn
        )

        toolbar.addWidget(
            self.forward_btn
        )

        toolbar.addWidget(
            self.reload_btn
        )

        toolbar.addWidget(
            self.downloads_btn
        )

        toolbar.addWidget(
            self.devtools_btn
        )

        toolbar.addWidget(
            self.url_bar
        )

        # Toolbar actions
        self.back_btn.clicked.connect(
            self.go_back
        )

        self.forward_btn.clicked.connect(
            self.go_forward
        )

        self.reload_btn.clicked.connect(
            self.reload_page
        )

        self.downloads_btn.clicked.connect(
            self.toggle_downloads
        )

        self.devtools_btn.clicked.connect(
            self.toggle_devtools
        )

        self.url_bar.returnPressed.connect(
            self.navigate
        )

        # "+" Tab
        self.plus_widget = QWidget()

        plus_index = self.tab_widget.addTab(
            self.plus_widget,
            "+"
        )

        # Hide close button
        self.tab_widget.tabBar().setTabButton(
            plus_index,
            self.tab_widget.tabBar().ButtonPosition.RightSide,
            None
        )

        # F12 DevTools shortcut
        self.devtools_shortcut = QShortcut(
            QKeySequence("F12"),
            self
        )

        self.devtools_shortcut.activated.connect(
            self.toggle_devtools
        )

        self.starting_up = False

    # -----------------------------------
    # DevTools
    # -----------------------------------
    def toggle_devtools(self):

        if not self.active_tab:
            return

        self.active_tab.toggle_devtools()

    # -----------------------------------
    # Downloads
    # -----------------------------------
    def setup_download_manager(self):

        self.download_dock = QDockWidget(
            "Downloads",
            self
        )

        self.download_list = QListWidget()

        self.download_dock.setWidget(
            self.download_list
        )

        self.addDockWidget(
            Qt.DockWidgetArea.BottomDockWidgetArea,
            self.download_dock
        )

        self.download_dock.hide()

        profile = (
            QWebEngineProfile.defaultProfile()
        )

        profile.downloadRequested.connect(
            self.handle_download
        )

    def toggle_downloads(self):

        if self.download_dock.isVisible():

            self.download_dock.hide()

        else:

            self.download_dock.show()

    def handle_download(self, download):

        downloads_path = os.path.join(
            os.path.expanduser("~"),
            "Downloads"
        )

        filename = (
            download.downloadFileName()
        )

        save_path = os.path.join(
            downloads_path,
            filename
        )

        download.setDownloadDirectory(
            downloads_path
        )

        download.setDownloadFileName(
            filename
        )

        # -----------------------------------
        # Download Widget
        # -----------------------------------
        item_widget = QWidget()

        layout = QHBoxLayout(item_widget)

        layout.setContentsMargins(
            5, 2, 5, 2
        )

        label = QLabel(
            f"{filename} - 0%"
        )

        cancel_btn = QPushButton(
            "Cancel"
        )

        layout.addWidget(label)

        layout.addStretch()

        layout.addWidget(cancel_btn)

        # -----------------------------------
        # List Item
        # -----------------------------------
        item = QListWidgetItem()

        self.download_list.addItem(item)

        self.download_list.setItemWidget(
            item,
            item_widget
        )

        item.setSizeHint(
            item_widget.sizeHint()
        )

        # -----------------------------------
        # Metadata
        # -----------------------------------
        self.download_items[download] = {
            "path": save_path,
            "status": "downloading",
            "label": label,
            "button": cancel_btn,
            "item": item,
        }

        # Cancel button
        cancel_btn.clicked.connect(
            lambda:
            self.cancel_download(download)
        )

        # Progress updates
        download.receivedBytesChanged.connect(
            lambda d=download:
            self.update_download_progress(d)
        )

        # Finish updates
        download.isFinishedChanged.connect(
            lambda d=download:
            self.finish_download(d)
        )

        download.accept()

        self.download_dock.show()

    def cancel_download(self, download):

        if download not in self.download_items:
            return

        data = self.download_items[
            download
        ]

        if data["status"] != "downloading":
            return

        download.cancel()

        data["status"] = "cancelled"

        data["label"].setText(
            "✕ Cancelled"
        )

        data["button"].hide()

    def update_download_progress(
        self,
        download
    ):

        if download not in self.download_items:
            return

        data = self.download_items[
            download
        ]

        received = (
            download.receivedBytes()
        )

        total = (
            download.totalBytes()
        )

        filename = (
            download.downloadFileName()
        )

        if total > 0:

            percent = int(
                (received / total) * 100
            )

        else:

            percent = 0

        data["label"].setText(
            f"{filename} - {percent}%"
        )

    def finish_download(
        self,
        download
    ):

        if download not in self.download_items:
            return

        data = self.download_items[
            download
        ]

        filename = (
            download.downloadFileName()
        )

        state_name = (
            download.state().name
        )

        if state_name == "DownloadCompleted":

            data["status"] = "finished"

            data["label"].setText(
                f"✓ {filename}"
            )

            data["button"].setText(
                "Open"
            )

            data["button"].show()

            data["button"].clicked.disconnect()

            data["button"].clicked.connect(
                lambda:
                self.open_download(download)
            )

        elif state_name == "DownloadCancelled":

            data["status"] = "cancelled"

            data["label"].setText(
                f"✕ {filename}"
            )

            data["button"].hide()

    def open_download(self, download):

        if download not in self.download_items:
            return

        path = self.download_items[
            download
        ]["path"]

        if not os.path.exists(path):
            return

        if sys.platform.startswith(
            "linux"
        ):

            os.system(
                f'xdg-open "{path}"'
            )

        elif sys.platform == "darwin":

            os.system(
                f'open "{path}"'
            )

        elif sys.platform == "win32":

            os.startfile(path)

    # -----------------------------------
    # Create New Tab
    # -----------------------------------
    def create_new_tab(
        self,
        url="https://google.com"
    ):

        tab = Tab(self, url)

        self.tabs.append(tab)

        insert_index = (
            self.tab_widget.count() - 1
        )

        self.tab_widget.insertTab(
            insert_index,
            tab.container,
            "New Tab"
        )

        self.tab_widget.setCurrentWidget(
            tab.container
        )

        self.active_tab = tab

        # URL sync
        tab.view.urlChanged.connect(
            lambda qurl, t=tab:
            self.sync_url(qurl, t)
        )

        # Dynamic title
        tab.view.titleChanged.connect(
            lambda title, t=tab:
            self.update_tab_title(
                t,
                title
            )
        )

        return tab

    # -----------------------------------
    # Get Tab
    # -----------------------------------
    def get_tab(self, widget):

        for tab in self.tabs:

            if tab.container == widget:
                return tab

        return None

    # -----------------------------------
    # Tab Changed
    # -----------------------------------
    def on_tab_changed(self, index):

        if self.starting_up:
            return

        widget = self.tab_widget.widget(
            index
        )

        # "+" clicked
        if widget == self.plus_widget:

            self.create_new_tab()

            return

        tab = self.get_tab(widget)

        if tab:

            self.active_tab = tab

            self.url_bar.setText(
                tab.view.url().toString()
            )

    # -----------------------------------
    # Close Tab
    # -----------------------------------
    def close_tab(self, index):

        widget = self.tab_widget.widget(
            index
        )

        # Never close "+"
        if widget == self.plus_widget:
            return

        tab = self.get_tab(widget)

        if not tab:
            return

        # Jump before close
        current_index = (
            self.tab_widget.currentIndex()
        )

        if current_index == index:

            target_index = index - 1

            if target_index < 0:
                target_index = 1

            if (
                self.tab_widget.widget(
                    target_index
                ) == self.plus_widget
            ):
                target_index = 0

            target_widget = (
                self.tab_widget.widget(
                    target_index
                )
            )

            target_tab = self.get_tab(
                target_widget
            )

            if target_tab:

                self.active_tab = target_tab

                self.tab_widget.setCurrentWidget(
                    target_tab.container
                )

                self.url_bar.setText(
                    target_tab.view.url().toString()
                )

        # Remove old tab
        self.tabs.remove(tab)

        self.tab_widget.removeTab(index)

        tab.container.deleteLater()

        # Always keep one tab
        if len(self.tabs) == 0:

            self.create_new_tab(
                "about:blank"
            )

    # -----------------------------------
    # Navigation
    # -----------------------------------
    def navigate(self):

        if not self.active_tab:
            return

        url = self.url_bar.text().strip()

        if not url.startswith((
            "http://",
            "https://"
        )):
            url = "https://" + url

        self.active_tab.view.setUrl(
            QUrl(url)
        )

    def sync_url(
        self,
        url,
        tab
    ):

        if tab == self.active_tab:

            self.url_bar.setText(
                url.toString()
            )

    # -----------------------------------
    # Update Tab Title
    # -----------------------------------
    def update_tab_title(
        self,
        tab,
        title
    ):

        index = self.tab_widget.indexOf(
            tab.container
        )

        if index != -1:

            self.tab_widget.setTabText(
                index,
                title[:20]
            )

    # -----------------------------------
    # Toolbar Actions
    # -----------------------------------
    def go_back(self):

        if self.active_tab:
            self.active_tab.view.back()

    def go_forward(self):

        if self.active_tab:
            self.active_tab.view.forward()

    def reload_page(self):

        if self.active_tab:
            self.active_tab.view.reload()


# -----------------------------------
# Run Browser
# -----------------------------------
def main():

    app = QApplication(sys.argv)

    browser = SnowyBrowser()

    browser.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
