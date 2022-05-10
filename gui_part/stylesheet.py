'''
Stylesheet for defining several layout parameters of NICApy
The style can be change, if desired
'''

style_sheet = """
            QLineEdit, QComboBox, QLabel, QCheckBox, QRadioButton{
                font-size: 10pt;
            }
            QLabel[cssClass="display"]{
                font-size: 13pt;
                color: black, green, red;
            }
            QLabel[cssClass="displayfiles"]{
                font-size: 11pt;
                color: black, green, red;
            }
            QLineEdit{
                min-height: 12px;
                max-height: 15px;
                qproperty-alignment: AlignCenter;
            }
            QComboBox{
                min-height: 22px;
            }
            QGroupBox{
                font-size: 10pt;
                font-weight: bold;
                min-width: 20px;
            }
            QGroupBox::title{
                background: transparent;
            }
            QGroupBox[cssClass="outer"]{
                font-size: 13pt;
                font-weight: bold;
                min-height: 20px;
            }
            QListWidget{
                min-height: 20px;
            }
            """