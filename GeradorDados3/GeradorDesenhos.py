import tkinter as tk
from tkinter import ttk
import cv2
import PIL.Image, PIL.ImageTk
import numpy as np
import os
from tkinter import messagebox
import copy

def ImgNormalizer(img):
    w,h = img.shape
    DrawX = []
    DrawY = []
    for x in range(w):
        for y in range(h):
            if img[x][y] != 255:
                DrawX.append(x)
                DrawY.append(y)

    # Se não ouver desenho nenhum, retorna imagens completamente vazias
    if not DrawX:
        imgSmall = np.full((28,28), 0, dtype=np.uint8)
        imgSmall2 = np.full((28,28), 0, dtype=np.uint8)
        return imgSmall,imgSmall2
        
    # Pega os valores mínimos e máximos das coordenadas
    MaxXValue = np.max(DrawX)
    MinXValue = np.min(DrawX)
    MaxYValue = np.max(DrawY)
    MinYValue = np.min(DrawY)
    
    # Calcula as amplitudes
    XAmplitude = MaxXValue - MinXValue
    YAmplitude = MaxYValue - MinYValue
    
    if XAmplitude > YAmplitude:
        # Altera as coordenadas para ir de 0 ate a aplitude maxima e centraliza a amplitude menor
        Amp = XAmplitude
        for i in range(len(DrawX)):
            DrawX[i] = DrawX[i] - MinXValue
            DrawY[i] = DrawY[i] - MinYValue + (Amp/2) - (YAmplitude/2)
    else:
        # Altera as coordenadas para ir de 0 ate a aplitude maxima e centraliza a amplitude menor
        Amp = YAmplitude
        for i in range(len(DrawX)):
            DrawX[i] = DrawX[i] - MinXValue + (Amp/2) - (XAmplitude/2)
            DrawY[i] = DrawY[i] - MinYValue
    
    DrawSmall = []
    for i in range(len(DrawX)):
        # Reduz a amplitude para 28x28 com 2 pixels de borda e arredonda os resultados
        newpair = []
        newpair.append(((23/Amp)*DrawX[i]) + 2)
        newpair.append(((23/Amp)*DrawY[i]) + 2) 
        newpairR = np.int32(np.rint(newpair))
        DrawSmall.append(newpairR)
    # Deixa apenas os pares únicos, excluindo os repetidos após o arredondamento
    DrawSmall = np.unique(DrawSmall,axis=0)

    #Desenha a imagem 28x28
    imgSmall = np.full((28,28), 0, dtype=np.uint8)
    imgSmall2 = np.full((28,28), 0, dtype=np.uint8)
    for pair in DrawSmall:
        imgSmall[pair[0]][pair[1]] = 255
        cv2.circle(imgSmall2,(pair[1],pair[0]),1,(255,255,255),-1)

    return imgSmall,imgSmall2


# ========================================================================================================================


