from PyQt5.QtWidgets import QRadioButton

class Radio(QRadioButton):
    def __init__(self, group_name):
        super().__init__()

        self.group = group_name
        self.clicked.connect(lambda: self.toggle_effect(0))
    
        # EffectNone = QRadioButton("None")
        # EffectNone.group = "Effect"
        # EffectNone.clicked.connect(lambda: self.toggle_effect(0))

        # EffectBlur = QRadioButton("Blur")
        # EffectBlur.group = "Effect"
        # EffectBlur.clicked.connect(lambda: self.toggle_effect(1))
        
        # EffectGrey = QRadioButton("Grey")
        # EffectGrey.group = "Effect"
        # EffectGrey.clicked.connect(lambda: self.toggle_effect(2))

        # EffectCanny = QRadioButton("Canny")
        # EffectCanny.group = "Effect"
        # EffectCanny.clicked.connect(lambda: self.toggle_effect(3))
        
        # EffectSobel = QRadioButton("Sobel")
        # EffectSobel.group = "Effect"
        # EffectSobel.clicked.connect(lambda: self.toggle_effect(4))