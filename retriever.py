# This Python file uses the following encoding: utf-8
import sys
import os
import pickle
from mainwindow import Ui_Form
from PySide2.QtWidgets import QApplication
from PySide2.QtWidgets import *
from PySide2.QtCore import Qt , QFile, QDir , QIODevice ,QObject , Slot , QPointF
from PySide2.QtGui import QImage , QColor, QPixmap , QPainter
from PySide2.QtUiTools import QUiLoader
from PySide2.QtSql import QSqlDatabase , QSqlQuery
from matplotlib import pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT
import cv2
import numpy as np

def get_mean_color(image):
    return np.mean(image , axis =(0,1))

def get_color_hist(image):
    # tuple to select colors of each channel line as enumerator
    colors = ("red", "green", "blue")
    channel_ids = (2, 1, 0)
    histogram = np.zeros((64,3))
    max_histogram = 0
    for channel_id, c in zip(channel_ids, colors):
        histogram[:,channel_id], bin_edges = np.histogram(image[:, :, channel_id],bins=64)
    if max_histogram < histogram.max():
        max_histogram = histogram.max()
    histogram = histogram*256 / max_histogram
    histogram = np.floor(histogram)
    return histogram

def get_color_layout(image):
    img_h = int(image.shape[0]/8)
    img_w = int(image.shape[1]/8)
    color_layout = np.zeros((8,8,3))
    for i in range(8):
        for j in range(8):
            sector = image[(i)*img_h:(i+1)*img_h,(j)*img_w:(j+1)*img_w,:]
            color_layout[i,j,:] = np.floor(np.mean(sector, axis =(0,1)))
    return color_layout



def histogram_similarity_measure(input_hist , model_hist):
    return (np.sum(np.minimum(input_hist,model_hist))/np.sum(model_hist) *100)

def layout_similarity_measure(input_layout , model_layout ):
    comparison =1- np.absolute(input_layout-model_layout)
    return (np.mean(comparison) *100)

def get_video_key_frames(video):
    current_layout = np.zeros((64,3))
    self.video.set(cv2.CAP_PROP_POS_FRAMES , 0)
    ret, frame = video.read()
    last_layout = get_color_hist(frame)
    keyframes = []
    keyframes.append(last_layout)
    while(video.isOpened()):
        # vid_capture.read() methods returns a tuple, first element is a bool
        # and the second is frame
        ret, frame = video.read()
        if ret == True:
            current_layout = get_color_hist(frame)
            if not histogram_similarity_measure(current_layout,last_layout,50):
                repeated = False
                for frm in keyframes:
                    if not histogram_similarity_measure(current_layout,frm,50):
                        repeated = True
                if not repeated:
                    keyframes.append(current_layout)
            last_layout = current_layout
        else:
            break
    return keyframes


class retriever(QWidget):
    def __init__(self):
        super(retriever,self).__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.ui.searchTypeComboBox.currentIndexChanged.connect(self.on_searchTypeComboBox_indexChanged)
        self.ui.searchMethodComboBox.currentIndexChanged.connect(self.on_searchMethodComboBox_indexChanged)
        self.ui.filePathLineEdit.editingFinished.connect(self.on_filePathLineEdit_editingFinished)
        self.ui.browseButton.clicked.connect(self.on_browseButton_clicked)
        self.ui.searchButton.clicked.connect(self.on_searchButton_clicked)
        self.ui.addToDataBaseButton.clicked.connect(self.on_addToDataBaseButton_clicked)
        self.scene = QGraphicsScene()
        hght = 85
        wdth = 245
#        hght = self.ui.inputImageGraphicsView.size().height()
#        wdth = self.ui.inputImageGraphicsView.size().width()
        self.histview = FigureCanvas(Figure(figsize=(wdth/72, hght/72)))
        self.axes = self.histview.figure.subplots()
        vlayout = QVBoxLayout()
        vlayout.addWidget(self.histview)
        self.ui.histogramWidget.setLayout(vlayout)
        self.ui.histogramWidget.hide()
        self.indexMethod = 0
        self.indexType = 0
        self.imageExists = False
