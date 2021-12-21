
import os
from xml.dom import minidom
import cv2

xml_folder = {"filename": "",
              "path": "",
              "size": {
                      "width":"",
                      "height":""
                      },
              "object": {
                      "name":"",
                      "bndbox":{
                              "xmin":"",
                              "ymin":"",
                              "xmax":"",
                              "ymax":"",
                              }
                      }
              }




def readXML(y,save_path,read_img,imageSize=800):
    file = minidom.parse(path + "/" + y)
    print("xml name: ",y)
    
    xml_folder["filename"] = file.getElementsByTagName('filename')
    xml_folder["filename"] = xml_folder["filename"][0].firstChild.data
#    print("filename:",xml_folder["filename"])
    
    xml_folder["path"] = file.getElementsByTagName('path')
    xml_folder["path"] = xml_folder["path"][0].firstChild.data
#    print("path:",xml_folder["path"])
    
    
    size = file.getElementsByTagName('size')
    xml_folder["size"]["width"] = size[0].getElementsByTagName('width')
    xml_folder["size"]["width"] = xml_folder["size"]["width"][0].firstChild.data
#    print("width:",xml_folder["size"]["width"])
    
    xml_folder["size"]["height"] = size[0].getElementsByTagName('height')
    xml_folder["size"]["height"] = xml_folder["size"]["height"][0].firstChild.data
#    print("height:",xml_folder["size"]["height"])
    

    
    myobject = file.getElementsByTagName('object')
#    print()
#    print(le-n(myobject))
    counter = 0
    
    for i in myobject:
        xml_folder["object"]["name"] = i.getElementsByTagName('name')
        xml_folder["object"]["name"] = xml_folder["object"]["name"][0].firstChild.data
#        print("name:",xml_folder["object"]["name"])
        
        bndbox = i.getElementsByTagName('bndbox')
        xml_folder["object"]["bndbox"]["xmin"] = bndbox[0].getElementsByTagName('xmin')
        xml_folder["object"]["bndbox"]["xmin"] = xml_folder["object"]["bndbox"]["xmin"][0].firstChild.data
#        print("xmin:",xml_folder["object"]["bndbox"]["xmin"])
        
        xml_folder["object"]["bndbox"]["ymin"] = bndbox[0].getElementsByTagName('ymin')
        xml_folder["object"]["bndbox"]["ymin"] = xml_folder["object"]["bndbox"]["ymin"][0].firstChild.data
#        print("ymin:",xml_folder["object"]["bndbox"]["ymin"])
        
        xml_folder["object"]["bndbox"]["xmax"] = bndbox[0].getElementsByTagName('xmax')
        xml_folder["object"]["bndbox"]["xmax"] = xml_folder["object"]["bndbox"]["xmax"][0].firstChild.data
#        print("xmax:",xml_folder["object"]["bndbox"]["xmax"])
        
        xml_folder["object"]["bndbox"]["ymax"] = bndbox[0].getElementsByTagName('ymax')
        xml_folder["object"]["bndbox"]["ymax"] = xml_folder["object"]["bndbox"]["ymax"][0].firstChild.data
#        print("ymax:",xml_folder["object"]["bndbox"]["ymax"])
        
        
        counter += 1
        writeIMG(save_path=save_path,read_img=read_img, len_object=len(myobject), counter=counter, imageSize=imageSize)
        writeXML(save_path=save_path, len_object=len(myobject), counter=counter,imageSize=imageSize)

##############################################################################
##############################################################################   

def writeIMG(save_path,read_img,len_object,counter, imageSize):
    img = cv2.imread(read_img + "/" + xml_folder["filename"])
    
    img_h, img_w,_ = img.shape
