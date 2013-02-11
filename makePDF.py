#takes an xml file of a certain form and creates a pdf file from it

#next steps - clean up the linesplit abstraction
#also add image functionality

from reportlab.pdfgen import canvas
import sys
import xml.etree.ElementTree as ET
from reportlab.lib.units import inch
from reportlab.pdfbase.pdfmetrics import stringWidth
from reportlab.lib import utils
import os.path

PPTSIZE = (1024, 768)
TITLE_FONT = "Helvetica-Oblique"
TITLE_SIZE = .5*inch
MAIN_FONT = "Helvetica-Oblique"
MAIN_SIZE = 18
SECTION_FONT = "Helvetica-Bold"
SECTION_SIZE = .5*inch
TAB_SIZE = 0.5*inch
IMAGEPATH = os.path.join(os.path.dirname(__file__),"images")


def makeTitleSlide(c,title,date, slidenum):
	addLogo(c, forTitle=True)
	c.setFillGray(0.25)
	c.rect(1*inch,9*inch,12*inch,.05*inch, fill=1)
	c.rect(1*inch,1*inch,12*inch,.05*inch, fill=1)
	c.setFillGray(0)
	c.setFont(TITLE_FONT, TITLE_SIZE)
	c.drawCentredString(7*inch, 5.5*inch, "Analytics Group")
	c.setFont(MAIN_FONT, MAIN_SIZE)
	c.drawCentredString(7*inch, 4.5*inch, title)
	c.drawCentredString(7*inch, 3.5*inch, date)
	c.setFont(MAIN_FONT, MAIN_SIZE/1.2)
	c.drawString(1*inch, 1.2*inch, "Jarret Petrillo, CEO, jarret.petrillo@gmail.com")
	c.drawRightString(13*inch, 1.2*inch, "Matt Bogen, CEO, zebogen@gmail.com")
	c.showPage()

def makeSlide(c, title, lines, slidenum):
	addLogo(c)
	addDesign(c)
	addTitle(c, title)
	addText(c, lines, xstart=1.2, ystart=8.5, size = 10.8)
	addPageNumber(c,slidenum)
	c.showPage()
		
def makeSection(c, title, slidenum):
	addLogo(c)
	c.setFillGray(0.25)
	c.rect(0.8*inch,5*inch,12.4*inch,2*inch, fill=1)
	addTitle(c, title, forSection = True)
	addPageNumber(c,slidenum)
	c.showPage()
	
def makeData(c, title, lines, chartdata, slidenum):
	addLogo(c)
	addDesign(c)
	addTitle(c, title)
	addText(c, lines, xstart=1.2, ystart=3.5, size = 10.6)
	addChart(c, chartdata[0], xstart=1.2, ystart=8.5, size = 11)
	addPageNumber(c,slidenum)
	c.showPage()

def makeImage(c, title, imagename, slidenum):
	addLogo(c)
	addDesign(c)
	addTitle(c, title)
	addImage(c, imagename, xstart=1, ystart=8.5, xsize = 12, ysize = 7.0)
	addPageNumber(c,slidenum)
	c.showPage()

def buildPresentation(root):
	filename = sys.argv[-1].split(".")[0]+".pdf"
	c = makeCanvas(filename)
	count = 0
	for slide in root:
		if slide.tag =="title":
			makeTitleSlide(c, slide.attrib['name'], slide.attrib['date'], count)
		elif slide.tag=="slide":
			makeSlide(c, slide.attrib['title'],slide.findall("p"), count)
		elif slide.tag=="section":
			makeSection(c, slide.attrib['name'], count)	
		elif slide.tag=="data":
			makeData(c, slide.attrib['title'],slide.findall("p"),slide.findall("chart"), count)
		elif slide.tag=="imageslide":
			makeImage(c, slide.attrib['title'],slide.attrib['image'], count)
		count+=1
	c.save()

def makeCanvas(filename):
	return canvas.Canvas(filename, pagesize=PPTSIZE)

def addLine(c, textObj,x, yheight, wrapLen, bulletSpace, lineSpace, fontName, fontSize, addBullet=False, anchorHeight=False, center=False):
	if addBullet:
		xtemp = textObj.getX() - 0.2*inch
		c.rect(xtemp,yheight,.05*inch,.05*inch, fill=1) #adds the bullet box
	linetoprint = ""
	count = 0
	wordsinline = x.split() #splits words
	while count < len(wordsinline):
		while stringWidth(linetoprint,fontName, fontSize)< wrapLen and count < len(wordsinline):
			linetoprint+=wordsinline[count]+" "
			count+=1
		
		if anchorHeight and count < len(wordsinline):
			adjustTemp = (lineSpace, lineSpace/2.0)[center]
			textObj.moveCursor(0,-adjustTemp)
		
		textObj.textLine(linetoprint)
		yheight -= lineSpace
		linetoprint = ""
	textObj.moveCursor(0,bulletSpace)
	yheight -= bulletSpace
	return yheight

def addChart(c, chartdata, xstart, ystart, size):
	addChartTitle(c, chartdata, xstart, ystart)	
	addChartPlot(c, chartdata, xstart, ystart, size)
	
	
def addChartTitle(c, chartdata, xstart,ystart):
	titleName = chartdata.attrib.get('title',"")
	c.setFont(SECTION_FONT, MAIN_SIZE)
	c.drawString(xstart*inch, ystart*inch, titleName)

