import zipfile
import os
import os.path
from zipfile import ZipFile


carpeta_Zip=r"Z:/Latex Report"
ruta_extraidos=r"C:/Users/echirino/Documents/exel_descomprimidos_SERAC"
password=None

#obtener archivos zip
for archivo in os.listdir(carpeta_Zip):
    if archivo.endswith(".zip"):
        ruta_zip = os.path.join(carpeta_Zip, archivo)
        print(ruta_zip)
        #obtener lista de nombres de archivos dentro del ZIP
        with ZipFile(ruta_zip, 'r') as zip:
            for excels in zip.infolist():
                nombres_excel=zip.namelist()
                
                #Verificar la longitud de la lista para filtrar los archivos que sean reportes
                l=len(nombres_excel)
                if l > 1:
                    reporte= nombres_excel[1]
                    print(reporte)
                    break
                else: 
                    reporte= nombres_excel[0]
                    print(reporte)
                    
                    break
                
            #Crear nuevo path para la comprobación 
            newpath= ruta_extraidos + "/" + str(reporte)
            print(newpath)
            #Verificar si el html es igual al xls 
            base_reporte, extension_reporte=os.path.splitext(newpath)
            extension='.html'
            verificacion= base_reporte + extension
            path_verificacion=os.path.join(ruta_extraidos, verificacion)
                
       #comprobacion de existencia del archivo xls de reporte en la carpeta de extraidos
            comprobacion= os.path.exists(path_verificacion)

            print(comprobacion)
            if comprobacion == False :
                print("activar proceso")
                zip.extract(reporte, path=ruta_extraidos, pwd=password)
                #renombrar reportes de xls a html
                for reportes in os.listdir(ruta_extraidos):
                    if reportes.endswith('xls'):
                        base, extension= os.path.splitext(reportes)
                        nuevo_nombre=base + '.html'
                        path1= os.path.join(ruta_extraidos, reportes)
                        path2= os.path.join(ruta_extraidos, nuevo_nombre)
                        comprobacion= os.path.exists(path2)
                        print(comprobacion)
                        if comprobacion == False:
                            print("¡Hecho!")
                            os.rename(path1, path2)
                            print("------------------------------------------------------------------")
                        else:
                            print("Ya se convirtió en html")
                            print("------------------------------------------------------------------")
                            
            else:
                print("ya existe")
                print("------------------------------------------------------------------")
                

            
       


                

            
        
        
        
        
        
        
    
        
            
            
    

        
                        
                                    