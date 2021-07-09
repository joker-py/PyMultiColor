from qt_core import *

class MenuButton(QPushButton):
    def __init__(self, parent, icon, geometry):
        super(MenuButton, self).__init__(parent=parent)
        # SETUP MENU CUSTOM BUTTON
        self.icon  = icon
        self.setGeometry(0, geometry, 75, 75)
        self.setCheckable(True)
        self.setStyle(0)
        self.clicked.connect(lambda: parent.window.setCurrentButton(self))

    def setStyle(self, style):
        # SET BUTTON CURRENT STYLESHEET
        styles = ['QPushButton {background: transparent; icon-size: 40px; border: none; icon: url(' + self.icon + ')} QPushButton::hover {background: rgba(0, 0, 0, 0.05)} QPushButton::pressed {background: rgba(0, 0, 0, 0.1)}', f'background: rgba(0, 0, 0, 0.1); icon-size: 40px; border: none; icon: url({self.icon+"-selected"})']
        self.setStyleSheet(styles[style])

class TitleBar(QLabel):
    def __init__(self, parent, theme):
        super(TitleBar, self).__init__(parent=parent)
        # SETUP TITLE BAR
        self.parent = parent
        self.setGeometry(0, 0, 1200, 40)
        self.setStyleSheet(f"background-color: {theme}; font-size: 20px; color: white")
        self.setContentsMargins(10, 0, 0, 0)
        self.setText(parent.windowTitle())

        # CREATE MINIMIZE BUTTON
        self.minimizeBtn = QPushButton(self)
        self.minimizeBtn.setGeometry(1120, 0, 40, 40)
        self.minimizeBtn.setStyleSheet('QPushButton {background: transparent; border: none; icon-size: 20px; icon: url(icons/minimize)} QPushButton::hover {background: rgba(0, 0, 0, 0.05)} QPushButton::pressed {background: rgba(0, 0, 0, 0.1)}')
        self.minimizeBtn.released.connect(parent.showMinimized)

        # CREATE CLOSE BUTTON
        self.closeBtn = QPushButton(self)
        self.closeBtn.setGeometry(1160, 0, 40, 40)
        self.closeBtn.setStyleSheet('QPushButton {background: transparent; border: none; icon-size: 20px; icon: url(icons/close)} QPushButton::hover {background: rgba(0, 0, 0, 0.05)} QPushButton::pressed {background: rgba(0, 0, 0, 0.1)}')
        self.closeBtn.released.connect(parent.close)

    # SET WINDOW MOVABLE (WARNING IS NORMAL)
    def mousePressEvent(self, event):
        self.dragPos = event.globalPos()

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton:
            self.parent.move(self.parent.pos() + event.globalPos() - self.dragPos)
            self.dragPos = event.globalPos()
            event.accept()