#    print("img_h, img_w ",img_h, img_w )
#    print()
    if img_h < imageSize and img_w < imageSize:
         #save image
        if len_object > 1:
            img_name = xml_folder["filename"].replace(".jpg", "")
            img_name = img_name +  "a" + str(counter) + ".jpg"
            save_img_path = save_path + "/" + img_name
        else:
            save_img_path = save_path + "/" + xml_folder["filename"]
        cv2.imwrite(save_img_path,img)
        
    else:
        
        xmin, ymin = xml_folder["object"]["bndbox"]["xmin"], xml_folder["object"]["bndbox"]["ymin"]
        xmax, ymax = xml_folder["object"]["bndbox"]["xmax"], xml_folder["object"]["bndbox"]["ymax"]
        xmin, ymin, xmax, ymax = int(xmin), int(ymin), int(xmax), int(ymax) 
        
        xSize = xmax - xmin
        ySize = ymax - ymin
#        print("xSize,ySize",xSize,ySize)
        
        if xSize > imageSize:
            pass
        else:
            y0 = int((imageSize - ySize) / 2)
    #        print("y0",y0)
            
            newy=[0,0]
    #        print("(ymin - y0)",(ymin - y0))
    #        print("(ymax + y0)",(ymax + y0), img_h)
            # y - orta
            if ((ymin - y0) >= 0) and ((ymax + y0) <= img_h):
                newy[0] = ymin - y0
                newy[1] = ymax + y0 
    #            print("0")
            
            elif ((ymin - y0) < 0) and ((ymax + y0) <= img_h):
                newy[0] = 0
                newy[1] = imageSize
    #            print("1")
                
            elif ((ymin - y0) >= 0) and ((ymax + y0) > img_h):
    #            newy[0] = img_h - imageSize
                newy[0] = 0 if (img_h - imageSize) <= 0 else (img_h - imageSize)
                newy[1] = img_h
    #            print("2")
            
            elif ((ymin - y0) < 0) and ((ymax + y0) > img_h):
                newy[0] = 0
                newy[1] = img_h
    #            print("3")
                
    #        print("yeni çerçeve y0", newy[0])
    #        print("yeni çerçeve y1", newy[1])
        #    
            #-----------------
            
            x0 = int((imageSize - xSize) / 2)
#            print("x0",x0)
            
            newx=[0,0]
#            print("(xmin - x0)",(xmin - x0))
#            print("(xmax + x0)",(xmax + x0), img_w)    
            # x - orta
            if ((xmin - x0) >= 0) and ((xmax + x0) <= img_w):
                newx[0] = xmin - x0 
                newx[1] = xmax + x0
#                print("0")
            
            elif ((xmin - x0) < 0) and ((ymax + x0) <= img_w):
                newx[0] = 0
                newx[1] = imageSize
#                print("1")
                
            elif ((xmin - x0) >= 0) and ((xmax + x0) > img_w):
                newx[0] = 0 if (img_w - imageSize) <= 0 else (img_w - imageSize)
                newx[1] = img_w
#                print("2")
                
            elif ((xmin - x0) < 0) and ((xmax + x0) < img_w):
                newx[0] = 0 
                newx[1] = img_w
#                print("3")
        #        
#            print("yeni çerçeve x0", newx[0])
#            print("yeni çerçeve x1", newx[1])
                
            
            new_ymin = ymin - newy[0]
            new_ymax = new_ymin + ySize
            
            new_xmin = xmin - newx[0]
            new_xmax = new_xmin + xSize
            
#            print("new_xmin, new_xmax",new_xmin, new_xmax)
#            print("new_ymin, new_ymax",new_ymin, new_ymax)
            
            xml_folder["object"]["bndbox"]["xmin"], xml_folder["object"]["bndbox"]["xmax"] = new_xmin, new_xmax
            xml_folder["object"]["bndbox"]["ymin"], xml_folder["object"]["bndbox"]["ymax"] = new_ymin, new_ymax
            
            
            #save image
            img2 = img[newy[0]: newy[1], newx[0]: newx[1]]
         
            xml_folder["size"]["width"] = img2.shape[1]
            xml_folder["size"]["height"] = img2.shape[0]
            
            if len_object > 1:
                img_name = xml_folder["filename"].replace(".jpg", "")
                img_name = img_name +  "a" + str(counter) + ".jpg"
                save_img_path = save_path + "/" + img_name
            else:
                save_img_path = save_path + "/" + xml_folder["filename"]
            cv2.imwrite(save_img_path,img2)


