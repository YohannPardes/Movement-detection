import pygame, os, time

img_list = os.listdir("Footages")

# the ratio of checked pixel for omptimisation
RATIO = 3

# the treshold wich define if a frame is considered has moving frame (to tune)
trigger_treshold = 10000

img_list = [pygame.image.load("Footages/"+ img) for img in img_list]


WIDTH, HEIGHT = img_list[0].get_size()
screen = pygame.display.set_mode((WIDTH, HEIGHT))


def extract_pixels(img, ratio):
	img_width, img_height = img.get_size()
	# print(img_width, img_height)
	pixels = []

	for x in range(img_width//ratio):
		x = x*ratio
		ligne = []
		for y in range(img_height//ratio):
			y = y*ratio
			ligne.append(((x, y),img.get_at((x, y))))
		pixels.append(ligne)

	return pixels

def from_pixels_list_to_img(pixels):
	new_img = pygame.Surface((WIDTH, HEIGHT))
	x_ratio, y_ratio = WIDTH//RATIO, HEIGHT//RATIO 
	for ligne in pixels:
		for pixel in ligne:

			pygame.draw.rect(new_img, pixel[1], (pixel[0][0], pixel[0][1], x_ratio, y_ratio))

	return new_img

def compare_img(img_1, img_2):
	pxls_1 = extract_pixels(img_1, RATIO)
	pxls_2 = extract_pixels(img_2, RATIO)

	diff_array = []
	total_diff = 0
	for ligne_1, ligne_2 in zip(pxls_1, pxls_2):
		ligne = []
		for pxl_1, pxl_2 in zip(ligne_1, ligne_2):
			diff = abs(pxl_1[1][0] - pxl_2[1][0]), abs(pxl_1[1][1] - pxl_2[1][1]), abs(pxl_1[1][2] - pxl_2[1][2])
			ligne.append((pxl_1[0], diff))
			total_diff += (diff[0]+diff[1]+diff[2])/3
		diff_array.append(ligne)

	return diff_array, total_diff


done = False
while not done:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			done = True

	for index in range(len(img_list)-1):
		pixels, total_diff = compare_img(img_list[index], img_list[index+1])
		print(total_diff)
		if total_diff >= trigger_treshold:
			diff_rendering = from_pixels_list_to_img(pixels)
			screen.blit(diff_rendering, (0, 0))
			pygame.display.flip()

			time.sleep(1)

	done = True