# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\legolas\OneDrive\Desktop\untitled.ui'
#
# Created by: PyQt5 UI code generator 5.15.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.

from PyQt5.QtWidgets import QMainWindow, QApplication, QMenu, QMenuBar, QAction, QFileDialog, QMessageBox
from PyQt5.QtGui import QIcon, QImage, QPainter, QPen, QBrush
from PyQt5.QtCore import Qt, QPoint
from PyQt5 import QtWidgets, uic
import sys
import math
import os
import xml.etree.ElementTree as ET

#
# start
#

app = QApplication(sys.argv)
mainForm = uic.loadUi(os.path.join('.', 'ui', 'main.ui'))
addForm = uic.loadUi(os.path.join('.', 'ui', 'add.ui'))

mainForm.show() 

#
# variables
#

class cond:
    
    COND_calculate_committed = False    

# +

materials = []

ARRAY_FOR_XML_DATABASE = [
    ['Бетон', 2400],
    ['Песок', 1650],
    ['Щебень', 1430],
    ['Кирпич (полнотелый)', 2465],
    ['Кирпич (пустотелый)', 1305],
    ['Кирпич (облицовочный)', 1152],
    ['Природный камень', 2950],
    ['Ламинат', 875],
    ['Паркет', 705],
    ['Древесина', 645],
    ['Краска', 1250],
    ['Лак', 920],
    ['Штукатурка', 1500],
    ['Побелка', 0.25],
    ['Стекло', 2500]
]

ed = [
    ['кг', 'Килограмм'],
    ['м3', 'Метров кубических'],
    ['л', 'литров']
]

#
# utils
#

def splitNumb(s):
    
    whole = '_null_'
    fraction = '_null_'
    arrayS = s.split('.')
    
    if (len(arrayS) > 1):
        fraction = arrayS[1]
        
    whole = (arrayS[0])[::-1]
    arrayS = []
    i = 0
    
    while (i < len(whole)):

        arrayS.append(whole[i])   

        i += 1
        
        if (i % 3 == 0):
            
            arrayS.append(' ')
            
    s = (''.join(arrayS))[::-1]
        
    if (fraction != '_null_'):
        s += "." + fraction
    
    return s         

# +

def Array_to_XML():
    
    root = ET.Element('root')
    
    for i in range(len(materials)):
        
        m = ET.SubElement(root, 'MATERIAL' )
        ET.SubElement(m, 'material').text = str(materials[i][0])
        ET.SubElement(m, 'weight').text = str(materials[i][1])
        
    tree = ET.ElementTree(root)
    
    tree.write(os.path.join('.', 'db', 'database.xml'))

# +

def XML_to_Array():
    
    tree = ET.ElementTree(file=os.path.join('.', 'db', 'database.xml'))
    root = tree.getroot()
    
    for elems in root:
        
        materials.append([elems[0].text, float(elems[1].text)])

# +

def fill_materials():
    
    XML_to_Array()
    
    for i in range(len(materials)):
        
        mainForm.comboBox_material.addItem(materials[i][0])    

# +

def exc_NaN():
    
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Critical)
    msg.setInformativeText('Входные данные могут иметь только целочисленный формат или формат числа с плавающей запятой')
    msg.setWindowTitle("Ошибка")
    msg.exec_()

# +

def NaN_check_mainForm():
    
    number = "_null_"
    
    # 1
    
    number = mainForm.txt_sqr.text()
    
    try:
        number = float(number)
    except Exception:
        exc_NaN()
        return False
        pass 
    
    # 2
    
    number = mainForm.txt_width.text()
    
    try:
        number = float(number)
    except Exception:
        exc_NaN()
        return False
        pass     
    
    # 3
    
    number = mainForm.txt_price.text()
    
    try:
        number = float(number)
    except Exception:
        exc_NaN()
        return False
        pass     
    
    # 4
    
    number = mainForm.txt_number.text()
    
    try:
        number = float(number)
    except Exception:
        exc_NaN()
        return False
        pass     
    
    # +
    
    return True
# +

def NaN_check_addForm():
    
    number = addForm.addForm_width.text()
    
    try:
        number = float(number)
    except Exception:
        exc_NaN()
        return False
        pass     
    
    return True