##############################################################################
##############################################################################
    
def writeXML(save_path,len_object,counter,imageSize):
    
    xmin, ymin = xml_folder["object"]["bndbox"]["xmin"], xml_folder["object"]["bndbox"]["ymin"]
    xmax, ymax = xml_folder["object"]["bndbox"]["xmax"], xml_folder["object"]["bndbox"]["ymax"]
    xmin, ymin, xmax, ymax = int(xmin), int(ymin), int(xmax), int(ymax) 
        
    xSize = xmax - xmin
    ySize = ymax - ymin
#    print(xSize,ySize)
        
    if xSize > imageSize:
        pass
    else:
        """read example xml"""
        example_xml = minidom.parse("example.xml")
        
#        #-------------------
#        img_filename = example_xml.getElementsByTagName('filename')
#        img_filename[0].firstChild.data = xml_folder["filename"]
        
        #-------------------
        img_path = example_xml.getElementsByTagName('path')
        img_path[0].firstChild.data = "C:/Users/mecit.sezgin/Desktop/plt/test"
        
        #-------------------
        img_size = example_xml.getElementsByTagName('size')
        img_size_width = img_size[0].getElementsByTagName('width')
        img_size_width[0].firstChild.data = xml_folder["size"]["width"]
        
        img_size_height = img_size[0].getElementsByTagName('height')
        img_size_height[0].firstChild.data = xml_folder["size"]["height"]
    
        #-------------------
        img_object = example_xml.getElementsByTagName('object')
        img_object_name = img_object[0].getElementsByTagName('name')
        img_object_name[0].firstChild.data = xml_folder["object"]["name"]
    
        img_object_bndbox = img_object[0].getElementsByTagName('bndbox')
        img_object_bndbox_xmin = img_object_bndbox[0].getElementsByTagName('xmin')
        img_object_bndbox_xmin[0].firstChild.data = xml_folder["object"]["bndbox"]["xmin"]
        
        img_object_bndbox_ymin = img_object_bndbox[0].getElementsByTagName('ymin')
        img_object_bndbox_ymin[0].firstChild.data = xml_folder["object"]["bndbox"]["ymin"]
        
        img_object_bndbox_xmax = img_object_bndbox[0].getElementsByTagName('xmax')
        img_object_bndbox_xmax[0].firstChild.data = xml_folder["object"]["bndbox"]["xmax"]
        
        img_object_bndbox_ymax = img_object_bndbox[0].getElementsByTagName('ymax')
        img_object_bndbox_ymax[0].firstChild.data = xml_folder["object"]["bndbox"]["ymax"]
        
        
        if len_object > 1:
            xml_name = xml_folder["filename"].replace(".jpg", "")
            xml_name = xml_name +  "a" + str(counter) + ".xml"
            save_xml_path = save_path + "/" + xml_name
        else:
            xml_name = xml_folder["filename"].replace(".jpg", "")
            xml_name = xml_name + ".xml"
            save_xml_path = save_path + "/" + xml_name
        
 
        #-------------------
        img_filename = example_xml.getElementsByTagName('filename')
        img_filename[0].firstChild.data = xml_name.replace("xml","jpg")
        
        with open(save_xml_path, "w") as fh:
            example_xml.writexml(fh)


##############################################################################
##############################################################################
path = "xml"
myList = os.listdir(path)
print("Total Classes Detected:",len(myList))
print("Importing  .......")

myXMLList = os.listdir(path) 
asd = 0
for y in myXMLList:
    asd +=1
    print(asd)
    readXML(y,read_img="foto",save_path="save",imageSize=500)
    