#        self.db = QSqlDatabase("QSQLITE")
#        self.db.setDatabaseName("content.db")
        self.dataBaseFiles = [
        "path_img_db.pickle",
        "mean_clr_db.pickle",
        "hist_img_db.pickle",
        "clr_lyt_db.pickle",
        "path_vid_db.pickle"
        ]
        if not os.path.isfile("./path_img_db.pickle"):
            temp = []
            for name in self.dataBaseFiles:
                pickle_out = open(name, 'wb')
                pickle.dump(temp , pickle_out)
                pickle_out.close()







    def on_searchTypeComboBox_indexChanged(self,index):
        self.scene.clear()
        self.ui.searchMethodComboBox.clear()
        self.ui.resultTable.clearContents()
        self.ui.resultTable.setRowCount(0)
        temp = self.ui.inputImageGraphicsView.scene()
        if not temp == None:
            temp.clear()
        temp = self.ui.inputRepresentation.scene()
        if not temp == None:
            temp.clear()
        self.ui.filePathLineEdit.clear()
        self.imageExists = False
        self.indexType = index
        if self.indexType == 0:
            self.ui.searchMethodComboBox.addItems(["Mean Color" , "Histogram Similarity" , "Color Layout"])
        elif self.indexType == 1:
            self.ui.searchMethodComboBox.addItems([ "By videoclip","By photo" ])

    def on_searchMethodComboBox_indexChanged(self,index):
        self.indexMethod = index
        self.ui.resultTable.clearContents()
        self.ui.resultTable.setRowCount(0)
        if self.indexType == 0:
            self.ui.label.setText(self.ui.searchMethodComboBox.currentText())
            if self.imageExists ==True:
                self.display_input_representation(self.image)
        elif self.indexType == 1:
            self.ui.inputRepresentation.show()
            self.ui.histogramWidget.hide()
            temp = self.ui.inputImageGraphicsView.scene()
            if not temp == None:
                temp.clear()
            temp = self.ui.inputRepresentation.scene()
            if not temp == None:
                temp.clear()
            self.ui.filePathLineEdit.clear()
            self.ui.label.setText("Histogram")
    def on_filePathLineEdit_editingFinished(self):
#        dir = QDir()
#        dir.setPath(self.ui.filePathLineEdit.text())
#        if dir.exists():
#        print("the path exists")
        if self.ui.filePathLineEdit.text():
            self.ui.resultTable.clearContents()
            self.ui.resultTable.setRowCount(0)
            self.imageExists =True
            if self.indexType == 1 and self.indexMethod == 0:
                self.video = cv2.VideoCapture(self.ui.filePathLineEdit.text())
                total_frames = self.video.get(cv2.CAP_PROP_FRAME_COUNT)
                total_frames = int(total_frames/2)
                self.video.set(cv2.CAP_PROP_POS_FRAMES , total_frames)
                ret, frm = self.video.read()
                self.video.set(cv2.CAP_PROP_POS_FRAMES , 0)
                self.display_inputImage(frm)
                self.display_image_histogram(frm)
#                self.keyFrames = get_video_key_frames(self.video)
#                self.display_histFrame(self.keyFrames[0])
            else:
                self.image = cv2.imread(self.ui.filePathLineEdit.text())