def addChartPlot(c, chartdata, xstart, ystart, size):
	chartHeight = 3.5*inch
	c.saveState()
	c.setLineWidth(5)
	c.setStrokeGray(0.2)

	axisX = xstart*inch + TAB_SIZE
	axisY = ystart*inch - 2*MAIN_SIZE
	axisEnd = axisX + size*inch - TAB_SIZE
	axisBottom = axisY - chartHeight
	
	axis = c.beginPath()
	axis.moveTo(axisX, axisY)
	axis.lineTo(axisX, axisBottom)
	axis.lineTo(axisEnd, axisBottom) 
	c.drawPath(axis, fill=0, stroke=1)
	
	numbersToPlot = [float(x) for x in chartdata.text.split(",")]
	minNum = min(numbersToPlot)
	maxNum = max(numbersToPlot)
	lineX = axisX + TAB_SIZE/2.0
	spaceX = (axisEnd - lineX) / (len(numbersToPlot)-1)
	
	c.setLineWidth(4)
	c.setStrokeColorRGB(0, 0.2, 0.4)

	line = c.beginPath()
	lineY = ((numbersToPlot[0]-minNum)/(maxNum - minNum)) * (chartHeight-MAIN_SIZE)+MAIN_SIZE
	line.moveTo(lineX,lineY+axisBottom) 
	for x in numbersToPlot[1:]:
		lineX+= spaceX
		lineY = ((x-minNum)/(maxNum - minNum)) * (chartHeight-MAIN_SIZE)+MAIN_SIZE
		line.lineTo(lineX,lineY+axisBottom) 	
	c.drawPath(line, fill=0, stroke=1)
	
	c.restoreState()
	
def addImage(c, imagename, xstart, ystart, xsize, ysize):
	imagepath=os.path.join(IMAGEPATH,imagename)
	img = utils.ImageReader(imagepath)
	iw, ih = img.getSize()
	aspect = ih / float(iw)
	if aspect < ysize/float(xsize): #this means that the width is full, so height has to be ajusted
		adjwidth, adjheight = xsize*inch, xsize*inch*aspect
	else: 		#the width has to be adjusted
		adjwidth, adjheight = ysize*inch/aspect, ysize*inch
	xpos = xstart*inch + (xsize*inch-adjwidth)/2.0 
	ypos = (ystart*inch - ysize*inch) + (ysize*inch-adjheight)/2.0 	
	c.drawImage(imagepath, xpos, ypos, width=adjwidth, height = adjheight)
	
def addText(c, lines, xstart, ystart, size):
	wrapSize = size*inch
	bulletSpace, lineSpace = 20, 30 #bulletspace is extra padding
	mainObj = c.beginText(xstart*inch, ystart*inch)
	mainObj.setFillGray(0)
	mainObj.setFont(MAIN_FONT, MAIN_SIZE)
	mainObj.setLeading(lineSpace) #this is the space between lines from the same bullet
	yheight = ystart*inch+5
	for x in lines:
		print x.text
		if x.attrib.get('tab',False):
			tabNum = float(x.attrib['tab'])
			mainObj.moveCursor(tabNum*TAB_SIZE, 0) #TAB_SIZE defined above in definition section
			wrapLen = wrapSize - tabNum*TAB_SIZE
			wrapLen = wrapSize - tabNum*TAB_SIZE
			yheight = addLine(c, mainObj,x.text, yheight, wrapLen, bulletSpace, lineSpace, MAIN_FONT, MAIN_SIZE, addBullet=True, anchorHeight=False, center=False)
			mainObj.moveCursor(-tabNum*TAB_SIZE, 0)

		else:
			wrapLen = wrapSize
			yheight = addLine(c, mainObj,x.text, yheight, wrapLen, bulletSpace, lineSpace, MAIN_FONT, MAIN_SIZE, addBullet=True, anchorHeight=False, center=False)
	c.drawText(mainObj)
	
def addPageNumber(slide, num):
	slide.saveState()
	slide.setFillGray(0.20)
	slide.setFont("Helvetica-Bold",14)
	slide.drawCentredString(7*inch, .5*inch,"%d"%num)
	slide.restoreState()
	
def addDesign(c):
	c.saveState()
	c.setFillGray(0.25)
	c.rect(1*inch,9*inch,12*inch,.05*inch, fill=1)
	c.rect(1*inch,1*inch,12*inch,.05*inch, fill=1)
	c.restoreState()
	
def addLogo(slide, forTitle=False):
	slide.saveState()
	slide.setFillGray(0.80)
	if forTitle:
		slide.rect(6*inch,6*inch,2*inch,1*inch, fill=1)
	else:
		slide.rect(11*inch,0,2*inch,1*inch, fill=1)
	slide.restoreState()

def addTitle(c,title, forSection = False):
	c.saveState()
	if forSection:
		titleAnchor = 5.8*inch
		titleObj = c.beginText(1.1*inch, titleAnchor)
		titleObj.setFillGray(1)
	else:
		titleAnchor = 9.3*inch
		titleObj = c.beginText(1.1*inch, titleAnchor)
		titleObj.setFillGray(0)
		
	bulletSpace, lineSpace = 0, 35
	wrapLen = 11*inch
	titleObj.setLeading(lineSpace)
	font, size = ((TITLE_FONT, TITLE_SIZE),(SECTION_FONT, SECTION_SIZE))[forSection]
	titleObj.setFont(font, size)
	newAnchor = addLine(c, titleObj,title, titleAnchor, wrapLen, bulletSpace, lineSpace, font, size, addBullet=False, anchorHeight=True, center = forSection)
	c.drawText(titleObj)
	c.restoreState()

def main():
	tree = ET.parse(sys.argv[-1])
	root = tree.getroot()
	buildPresentation(root)
	
main()