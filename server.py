from flask import Flask
from flask_cors import CORS
import os
from flask import request
import requests
from bs4 import BeautifulSoup
from PIL import Image, ImageDraw, ImageFont


app = Flask(__name__)
CORS(app)




# удаляет ненужные файлы
def delete_trash():
	if(os.path.exists('a.jpg')):
		os.remove('a.jpg')
	if(os.path.exists('avatar.jpg')):
		os.remove('avatar.jpg')


# сохраняет аватар
def save_image(url):
	res = requests.get(url, stream=True)
	with open('avatar.jpg', 'wb') as f:
		for chunk in res.iter_content(81920):
			f.write(chunk)


# рисует бейджик
def draw_bage(name):
	avatar = Image.open('avatar.jpg').convert("RGBA").resize((130, 130), Image.ANTIALIAS)

	fontPath = "C:\\Windows\\Fonts\\Arial.ttf"
	font = ImageFont.truetype ( fontPath, 35) 
	im = Image.new("RGB", (449,250), "#adb9d3")
	draw = ImageDraw.Draw(im)
	draw.rectangle((155, 30, 293, 168), fill='#fffffb')
	
	# имя
	f_msg2 = "l"*len(name)
	w, h = draw.textsize(f_msg2)
	draw.text(((449-w*3)/2,180), name, font=font, fill="black")
	
	#draw = ImageDraw.Draw(im)
	im.save('a.jpg', 'JPEG')

	im = Image.open('a.jpg').convert("RGBA")
	im.paste(avatar, (160, 35), avatar)
	im.save('bage.png',dpi=(300,300))

# глафная функция
def parse(url):
	soup = BeautifulSoup(requests.get(url).text, 'html5lib')
	image_link = soup.find('img', class_='_11kf')['src']#.replace('_nc_cat=0', '_nc_cat=1')
	name = soup.find('a', class_='_2nlw').get_text().split(' ')[0] + ' ' + soup.find('a', class_='_2nlw').get_text().split(' ')[1]
	save_image(image_link)
	draw_bage(name)
	delete_trash()


@app.route("/", methods=["GET", "POST"])
def hello():
	url = request.args.get('text')
	parse(url)
	return open('index.html', 'r', encoding="utf-8").read()
	



if __name__ == "__main__":
	app.run()