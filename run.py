from blogREST import server
from waitress import serve
import os
if __name__ == '__main__':
    if os.getenv('Flask_Env') =='production':
        serve(server.app, host='0.0.0.0', port=4000)
    else:
        server.run()