class JanelaInicial:
    def __init__(self,path):
        self.path = path
        self.window = tk.Tk()
        self.window.title("Initial Settings")

        #Dimensões da area de desenho
        self.canvas_width = 500
        self.canvas_height = 500

        #Criação da tela de desenho
        self.canvas = tk.Canvas(self.window, width=self.canvas_width, height=self.canvas_height)
        self.canvas.pack(side=tk.LEFT, pady=10, padx=10)

        # Create blank image for drawing
        self.image = np.ones((self.canvas_height, self.canvas_width, 3), dtype=np.uint8) * 255
        
        # Drawing parameters
        self.drawing = False
        self.last_x = None
        self.last_y = None
        self.color = (0,0,0)  # Black color
        self.thickness = 10

         # Bind mouse events
        self.canvas.bind("<Button-1>", self.start_drawing)
        self.canvas.bind("<B1-Motion>", self.draw)
        self.canvas.bind("<ButtonRelease-1>", self.stop_drawing)
        
        # Create controls
        self.controls_frame = tk.Frame(self.window)
        self.controls_frame.pack(side=tk.RIGHT, padx=10)

        # label de descrição
        self.count_label = tk.Label(self.controls_frame, text="Enter the name of the class to be generated and\ndraw a base to help in the drawing process")
        self.count_label.grid(row=0, column=0, pady=10)
        
        tk.Button(self.controls_frame, text="Clear(R)", command=self.clear_canvas).grid(row=1,column=0,pady=5)

        #Escolha de classe
        self.Class_selection_frame = tk.Frame(self.controls_frame)
        self.Class_selection_frame.grid(row=2, column=0, pady=5)
        self.class_label = tk.Label(self.Class_selection_frame, text="Choose a class:")
        self.class_label.grid(row=0, column=0, pady=5)
        self.classe_desenho = tk.Entry(self.Class_selection_frame)
        self.classe_desenho.grid(row=0, column=1, pady=5)
        
        # Botões
        ttk.Button(self.controls_frame, text="Confirm Class", command=self.GoToDrawing).grid(row=3, column=0, pady=5)

        self.update_canvas()
        
    def start_drawing(self, event):
        self.drawing = True
        self.last_x = event.x
        self.last_y = event.y
        
    def draw(self, event):
        if self.drawing:
            current_x, current_y = event.x, event.y
            # Draw on OpenCV image
            cv2.line(self.image, (self.last_x, self.last_y), (current_x, current_y), self.color, self.thickness)
            self.last_x, self.last_y = current_x, current_y

            self.update_canvas()
            
    def stop_drawing(self, event):
        self.drawing = False
        
    def clear_canvas(self):
        self.image = np.ones((self.canvas_height, self.canvas_width, 3), dtype=np.uint8) * 255
        self.update_canvas()
        
    def update_canvas(self):
        # Convert OpenCV image to PhotoImage
        rgb_image = cv2.cvtColor(self.image, cv2.COLOR_BGR2RGB)
        pil_image = PIL.Image.fromarray(rgb_image)
        self.photo = PIL.ImageTk.PhotoImage(image=pil_image)
        
        # Update canvas
        self.canvas.create_image(0, 0, image=self.photo, anchor=tk.NW)

    def GoToDrawing(self):
        classe = self.classe_desenho.get()
        if(classe == ""):
            messagebox.showerror("Error", "Enter a class!")
        else:
            self.window.withdraw()
            JanelaDesenho(self.window, self.path, classe, self.image)
    
    def run(self):
        self.window.mainloop()

