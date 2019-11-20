import subprocess

def start_mongodb():
    try:
        subprocess.Popen(['c:\\Program Files\\MongoDB\\Server\\4.0\\bin\\mongod.exe',
                          '--dbpath','D:\\data\\db'])
        return {'message': 'MongoDB started successfully!'}
    except:
        return {'message': "Could not start MongoDB"}

def stop_mongodb():
    try:
        subprocess.Popen(['c:\\Program Files\\MongoDB\\Server\\4.0\\bin\\mongod.exe',
                          '--dbpath','D:\\data\\db'])
        return {'message': 'MongoDB started successfully!'}
    except:
        return {'message': "Could not start MongoDB"}