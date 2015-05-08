makePDF: 
=======

## MakePDF implements a powerpoint mark-up language in Python

- Built on reportlab, makePDF takes an xml file and generates a fully rendered pdf, mimicing a powerpoint presentation 

## Project goals:
* abstract design decisions and content decisions from making a presentation
* implement flexible slide designs
* with the design questions solved, be able to make clean presentations as part of an analytics pipeline

## How it works:
- makePDF.py is executed from the command line
- running the following code 'python makePDF.py sample.xml' will create a pdf file named sample.pdf in the current drive

## Sample.xml

<?xml version="1.0"?>
<presentation>
	<info company="Company Title" logo="company_logo.png"/>
	
	<title title= "Presentation Title" date="Month Day, Year" people="First Name Last Name, email.address@gmail.com"/>

	<section name="Section Slide"/>
	
	<imageslide title="Slide Title" image='image.png'/>
	
	<codeslide title="Slide Title">
		<codeblock>
			<l focus="1">first line of code, will be bold</l>
			<l focus="1" indent="1">second line of code will be bold and indented once</l>
			<l indent="1">third line of code will be indented once, not bold</l>
		</codeblock>
	</codeslide>
	
	<data type="line" title= "Data Slide Title">
		<p>description of chart</p>
		<chart title="Revenue">1,3,4,7,8,11,8,4,3,5</chart>
	</data>
	
	<slide title= "Slide Title">
		<p>bullet point 1</p>
		<p>bullet point 2</p>
		<p>bullet point 3</p>
	</slide>

</presentation>
