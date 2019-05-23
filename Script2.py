#-*-coding:utf-8-*-

#
#............. Criado por Lucas V. Araujo .............
#

from Tkinter import *
import ImageTk, FileDialog, os, threading, sys
import tkSimpleDialog, tkMessageBox
from PIL import Image, ImageDraw2
class Janela:
    def __init__(self, itk):
        if not 'tmp' in os.listdir(os.curdir):
            os.mkdir('tmp')

        self.current_thread=None
        self.escala = 1
        self.jn=itk

        self.fr1=Frame(itk)
        self.fr1.pack(side=LEFT, fill="both", expand=False)

        self.fr2=Frame(itk)
        self.fr2.configure(width=220, height=700)
        self.fr2.pack(side=RIGHT, fill="y", expand=False)

        #
        #Menu

        self.main_menu = Menu(self.jn)
        self.menu_arquivo = Menu(self.main_menu)
        self.menu_arquivo.add_command(label='Abrir', command=self.abrir_img)
        self.menu_arquivo.add_separator()
        self.menu_arquivo.add_command(label='Salvar', command=self.salvar_img)
        self.menu_arquivo.add_separator()
        self.menu_arquivo.add_command(label='Sair', command=self.exit)
        self.menu_efeitos= Menu(self.main_menu)
        self.menu_efeitos.add_command(label='Tons de Cinza', command=self.th_cinza)
        self.menu_efeitos.add_separator()
        self.menu_efeitos.add_command(label='Negativo', command=self.th_negativo)
        self.menu_efeitos.add_separator()
        self.menu_efeitos.add_command(label='Somar constante a cada pixel', command=self.th_somapixel)
        self.menu_efeitos.add_separator()
        self.menu_efeitos.add_command(label='Binarização', command=self.th_binarizar)
        self.menu_efeitos.add_separator()
        self.menu_efeitos.add_command(label='Quantizar', command = self.Quantizar)
        self.menu_Extras= Menu(self.main_menu)
        self.menu_Extras.add_command(label="Encontrar círculos", command = self.encontrar_circulos)
        self.menu_Extras.add_separator()
        self.menu_Extras.add_command(label="Thumbnail", command=self.Thumbnail)
        self.menu_ajuda = Menu(self.main_menu)
        self.menu_ajuda.add_command(label='Sobre', command=self.About)
        self.main_menu.add_cascade(label='Arquivo', menu=self.menu_arquivo)
        self.main_menu.add_cascade(label='Efeitos', menu=self.menu_efeitos)
        self.main_menu.add_cascade(label="Extras", menu=self.menu_Extras)
        self.main_menu.add_cascade(label='Ajuda', menu=self.menu_ajuda)
        self.jn.configure(menu=self.main_menu)

        #
        #

        #
        #Pixel

        self.lb=Label(self.fr2, text='(X, Y)')
        self.lb.pack(side=BOTTOM)

        self.lb2=Label(self.fr2,text='(R, G, B)')
        self.lb2.pack(side=BOTTOM)

        self.seColor = Canvas(self.fr2)
        self.seColor.configure(width=50, height=50)
        self.seColor.pack(side=BOTTOM)

        #
        #

        #
        #Histogram

        self.cvHistogram = Canvas(self.fr2)
        self.rgbHistogram = Image.new("RGB", (300, 300), (255,255,255))
        self.Histogram = ImageTk.PhotoImage(image=self.rgbHistogram)
        self.cvHistogram.create_image(0,0,image=self.Histogram)
        self.cvHistogram.pack(side=BOTTOM, fill = "both", expand=True)

        #
        #

        self.c=Canvas(self.fr1)
        ImageTk.Image.new('RGB', (600, 400), (255, 255, 255)).save('tmp/default.jpg')
        self.currentImg = 'default.jpg'
        self.carrega_imagem(imagem='default.jpg')
        self.c.bind('<Motion>', self.c_mousemov)
        self.c.bind("<B1-Motion>", self.MouseClickedMove)
        self.c.bind("<ButtonRelease-1>", self.th_histogram)
        self.c.pack(fill="both", expand=True)


    def exit(self):
        self.jn.quit()
        sys.exit(0)
    def MouseClickedMove(self, e):
        try:
            self.pimg.putpixel((int(e.x/self.escala+1), int(e.y/self.escala)), (255,0,0))
            self.pimg.putpixel((int(e.x/self.escala)+1, int(e.y/self.escala)+1), (255,0,0))
            self.pimg.putpixel((int(e.x/self.escala), int(e.y/self.escala)), (255,0,0))
            self.pimg.putpixel((int(e.x/self.escala), int(e.y/self.escala)+1), (255,0,0))
        except Exception, e:
            print e.message
        self.carrega_imagem(self.pimg, True)

    def Thumbnail(self):
        WxH = tkSimpleDialog.askstring("Resolução", "Informe a resolução da thumbnail")
        if len(WxH) >0 and "x" in WxH:
            W = int(WxH.split("x")[0])
            H = int(WxH.split("x")[1])
            self.pimg.thumbnail((W, H))
            self.carrega_imagem(self.pimg)
    def About(self):
        self.MsgBox(msg='Programa criado em Python, usando as bibliotecas Tkinter e PIL, para demonstrar processamento de imagens.', sTitle='Sobre', typ='info')
    def MsgBox(self, msg, sTitle, typ='warning'):
        if typ=='warning':
            tkMessageBox.showwarning(title=sTitle, message=msg)
        elif typ=='error':
            tkMessageBox.showerror(title=sTitle, message=msg)
        elif typ=='info':
            tkMessageBox.showinfo(title=sTitle, message=msg)

    def carrega_imagem(self, imagem=None, dw = False):
        try:
            width, height = self.jn.winfo_width() - 130, self.jn.winfo_height() - 120
        except Exception, ex:
            pass

        try:
            self.pimg = Image.open(r'tmp/%s' % imagem) if type(imagem) == type('') else imagem
        except Exception, ex:
            self.MsgBox(msg=ex.message, sTitle='Erro!', typ='error')
        imgwidth, imgheight = self.pimg.size[0], self.pimg.size[1]
        #print 'Original: %dx%d' %(imgwidth, imgheight)
        if self.escala != 1:
            imgwidth = int(imgwidth * self.escala)
            imgheight = int(imgheight * self.escala)
            #print 'Auto-Resize'
        if imagem !='default.jpg':
            while (imgwidth > width) or (imgheight > height):
                imgwidth = int(imgwidth * 0.9)
                imgheight = int(imgheight * 0.9)
                self.escala = self.escala * 0.9
        if self.escala != 1:
            self.img=ImageTk.PhotoImage(self.img_resize(imgwidth, imgheight))
        else:
            self.img=ImageTk.PhotoImage(image=self.pimg)
        self.c.create_image(0,0, image=self.img, anchor=NW)
        self.c.configure(width=imgwidth, height=imgheight, scrollregion=self.c.bbox(ALL))
        if dw == False:
            self.th_histogram()


    def img_resize(self, width, height):
        try:
            #print 'Resize para: %dx%d' %(width, height)
            return self.pimg.resize((width, height))
        except Exception, e:
            self.MsgBox(e.message, "ERRO!", 'error')
            return None

    def Quantizar(self):
        try:
            self.carrega_imagem(self.pimg.quantize().convert('RGB')) #.convert('RGB')
        except:
            self.carrega_imagem(self.pimg.convert('RGB').quantize())


    def th_binarizar(self):
        self.pimg = self.pimg.convert('L') #.convert('RGB')
        if self.current_thread !=None:
            self.MsgBox('Aguarde até a operação atual ser finalizada', 'Aguarde...')
        else:
            valor = tkSimpleDialog.askinteger(title='Limiar', prompt='Entre com um número')
            if valor != None:
                for t in range(20):
                    self.current_thread = threading.Thread(target=self.binarizar, args=(valor, t))
                    self.current_thread.daemon=True
                    self.current_thread.start()
    def binarizar(self, limiar, rng):
        wt = self.pimg.size[0] / 20
        wt_f = wt * (rng+1)
        if rng == 19:
            wt_f = self.pimg.size[0]
        for i in range(wt * rng, wt_f):
            for j in range(self.pimg.size[1]):
                pxl = self.pimg.getpixel((i,j))
                if pxl < limiar:
                    pxl = 0
                else:
                    pxl=256
                self.pimg.putpixel((i,j), pxl)

        if rng == 19:
            self.carrega_imagem(self.pimg.convert('RGB'))
            self.current_thread=None

    def th_cinza(self):
        self.carrega_imagem(self.pimg.convert('L').convert('RGB'))

        #
        #
        #if self.current_thread !=None :
        #    self.MsgBox('Aguarde até a operação atual ser finalizada', 'Aguarde...')
        #else:
        #	for t in range(20):
        #		self.current_thread = threading.Thread(target=self.img_cinza, args=(t,))
        #		self.current_thread.daemon = True
        #		self.current_thread.start()
    #def img_cinza(self, rng):
    #	wt = self.pimg.size[0] / 20
    #	wt_f = wt * (rng+1)
    #	if rng == 19:
    #		wt_f = self.pimg.size[0]
    #	if self.pimg.mode == 'P':
    #		self.pimg = self.pimg.convert('RGB')
    #    for i in range(wt * rng, wt_f):
    #        for j in range(self.pimg.size[1]):
    #            cl=self.pimg.getpixel((i,j))
    #            nc=0
    #            for x in cl:
    #                nc+=x
    #            nc=int(nc/3.0)
    #            self.pimg.putpixel((i,j), (nc,nc,nc))
    #    if rng == 19:
    #    	self.carrega_imagem(self.pimg)
    #    	self.current_thread=None
    #
    #

    def th_somapixel(self):
        self.pimg = self.pimg.convert('RGB')
        if self.current_thread !=None :
            self.MsgBox('Aguarde até a operação atual ser finalizada', 'Aguarde...')
        else:
            value = tkSimpleDialog.askinteger(title='Constante', prompt='Entre com um número:')
            if value != None:
                for t in range(20):
                    self.current_thread = threading.Thread(target=self.somapixel, args=(value, t))
                    self.current_thread.daemon = True
                    self.current_thread.start()

    def somapixel(self, valor, rng):
        wt = self.pimg.size[0] / 20
        wt_f = wt * (rng+1)
        if rng == 19:
            wt_f = self.pimg.size[0]
        for i in range(wt * rng, wt_f):
            for j in range(self.pimg.size[1]):
                pxl=self.pimg.getpixel((i,j))
                self.pimg.putpixel((i,j), (pxl[0]+valor, pxl[1]+valor, pxl[2]+valor))
        if rng == 19:
            self.carrega_imagem(self.pimg)
            self.current_thread=None
    def circ(self, image, x0, y0, r, colr=0):
        for x1 in range(x0-r+1, x0+r-1):
            y = int(y0 - (r**2 - (x1-x0)**2)**0.5)
            cl=image.getpixel((x1, y+1))
            if cl != colr:
                return False
        for x1 in range(x0-r+1, x0+r-1):
            y = int(y0 + (r**2 - (x1-x0)**2)**0.5)
            cl=image.getpixel((x1, y-1))
            if cl !=colr:
                return False
        return True

    def rcirc(self, image, x, y, r, color="red"):
        Drawner = ImageDraw2.Draw(image)
        Drawner.ellipse(((x-1-r,y-1-r), (x+r+1, y+r+1)), ImageDraw2.Pen("red"))
        Drawner.ellipse(((x-r,y-r), (x+r, y+r)), ImageDraw2.Pen("red"))

    def getcirc(self, image, r, color=0):
        count = 0
        img = image.convert("L")
        for i in range(r, img.size[0]-r):
            for j in range(r, img.size[1]-r):
                if self.circ(img, i, j, r) ==True:
                    self.rcirc(image, i, j, r)
                    #print "Encontrada imagem em (%d, %d)" %(i,j)
                    i+=r
                    j+=r
                    count+=1
        self.carrega_imagem(image)
        self.MsgBox("%d círculos foram encontrados." %count, "Círculos", typ="info")
    def encontrar_circulos(self):
        raio = tkSimpleDialog.askinteger(title='Raio', prompt='Informe o raio dos círculos')
        if (raio > 0) and (self.current_thread == None):
            #for i in range(20):
            self.getcirc(self.pimg, raio)
    def th_negativo(self):
        self.pimg = self.pimg.convert('RGB')
        if self.current_thread !=None :
            self.MsgBox('Aguarde até a operação atual ser finalizada', 'Aguarde...')
        else:
            for t in range(20):
                self.current_thread = threading.Thread(target=self.img_negativo, args=(t,))
                self.current_thread.daemon = True
                self.current_thread.start()
    def img_negativo(self, rng):
        wt = self.pimg.size[0] / 20
        wt_f = wt * (rng+1)
        if rng == 19:
            wt_f = self.pimg.size[0]
        for i in range(wt * rng, wt_f):
            for j in range(self.pimg.size[1]):
                pxl=self.pimg.getpixel((i,j))                
                self.pimg.putpixel((i,j), (255-pxl[0], 255-pxl[1], 255-pxl[2]))
        if rng == 19:
            self.carrega_imagem(self.pimg)
            self.current_thread = None

    def c_mousemov(self,e):        
        self.lb['text']='(%d, %d)'%(e.x, e.y) # int(self.c['height'])- e.y)
        try:
            self.pxl=self.pimg.getpixel((int(e.x / self.escala), int(e.y/self.escala)))# int(self.c['height'])- e.y))
            if type(self.pxl) == type(()):
                try:
                    self.lb2['text']= '(R=%d, G=%d, B=%d)' % self.pxl
                except:
                    self.lb2['text']= '(R=%d, G=%d, B=%d)' % self.pxl[0:3]
                self.sCl=ImageTk.PhotoImage(image=ImageTk.Image.new('RGB', (50,50), self.pxl))
                self.seColor.create_image(0,0,image=self.sCl, anchor=NW)
            else:
                self.lb2['text']= self.pxl #'(R=%d, G=%d, B=%d)' % self.pxl
                self.sCl=ImageTk.PhotoImage(image=ImageTk.Image.new(self.pimg.mode, (50,50), self.pxl))
                self.seColor.create_image(0,0,image=self.sCl, anchor=NW)
        except IndexError:
            pass
        except Exception, e:
            print e.message

    def abrir_img(self):
        for f in os.listdir('tmp'):
            if f !='default.jpg':
                try:
                    os.remove('tmp/%s' %f)
                except Exception, e:
                    self.MsgBox(e.message, "ERRO!", 'error')
        self.fd=FileDialog.FileDialog(self.jn, 'Abrir imagem')
        self.currentImg=self.fd.go(os.curdir, pattern='*.jpg')
        if not(self.currentImg is None):
            self.escala = 1
            tmpName=self.currentImg.replace('\\', '/').split('/')[-1]
            open('tmp/%s' %tmpName, 'wb').write(open(self.currentImg, 'rb').read())
            self.currentImg=str(tmpName)
            self.carrega_imagem(self.currentImg)

    def salvar_img(self):
        sv=FileDialog.SaveFileDialog(self.jn, "Salvar imagem")
        pth=os.environ['USERPROFILE'] if os.name =='nt' else '/'
        imgName=sv.go(pth)
        if imgName !=None:
            self.pimg.save(imgName)

    def th_histogram(self, x=0, y=50):
        h=threading.Thread(target=self.draw_histogram, args=(y,))
        h.daemon=True
        h.start()

    def draw_histogram(self, y):
        his=self.pimg.histogram()
        h2=list(his)
        h2.sort()
        h2=h2[-1]
        red = his[0:256]
        green = his[256: 512]
        blue = his[512:768]
        self.rgbHistogram = Image.new('RGB', (256, 3*y+60), (255,255,255))
        self.rgbHistogramDraw = ImageDraw2.Draw(self.rgbHistogram)
        PosY = y
        for i in range(len(red)):
            self.rgbHistogramDraw.line(((i, PosY), (i, PosY -(red[i] * y)/h2)), ImageDraw2.Pen("red"))
        PosY+=70
        for i in range(len(green)):
            self.rgbHistogramDraw.line(((i, PosY), (i, PosY -(green[i] * y)/h2)), ImageDraw2.Pen("green"))
        PosY+=70
        for i in range(len(blue)):
            self.rgbHistogramDraw.line(((i, PosY), (i, PosY -(blue[i] * y)/h2)), ImageDraw2.Pen("blue"))
        self.rgbHistogram.save("Histogram.jpg")
        self.Histogram = ImageTk.PhotoImage(image=self.rgbHistogram)
        self.cvHistogram.create_image(0,0,image=self.Histogram, anchor=NW)
        self.cvHistogram.configure(width=self.rgbHistogram.size[0], height=self.rgbHistogram.size[1])
raiz=Tk()
raiz.title('Processamento de Imagem')
raiz.state('zoomed')
Janela(raiz)
raiz.mainloop()