#                self.preview = QPixmap(self.ui.filePathLineEdit.text())
                self.display_inputImage(self.image)
                self.display_input_representation(self.image)
    def on_browseButton_clicked(self):
        if self.indexType == 1 and self.indexMethod == 0:     # video input
            self.filename = QFileDialog.getOpenFileName(self,"Open File",".",
                                                        "Videos (*.mp4)")
        else:       # images
            self.filename = QFileDialog.getOpenFileName(self, "Open File",
                                                        ".","Images (*.png *.jpg)")
        self.ui.filePathLineEdit.setText(self.filename[0])
        self.on_filePathLineEdit_editingFinished()


    def display_inputImage(self, cv2Image):
        height, width, channel = cv2Image.shape
        bytesPerLine = 3 * width
        qImg = QImage(cv2Image.data, width, height, bytesPerLine, QImage.Format_BGR888)
        self.preview = QPixmap.fromImage(qImg)
        self.preview = self.preview.scaled(self.ui.inputImageGraphicsView.size(),Qt.KeepAspectRatio)
        self.scene = QGraphicsScene(self)
        self.scene.addPixmap(self.preview)
        self.ui.inputImageGraphicsView.setScene(self.scene)

    def display_img_table(self,path , percentage , img_vid = True):
        if img_vid == True:
            rowNum = self.ui.resultTable.rowCount()
            self.ui.resultTable.setRowCount(rowNum+1)
            filenam = QLabel(path , self)
            self.ui.resultTable.setCellWidget(rowNum , 0 , filenam)
            similSTR = QLabel(str(percentage) , self)
            self.ui.resultTable.setCellWidget(rowNum , 1 , similSTR)
            prev = QPixmap(path)
            prev = prev.scaled(self.ui.inputImageGraphicsView.size(),Qt.KeepAspectRatio)
            scen = QGraphicsScene(self)
            scen.addPixmap(prev)
            graphics = QGraphicsView(self)
            graphics.setScene(scen)
            self.ui.resultTable.setCellWidget(rowNum , 2 , graphics)
        else:
            vid = cv2.VideoCapture(path)
            total_frames = vid.get(cv2.CAP_PROP_FRAME_COUNT)
            total_frames = int(total_frames/2)
            vid.set(cv2.CAP_PROP_POS_FRAMES , total_frames)
            ret, frm = vid.read()
            vid.set(cv2.CAP_PROP_POS_FRAMES , 0)
            height, width, channel = frm.shape
            bytesPerLine = 3 * width
            qImg = QImage(cv2Image.data, width, height, bytesPerLine, QImage.Format_BGR888)
            prev = QPixmap.fromImage(qImg)
            scen = QGraphicsScene(self)
            scen.addPixmap(prev)
            graphics = QGraphicsView(self)
            graphics.setScene(scen)
            self.ui.resultTable.setCellWidget(rowNum , 2 , graphics)

    def display_input_representation(self,cv2Image):
        if self.indexMethod == 0:
            self.display_image_mean(cv2Image)
        elif self.indexMethod == 1:
            self.display_image_histogram(cv2Image)
        elif self.indexMethod == 2:
            self.display_image_layout(cv2Image)

    def display_histFrame(self,frameIn):
        self.ui.inputRepresentation.hide()
        self.ui.histogramWidget.show()
        colors = ("red", "green", "blue")
        channel_ids = (2, 1, 0)
        bins = range(64)
        self.axes.clear()
        for channel_id, c in zip(channel_ids, colors):
            self.axes.plot(bins , frameIn[:,channel_id] ,color = c)
        self.histview.draw()

    def display_image_mean(self,cv2Image):
        self.ui.inputRepresentation.show()
        self.ui.histogramWidget.hide()
        temp = self.ui.inputRepresentation.scene()
        if not temp == None:
            temp.clear()
        temp =get_mean_color(cv2Image).reshape(1,1,3)
        new_dim = (cv2Image.shape[1],cv2Image.shape[0])
        temp =cv2.resize(temp/255.0 ,  new_dim ,interpolation=cv2.INTER_AREA)
        temp = temp * 255.0
        self.layout_arr = np.uint8(temp)
        bytesPerLine = 3 * self.layout_arr.shape[1]
        qImg = QImage(self.layout_arr.data, self.layout_arr.shape[1], self.layout_arr.shape[0], bytesPerLine, QImage.Format_BGR888)
        self.represent = QPixmap.fromImage(qImg)
        self.represent = self.represent.scaled(self.ui.inputRepresentation.size(),Qt.KeepAspectRatio)
        self.repscene = QGraphicsScene(self)
        self.repscene.addPixmap(self.represent)
        temp = self.ui.inputRepresentation.scene()
        if not temp == None:
            temp.clear()
        self.ui.inputRepresentation.setScene(self.repscene)

    def display_image_histogram(self,cv2Image):
        self.ui.inputRepresentation.hide()
        self.ui.histogramWidget.show()
        colors = ("red", "green", "blue")
        channel_ids = (2, 1, 0)