# +

#
# form setup
#

fill_materials()

# +

for i in range(len(ed)):
    
    mainForm.comboBox_ed.addItem(ed[i][0])

# +

mainForm.txt_sqr.setText("100")
mainForm.txt_width.setText("1500")
mainForm.txt_price.setText("500")
mainForm.txt_number.setText("10")

#      
# form events
#

def mainForm_click_calculate(): 
    
    cond.COND_calculate_committed = True
    
    if (
        (mainForm.txt_sqr.text() != "") and 
        (mainForm.txt_width.text() != "") and
        (mainForm.txt_price.text() != "") and 
        (mainForm.txt_number.text() != "")           
    ):
        
        if (NaN_check_mainForm()):            
        
            selected_material = str(mainForm.comboBox_material.currentText())
            
            for i in range(len(materials)):            
                      
                if (materials[i][0] == selected_material):
                    
                    sqr = float(mainForm.txt_sqr.text())
                    width = float(mainForm.txt_width.text())
                    price = float(mainForm.txt_price.text())
                    number = float(mainForm.txt_number.text())
                    
                    resultSqr = sqr * (width / 1000)
                    resultPrice = 0
                    resultNumber = resultSqr
                    
                    unit = "_null_"
                    outStr = "Вам необходимо:   \n"
                    
                    for j in range(len(ed)):
                        
                        selected_ed = str(mainForm.comboBox_ed.currentText())
                        
                        if (selected_ed == ed[j][0]):
                            
                            if (j == 0):
                                resultNumber = resultSqr * float(materials[i][1])
                            elif (j == 2):
                                resultNumber = resultSqr * 1000
                            
                            resultSqr = round(resultNumber, 2)
                            resultNumber /= number 
                            resultPrice = round(resultNumber * price, 2)
                            unit = ed[j][0]
                            
                            outStr += splitNumb(str(math.ceil(resultNumber))) + " шт. * " 
                            outStr += splitNumb(str(price)) + " руб. = "
                            outStr += splitNumb(str( price if (resultPrice < price) else resultPrice)) + " руб.  \n( "
                            outStr += splitNumb(str(resultSqr)) + " " + unit + " )"
                            
                            mainForm.label_out.setText(outStr)             
            
    else:
        
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)
        msg.setInformativeText('Заполните все поля')
        msg.setWindowTitle("Ошибка")
        msg.exec_()   

# +

def mainForm_click_add():
    
    addForm.show()

# +

def mainForm_click_save():
        
    if (cond.COND_calculate_committed):
        
        filePath, _ = QFileDialog.getSaveFileName(None, "Save Image", "", "TXT(*.txt)")
    
        if filePath == "":
           return
       
        f = open(filePath , 'w')  
        f.write(str(mainForm.label_out.text()))
        f.close()  
        
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setInformativeText('Данные успешно сохранены в файл')
        msg.setWindowTitle("Успех")
        msg.exec_()  
    
    else:
        
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)
        msg.setInformativeText('Расчеты не были произведены')
        msg.setWindowTitle("Ошибка")
        msg.exec_()  

# +

def addForm_click_add():
    
    if (NaN_check_addForm()):
        
        if(
            (addForm.addForm_name.text() != "") and 
            (addForm.addForm_width.text() != "")
        ):
        
            materials.append([addForm.addForm_name.text(), addForm.addForm_width.text()])
            Array_to_XML()
            fill_materials()
            
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Information)
            msg.setInformativeText('Материал успешно добавлен в базу данных')
            msg.setWindowTitle("Успех")
            msg.exec_()    
        
        else:
            
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setInformativeText('Не все поля были заполнены')
            msg.setWindowTitle("Ошибка")
            msg.exec_()  

# +

mainForm.pushButton.clicked.connect(mainForm_click_calculate)
mainForm.add_to_xml.clicked.connect(mainForm_click_add)
mainForm.save_to_txt.clicked.connect(mainForm_click_save)
addForm.btn_add_db.clicked.connect(addForm_click_add)

#
# exit
#

sys.exit(app.exec())