class JanelaDesenho:
    def __init__(self, Config_window, path, DrawingName, base_image, count=0):
        self.window = tk.Toplevel()
        self.Config_window = Config_window
        self.path = path
        self.window.title(DrawingName)
        self.DrawingName = DrawingName
        self.count = count
        self.base_image = self.gray_image(base_image)
      

        self.Create_directory() 

        self.window.protocol("WM_DELETE_WINDOW", self.on_closing)

        # Bind keyboard events to the window
        self.window.bind("<Key>", self.key_press)
        # Set focus to the window so it can receive keyboard events
        self.window.focus_set()
        
        # Initialize canvas
        self.canvas_width = 500
        self.canvas_height = 500
        
        # Create canvas
        self.canvas = tk.Canvas(self.window, width=self.canvas_width, height=self.canvas_height)
        self.canvas.pack(side=tk.LEFT, pady=10, padx=10)
        
        # Create blank image for drawing
        self.image = copy.deepcopy(self.base_image)

        #Cria a segunda imagem vazia para desenhar
        self.image2 = np.ones((self.canvas_height, self.canvas_width, 3), dtype=np.uint8) * 255

        # Drawing parameters
        self.drawing = False
        self.last_x = None
        self.last_y = None
        self.color = (0,0,0)  # Black color
        self.thickness = 5
        
        # Bind mouse events
        self.canvas.bind("<Button-1>", self.start_drawing)
        self.canvas.bind("<B1-Motion>", self.draw)
        self.canvas.bind("<ButtonRelease-1>", self.stop_drawing)
        
        # Create controls
        self.controls_frame = ttk.Frame(self.window)
        self.controls_frame.pack(side=tk.RIGHT, padx=10)
        
        # label de contagem
        self.count_label = tk.Label(self.controls_frame, text=f'Drawn images = {str(self.count)}')
        self.count_label.pack(pady=10)
            
        # Botões
        ttk.Button(self.controls_frame, text="Save(S)", command=self.save_canvas).pack()
        ttk.Button(self.controls_frame, text="Clear(R)", command=self.clear_canvas).pack()

        self.update_canvas()
        
    def start_drawing(self, event):
        self.drawing = True
        
    def draw(self, event):
        if self.drawing:
            current_x, current_y = event.x, event.y
            # Draw on OpenCV image
            cv2.circle(self.image,
                       (current_x, current_y),
                       self.thickness,
                       self.color,
                       -1)
            # Draw on OpenCV image2
            cv2.circle(self.image2,
                       (current_x, current_y),
                       0,
                       self.color,
                       -1)
            self.update_canvas()
            
    def stop_drawing(self, event):
        self.drawing = False
        
    def clear_canvas(self):
        self.image = copy.deepcopy(self.base_image)
        self.image2 = np.ones((self.canvas_height, self.canvas_width, 3), dtype=np.uint8) * 255
        self.update_canvas()
        
    def update_canvas(self):
        # Convert OpenCV image to PhotoImage
        rgb_image = cv2.cvtColor(self.image, cv2.COLOR_BGR2RGB)
        pil_image = PIL.Image.fromarray(rgb_image)
        self.photo = PIL.ImageTk.PhotoImage(image=pil_image)
        
        # Update canvas
        self.canvas.create_image(0, 0, image=self.photo, anchor=tk.NW)
    
    def save_canvas(self):
        #Gera os nomes
        SaveNameThin = self.DrawingName +"-Thin-"+ str(self.count) + ".jpg"
        SaveNameBold = self.DrawingName +"-Bold-"+ str(self.count) + ".jpg"
        SaveNameFull = self.DrawingName +"-Full-"+ str(self.count) + ".jpg"

        #Gera os paths para salvar as imagens
        DataBankPathThin = os.path.join(self.path,"DataBase\\Thin\\"+self.DrawingName+"\\"+SaveNameThin)
        DataBankPathBold = os.path.join(self.path,"DataBase\\Bold\\"+self.DrawingName+"\\"+SaveNameBold)
        DataBankPathFull = os.path.join(self.path,"DataBase\\Full\\"+self.DrawingName+"\\"+SaveNameFull)


        ImagesSmall = ImgNormalizer(cv2.cvtColor(self.image2, cv2.COLOR_BGR2GRAY))
        # Salva as imagens no caminho selecionado
        if not cv2.imwrite(DataBankPathThin, ImagesSmall[0]):
            raise Exception("Could not write the image")
        if not cv2.imwrite(DataBankPathBold, ImagesSmall[1]):
            raise Exception("Could not write the image")
        if not cv2.imwrite(DataBankPathFull, self.image2):
            raise Exception("Could not write the image")
        
        self.count = self.count + 1
        self.count_label.config(text=f'Drawn images = {str(self.count)}')

    def key_press(self, event):
        """Handle keyboard events"""
        key = event.keysym

        # Salva a imagem quando 's' é pressionado
        if key.lower() == "s":
            self.save_canvas()
        # Limpa a imagem quando 'r' é pressionado
        elif key.lower() == "r":
            self.clear_canvas()

    def Create_directory(self):
        # Create the directory
        ThinDatabase = os.path.join(self.path, "DataBase\\Thin\\"+self.DrawingName)
        BoldDatabase = os.path.join(self.path, "DataBase\\Bold\\"+self.DrawingName)
        FullDatabase = os.path.join(self.path, "DataBase\\Full\\"+self.DrawingName)
        
        #Thin DataBase
        try:
            os.makedirs(ThinDatabase)
            print(f"Directory '{ThinDatabase}' created successfully.")
        except FileExistsError:
            print(f"Directory '{ThinDatabase}' already exists.")
        except PermissionError:
            print(f"Permission denied: Unable to create '{ThinDatabase}'.")
        except Exception as e:
            print(f"An error occurred: {e}")

        #Bold DataBase
        try:
            os.makedirs(BoldDatabase)
            print(f"Directory '{BoldDatabase}' created successfully.")
        except FileExistsError:
            print(f"Directory '{BoldDatabase}' already exists.")
        except PermissionError:
            print(f"Permission denied: Unable to create '{BoldDatabase}'.")
        except Exception as e:
            print(f"An error occurred: {e}")

        #Full DataBase
        try:
            os.makedirs(FullDatabase)
            print(f"Directory '{FullDatabase}' created successfully.")
        except FileExistsError:
            print(f"Directory '{FullDatabase}' already exists.")
        except PermissionError:
            print(f"Permission denied: Unable to create '{FullDatabase}'.")
        except Exception as e:
            print(f"An error occurred: {e}")
        
        self.count = len(os.listdir(ThinDatabase))

    def on_closing(self):
        if messagebox.askokcancel("Quit", "Do you really want to quit?"):
            self.window.destroy()
            self.Config_window.deiconify()

    def gray_image(self,base_image):
        gray_image = np.where(base_image == 0, 127, base_image)
        return gray_image

# ======================================================================================================

if __name__ == "__main__":
    path = os.getcwd()
    app = JanelaInicial(path)
    app.run()