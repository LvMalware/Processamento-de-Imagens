from PIL import Image, ImageDraw2
import math

img=Image.open('circulos.jpg')

def circ(image, x0, y0, r, colr=0):
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

def rcirc(image, x, y, r, color="red"):
	Drawner = ImageDraw2.Draw(image)
	Drawner.ellipse(((x-1-r,y-1-r), (x+r+1, y+r+1)), ImageDraw2.Pen("red"))
	Drawner.ellipse(((x-r,y-r), (x+r, y+r)), ImageDraw2.Pen("red"))

def getcirc(image, r, color=0):
	img = image.convert("L")
	for i in range(r, img.size[0]-r):
		for j in range(r, img.size[1]-r):
			if circ(img, i, j, r) ==True:
				rcirc(image, i, j, r)
				print "Encontrada imagem em (%d, %d)" %(i,j)
				i+=r
				j+=r
	image.save("TESTE.PNG")
getcirc(img, 50)