from lib.app import *
from lib.MyLogger import setup_custom_logger
from lib.user import AdminLogin

if __name__ == "__main__":
    global api
    global app
    api.add_resource(Slots, '/api/v1.0/slots')
    api.add_resource(Slot, '/api/v1.0/slots/<int:id>')
    api.add_resource(AdminLogin, '/login')

    Log = setup_custom_logger('parking')
    Log.info("Starting Parking app...")

    app.run(port=5000, debug=True)
