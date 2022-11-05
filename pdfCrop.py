import PySimpleGUI as sg
from PyPDF2 import PdfFileReader, PdfFileWriter

font_type = "Ubuntu"
font_dim = 15

layout = [
          [sg.Text('Source for Files ', size=(15, 1),font=(font_type, font_dim)), sg.InputText(),sg.FileBrowse(font=(font_type, font_dim)),sg.Button('', button_color=(sg.theme_background_color(),sg.theme_background_color()),image_filename="Icon.png", image_subsample=1, border_width=0)],
          [sg.Text('Set lower left  (eg:(100,0))   ',font=(font_type, font_dim)),sg.Input()],
          [],
          [sg.Text('Set upper right (eg:(500,741)) ',font=(font_type, font_dim)),sg.Input()],
          [],
          [sg.Button('Save',font=(font_type, font_dim)),sg.Button('Get Values',font=(font_type, font_dim)),sg.Button('Exit',font=(font_type, font_dim)),sg.T(' '  * 40),sg.Text('Version 1.0\nDeveloped by Dav')],]



window = sg.Window('Pdf Crop', layout)


while True: 
    event, values = window.read()
    if event in (None, 'Exit'):
        window.close()
        break
    if event in (None, 'Get Values'):
        path = values[0]
        reader = PdfFileReader(path,"r")
        page = reader.getPage(0)
        sg.popup('Number of pages', reader.getNumPages(), 
                 'Lower Left', page.cropBox.getLowerLeft(),
                 'Upper Left', page.cropBox.getUpperLeft(),
                 'Lower Right', page.cropBox.getLowerRight(),
                 'Upper Right', page.cropBox.getUpperRight(),
                 font=(font_type, font_dim))
    if event in (None, 'Save'):
    	#path_folder+file_name
        path = values[0]
        #convert into float variables the 4 values taken  from GUI
        x11 = float(values[1].replace("(","").replace(")","").split(",")[0])
        y11 = float(values[1].replace("(","").replace(")","").split(",")[1])
        x22 = float(values[2].replace("(","").replace(")","").split(",")[0])
        y22 = float(values[2].replace("(","").replace(")","").split(",")[1])
        #Crop Pdf
        reader = PdfFileReader(path,"r")
        writer = PdfFileWriter()
        n = reader.getNumPages()
        for i in range(reader.getNumPages()): 
            page = reader.getPage(i)
            page.cropBox.setLowerLeft((x11,y11))
            page.cropBox.setUpperRight((x22,y22))
            writer.addPage(page)
        new_path = path.replace(".pdf","2.pdf" )#add "2" to the new file name
        outstream = open(new_path,"wb")
        writer.write(outstream)
        outstream.close()
        sg.popup('The new file path is:\n',new_path, font=(font_type, font_dim))