#        colors = (QColor("Red"), QColor("Green"), QColor("Blue"))
#        channel_ids = (2, 1, 0)
        temp = get_color_hist(cv2Image)
        bins = range(64)
        self.axes.clear()
        for channel_id, c in zip(channel_ids, colors):
            self.axes.plot(bins , temp[:,channel_id] ,color = c)
        self.histview.draw()
#        chart = Qchart()
#        chart.legend().hide()
#        for channel in channel_ids:
#            series = QLineSeries()
#            series.setColor(colors[channel])
#            for bin , val in enumerate(self.layout_arr[:,channel]):
#                series.append(bin,val)
#            chart.addSeries(series)
#        chart.createDefaultAxes()
#        self.ui.inputRepresentation = QChartView(chart,self.ui.searchResultsGroupBox)
#        self.ui.inputRepresentation.setRenderHint(QPainter.Antialiasing)
        pass

    def display_image_layout(self,cv2Image):
        self.ui.inputRepresentation.show()
        temp = self.ui.inputRepresentation.scene()
        if not temp == None:
            temp.clear()
        self.ui.histogramWidget.hide()
        temp = get_color_layout(cv2Image)
        new_dim = (cv2Image.shape[1],cv2Image.shape[0])
        temp =cv2.resize(temp/255.0 ,  new_dim ,interpolation=cv2.INTER_AREA)
        temp = temp * 255
        self.layout_arr = np.uint8(temp)