class Window(QMainWindow):
    def __init__(self):
        super().__init__()

        # LOAD SETTINGS
        self.settings = json.loads(open('settings.json').read())

        # CREATE APP PALETTE
        self.palette = ['#284153', '#EAF6FF', '#2F97C1']

        # SETUP THEME COLORS
        self.themes = ['#FF006E', '#FB5607', '#F5B400', '#7B2CBF', '#9D4EDD', '#C77DFF',
                       '#40916C', '#52B788', '#74C69D', '#2A6F97', '#3A86FF', '#61A5C2']

        # LOAD THEME
        self.theme = self.themes[self.settings['theme']]

        # SETUP APP SETTINGS
        self.resize(1200, 720)
        self.setWindowTitle('MY APP NAME')
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setStyleSheet(f"background-color: {self.palette[0]}; font-family: Segoe UI; font-weight: bold")

        # CREATE LEFT MENU
        self.menu = QLabel(self)
        self.menu.window = self
        self.menu.setGeometry(0, 40, 75, 690)
        self.menu.setStyleSheet(f"background-color: {self.theme}")
        self.menu.lastBtn = None
        self.menu.home = MenuButton(self.menu, 'icons/home', 0)
        self.menu.search = MenuButton(self.menu, 'icons/search', 75)
        self.menu.calendar = MenuButton(self.menu, 'icons/persons', 150)
        self.menu.settings = MenuButton(self.menu, 'icons/settings', 605)

        # LOAD NAVIGATION BAR
        self.navbar = TitleBar(self, self.theme)

        # CREATE STACKED WIDGET
        self.pages = QStackedWidget(self)
        self.pages.setGeometry(75, 40, 1125, 680)
        self.pages.setStyleSheet('background: transparent; border: none')

        # SETUP PAGES
        self.menu.home.page = QWidget(); self.pages.addWidget(self.menu.home.page)
        self.menu.search.page = QWidget(); self.pages.addWidget(self.menu.search.page)
        self.menu.calendar.page = QWidget(); self.pages.addWidget(self.menu.calendar.page)
        self.menu.settings.page = QWidget(); self.pages.addWidget(self.menu.settings.page)

        # SETUP SETTINGS
        self.menu.settings.page.themes = QFrame(self.menu.settings.page)
        self.menu.settings.page.themes.setGeometry(50, 50, 1025, 325)
        self.menu.settings.page.themes.setStyleSheet('background: transparent; border: none')
        self.menu.settings.page.themes.lastObj = None

        # COLOR 1 BUTTON (self.themes[0])
        self.menu.settings.page.themes.color_1 = QPushButton(self.menu.settings.page.themes)
        self.menu.settings.page.themes.color_1.setGeometry(0, 0, 150, 150)
        self.menu.settings.page.themes.color_1.setStyleSheet(
            f'background: {self.themes[0]}; border: none; border-radius: 75px')
        self.menu.settings.page.themes.color_1.name = 0
        self.menu.settings.page.themes.color_1.clicked.connect(lambda: self.changeTheme(self.menu.settings.page.themes.color_1))

        # COLOR 2 BUTTON (self.themes[1])
        self.menu.settings.page.themes.color_2 = QPushButton(self.menu.settings.page.themes)
        self.menu.settings.page.themes.color_2.setGeometry(175, 0, 150, 150)
        self.menu.settings.page.themes.color_2.setStyleSheet(
            f'background: {self.themes[1]}; border: none; border-radius: 75px')
        self.menu.settings.page.themes.color_2.name = 1
        self.menu.settings.page.themes.color_2.clicked.connect(lambda: self.changeTheme(self.menu.settings.page.themes.color_2))

        # COLOR 3 BUTTON (self.themes[2])
        self.menu.settings.page.themes.color_3 = QPushButton(self.menu.settings.page.themes)
        self.menu.settings.page.themes.color_3.setGeometry(350, 0, 150, 150)
        self.menu.settings.page.themes.color_3.setStyleSheet(
            f'background: {self.themes[2]}; border: none; border-radius: 75px')
        self.menu.settings.page.themes.color_3.name = 2
        self.menu.settings.page.themes.color_3.clicked.connect(lambda: self.changeTheme(self.menu.settings.page.themes.color_3))

        # COLOR 4 BUTTON (self.themes[3])
        self.menu.settings.page.themes.color_4 = QPushButton(self.menu.settings.page.themes)
        self.menu.settings.page.themes.color_4.setGeometry(525, 0, 150, 150)
        self.menu.settings.page.themes.color_4.setStyleSheet(
            f'background: {self.themes[3]}; border: none; border-radius: 75px')
        self.menu.settings.page.themes.color_4.name = 3
        self.menu.settings.page.themes.color_4.clicked.connect(lambda: self.changeTheme(self.menu.settings.page.themes.color_4))

        # COLOR 5 BUTTON (self.themes[4])
        self.menu.settings.page.themes.color_5 = QPushButton(self.menu.settings.page.themes)
        self.menu.settings.page.themes.color_5.setGeometry(700, 0, 150, 150)
        self.menu.settings.page.themes.color_5.setStyleSheet(
            f'background: {self.themes[4]}; border: none; border-radius: 75px')
        self.menu.settings.page.themes.color_5.name = 4
        self.menu.settings.page.themes.color_5.clicked.connect(lambda: self.changeTheme(self.menu.settings.page.themes.color_5))

        # COLOR 6 BUTTON (self.themes[5])
        self.menu.settings.page.themes.color_6 = QPushButton(self.menu.settings.page.themes)
        self.menu.settings.page.themes.color_6.setGeometry(875, 0, 150, 150)
        self.menu.settings.page.themes.color_6.setStyleSheet(
            f'background: {self.themes[5]}; border: none; border-radius: 75px')
        self.menu.settings.page.themes.color_6.name = 5
        self.menu.settings.page.themes.color_6.clicked.connect(lambda: self.changeTheme(self.menu.settings.page.themes.color_6))

        # COLOR 7 BUTTON (self.themes[6])
        self.menu.settings.page.themes.color_7 = QPushButton(self.menu.settings.page.themes)
        self.menu.settings.page.themes.color_7.setGeometry(0, 175, 150, 150)
        self.menu.settings.page.themes.color_7.setStyleSheet(
            f'background: {self.themes[6]}; border: none; border-radius: 75px')
        self.menu.settings.page.themes.color_7.name = 6
        self.menu.settings.page.themes.color_7.clicked.connect(lambda: self.changeTheme(self.menu.settings.page.themes.color_7))

        # COLOR 8 BUTTON (self.themes[7])
        self.menu.settings.page.themes.color_8 = QPushButton(self.menu.settings.page.themes)
        self.menu.settings.page.themes.color_8.setGeometry(175, 175, 150, 150)
        self.menu.settings.page.themes.color_8.setStyleSheet(
            f'background: {self.themes[7]}; border: none; border-radius: 75px')
        self.menu.settings.page.themes.color_8.name = 7
        self.menu.settings.page.themes.color_8.clicked.connect(lambda: self.changeTheme(self.menu.settings.page.themes.color_8))

        # COLOR 9 BUTTON (self.themes[8])
        self.menu.settings.page.themes.color_9 = QPushButton(self.menu.settings.page.themes)
        self.menu.settings.page.themes.color_9.setGeometry(350, 175, 150, 150)
        self.menu.settings.page.themes.color_9.setStyleSheet(
            f'background: {self.themes[8]}; border: none; border-radius: 75px')
        self.menu.settings.page.themes.color_9.name = 8
        self.menu.settings.page.themes.color_9.clicked.connect(lambda: self.changeTheme(self.menu.settings.page.themes.color_9))

        # COLOR 10 BUTTON (self.themes[9])
        self.menu.settings.page.themes.color_10 = QPushButton(self.menu.settings.page.themes)
        self.menu.settings.page.themes.color_10.setGeometry(525, 175, 150, 150)
        self.menu.settings.page.themes.color_10.setStyleSheet(
            f'background: {self.themes[9]}; border: none; border-radius: 75px')
        self.menu.settings.page.themes.color_10.name = 9
        self.menu.settings.page.themes.color_10.clicked.connect(lambda: self.changeTheme(self.menu.settings.page.themes.color_10))

        # COLOR 11 BUTTON (self.themes[10])
        self.menu.settings.page.themes.color_11 = QPushButton(self.menu.settings.page.themes)
        self.menu.settings.page.themes.color_11.setGeometry(700, 175, 150, 150)
        self.menu.settings.page.themes.color_11.setStyleSheet(
            f'background: {self.themes[10]}; border: none; border-radius: 75px')
        self.menu.settings.page.themes.color_11.name = 10
        self.menu.settings.page.themes.color_11.clicked.connect(lambda: self.changeTheme(self.menu.settings.page.themes.color_11))

        # COLOR 12 BUTTON (self.themes[11])
        self.menu.settings.page.themes.color_12 = QPushButton(self.menu.settings.page.themes)
        self.menu.settings.page.themes.color_12.setGeometry(875, 175, 150, 150)
        self.menu.settings.page.themes.color_12.setStyleSheet(
            f'background: {self.themes[11]}; border: none; border-radius: 75px')
        self.menu.settings.page.themes.color_12.name = 11
        self.menu.settings.page.themes.color_12.clicked.connect(lambda: self.changeTheme(self.menu.settings.page.themes.color_12))

        # SHOW WINDOW
        self.setCurrentButton(self.menu.home)
        self.show()

    # CHANGE THEME COLOR BY BUTTON
    def changeTheme(self, object):
        # RECOLOR LAST SELECTED BUTTON
        if self.menu.settings.page.themes.lastObj:
            self.menu.settings.page.themes.lastObj.setStyleSheet(f'background: {self.themes[self.menu.settings.page.themes.lastObj.name]}; border: none; border-radius: 75px')

        # LOAD THEME
        self.theme = self.themes[object.name]

        # SET THEME ON WIDGETS
        self.menu.setStyleSheet(f"background-color: {self.theme}")
        self.navbar.setStyleSheet(f"background-color: {self.theme}; font-size: 16px; color: white; font-family: Nirmala UI; font-weight: regular")

        # COLOR SELECTED BUTTON
        object.setStyleSheet(f'background: {self.theme}; border: 5px solid white; border-radius: 75px')

        # SAVE CHANGED SETTINGS
        self.settings['theme'] = object.name
        json.dump(self.settings, open('settings.json', 'w'))

        # SET LAST OBJECT
        self.menu.settings.page.themes.lastObj = object

    # SET SELECTED MENU BUTTON
    def setCurrentButton(self, button):
        if self.menu.lastBtn:
            self.menu.lastBtn.setStyle(0)
        button.setStyle(1)
        self.menu.lastBtn = button
        self.pages.setCurrentWidget(button.page)

if __name__ == '__main__':
    app = QApplication(sys.argv) # LOAD APP

    window = Window() # LOAD WINDOW

    # \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
    sys.exit(app.exec()) # EXEC APP
    # ///////////////////////////////////////////////////////////////
