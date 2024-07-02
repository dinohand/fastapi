from common.log_manager import Log_Manager

def file_save(file_name):
    logger = Log_Manager().getLogger('FILE')
    try:
        fs.save(file_name)
        logger.info('파일이 저장디었습니다')
        return "ok"
    except Exception as e:
        logger.error(e)
        return "fail"

def return_imagr_stream(img_local_path):
    img_stream =''
    with open(img_local_path,'rb') as im_f:
       img_stream =img_f.read()
       img_stream =base64.b64encode(img_stream).decode()
    return img_stream

def nvl(a,b):
    if a== None or a == '': return b
    else: return a