#        height, width, channel = self.layout_arr.shape
        bytesPerLine = 3 * self.layout_arr.shape[1]
        qImg = QImage(self.layout_arr.data, self.layout_arr.shape[1], self.layout_arr.shape[0], bytesPerLine, QImage.Format_BGR888)
        self.represent = QPixmap.fromImage(qImg)
        self.represent = self.represent.scaled(self.ui.inputRepresentation.size(),Qt.KeepAspectRatio)
        self.repscene = QGraphicsScene(self)
        self.repscene.addPixmap(self.represent)
        temp = self.ui.inputRepresentation.scene()
        if not temp == None:
            temp.clear()
        self.ui.inputRepresentation.setScene(self.repscene)

    def on_searchButton_clicked(self):
        if self.imageExists == True:
            self.ui.resultTable.clearContents()
            self.ui.resultTable.setRowCount(0)
            if self.indexType ==0:
                if self.indexMethod == 0:
                    mean_clr = get_mean_color(self.image)
                    pickle_in = open(self.dataBaseFiles[0], 'rb')
                    path_list = pickle.load(pickle_in)
                    pickle_in.close()
                    pickle_in = open(self.dataBaseFiles[1], 'rb')
                    rep_list = pickle.load(pickle_in)
                    pickle_in.close()
                    simil  = 0
                    for indx,elem in enumerate(rep_list):
                        simil = np.absolute(elem - mean_clr)
                        simil = 1 - simil
                        simil = simil * 100
                        simil = np.mean(simil)
                        if simil >= self.ui.similaritySpinBox.value():
                            self.display_img_table(path_list[indx] , simil)


                elif self.indexMethod ==1:
                    histog = get_color_hist(self.image)
                    pickle_in = open(self.dataBaseFiles[0], 'rb')
                    path_list = pickle.load(pickle_in)
                    pickle_in.close()
                    pickle_in = open(self.dataBaseFiles[2], 'rb')
                    rep_list = pickle.load(pickle_in)
                    pickle_in.close()
                    simil  = 0
                    for indx,elem in enumerate(rep_list):
                        simil = histogram_similarity_measure(histog , elem )
                        if simil >= self.ui.similaritySpinBox.value():
                            self.display_img_table(path_list[indx] , simil)

                elif self.indexMethod ==2:
                    lyt = get_color_layout(self.image)
                    pickle_in = open(self.dataBaseFiles[0], 'rb')
                    path_list = pickle.load(pickle_in)
                    pickle_in.close()
                    pickle_in = open(self.dataBaseFiles[3], 'rb')
                    rep_list = pickle.load(pickle_in)
                    pickle_in.close()
                    simil  = 0
                    for indx,elem in enumerate(rep_list):
                        simil =histogram_similarity_measure(lyt , elem )
                        if simil >= self.ui.similaritySpinBox.value():
                            self.display_img_table(path_list[indx] , simil)

            elif self.indexType ==1:
                if self.indexMethod ==0:
                    keys = get_video_key_frames(self.video)
                    pickle_in = open(self.dataBaseFiles[0], 'rb')
                    path_list = pickle.load(pickle_in)
                    pickle_in.close()
                    pickle_in = open(self.dataBaseFiles[4], 'rb')
                    rep_list = pickle.load(pickle_in)
                    pickle_in.close()
                    simil_list = []
                    simil  = 0
                    for keyf in keys:
                        for vid in rep_list:
                            for elem in vid[1]:
                                simil = histogram_similarity_measure(keyf , elem )
                                if simil >= self.ui.similaritySpinBox.value():
                                    simil_list.append(simil)
                            if not len(simil_list) ==0:
                                simil = np.mean(np.array(simil_list))
                                self.display_img_table(path_list[indx] , simil)
                            simil_list=[]
                elif self.indexMethod == 1:
                    histog = get_color_hist(self.image)
                    pickle_in = open(self.dataBaseFiles[0], 'rb')
                    path_list = pickle.load(pickle_in)
                    pickle_in.close()
                    pickle_in = open(self.dataBaseFiles[4], 'rb')
                    rep_list = pickle.load(pickle_in)
                    pickle_in.close()
                    simil_list = []
                    frame_simil = []
                    simil  = 0
                    for vid in rep_list:
                        for elem in vid[1]:
                            simil = histogram_similarity_measure(histog , elem )
                            if simil >= self.ui.similaritySpinBox.value():
                                frame_simil.append(simil)
                        if not len(frame_simil) ==0:
                            simil_list.append(max(frame_simil))
                        frame_simil =[]
                    if not len(simil_list) ==0:
                        simil = np.mean(np.array(simil_list))
                        self.display_img_table(path_list[indx] , simil)
                    simil_list=[]


    def on_addToDataBaseButton_clicked(self):
        if self.imageExists == True:
            if self.indexType == 1 and self.indexMethod == 0: #video
                vid_details = []
                vid_details.append(self.ui.filePathLineEdit.text())
                keyframes = get_video_key_frames(self.video)
                vid_details.append(keyframes)
    #            detail =[]
                pickle_in = open(self.dataBaseFiles[4], 'rb')
                detail = pickle.load(pickle_in)
                pickle_in.close()
                detail.append(vid_details)
                pickle_out = open(self.dataBaseFiles[4],'wb')
                pickle.dump(detail,pickle_out)
                pickle_out.close()

            else:       #images
                img_details = []
                img_details.append(self.ui.filePathLineEdit.text())
                img_details.append(get_mean_color(self.image))
                img_details.append(get_color_hist(self.image))
                img_details.append(get_color_layout(self.image))
    #            paths = []
    #            mean_clrs= []
    #            hists = []
    #            clr_lyts = []
    #            paths.append(self.ui.filePathLineEdit.text())
    #            mean_clrs.append(get_mean_color(self.image))
    #            hists.append(get_color_hist(self.image))
    #            clr_lyts.append(get_color_layout(self.image))
                for i in range(4):
                    pickle_in = open(self.dataBaseFiles[i], 'rb')
                    detail = pickle.load(pickle_in)
                    pickle_in.close()
    #                detail = []
                    detail.append(img_details[i])
                    pickle_out = open(self.dataBaseFiles[i], 'wb')
                    pickle.dump(detail , pickle_out)
                    pickle_out.close()




if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = retriever()
    window.show()
    sys.exit(app.exec_())
