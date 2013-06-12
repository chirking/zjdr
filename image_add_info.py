#coding=utf-8

import tempfile
from wx_send import download_file, upload_image
 
def add_info_name(origin_file, data_file, output_file):  
    container = open(origin_file, "rb").read()  
    data = open(data_file, "rb").read()  
    f = open(output_file, "wb")  
    f.write(container)  
    if len(data) <= 1024:  
        data = '%s%s' %(data,' '*(1024 - len(data)))  
    else:  
        raise Exception("flag data too long")  
 
    f.write(data)  
    f.close()  


def add_info(origin_file, data, output_file_name=None, file_type=None):
    container = origin_file.read()
    if None==output_file_name:
        output_file_name=tempfile.mktemp()    
        if None!=file_type and ''!=file_type:
            output_file_name = output_file_name+'.'+file_type

    f = open(output_file_name, "wb")  
    f.write(container)
    if len(data) <= 1024:  
        data = '%s%s' %(data,' '*(1024 - len(data)))  
    else:  
        raise Exception("flag data too long")  
    # print data
 
    f.write(data)
    f.close()  
    return output_file_name   


def get_info_pic_url(base_pic_url, info_data):
    base_pic_name = download_file(base_pic_url, 'jpg')
    info_pic_name = add_info(open(base_pic_name, 'rb'), info_data, file_type='jpg')
    info_pic_url = upload_image(None, open(info_pic_name, 'rb'), info_pic_name)

    return info_pic_url 

 
def read_info_name(filename):  
    container = open(filename,"r").read()  
    return container[len(container) - 1024:len(container)].rstrip()  

def read_info(file):  
    container = file.read()  
    return container[len(container) - 1024:len(container)].rstrip()
 

if "__main__" == __name__:  
    
    output_file_name = add_info(open('test/xlk.jpg', "rb"), 'add some info to image', 'test/xlk2.jpg')

    print read_info_name(output_file_name)

    info_pic_url = get_info_pic_url('http://img3.douban.com/lpic/s26686430.jpg', '你好，我是追剧达人')
    print info_pic_url

    info_pic_name = download_file(info_pic_url, 'jpg')

    print read_info_name(info_pic_name)

