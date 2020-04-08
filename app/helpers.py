import os
def deleteImagen(deleteArticles):
	dir_imagenes=os.path.dirname(os.path.abspath(__file__))+"/articulos/templates/images/"
	
	if deleteArticles:
		#print(deleteArticles)
		for articulo in deleteArticles:
			#print(articulo.images)
			for image in articulo.images:
				#print(image)
				os.remove("{}{}".format(dir_imagenes,image.name))	
	else:
		print("Aqui va un abort")