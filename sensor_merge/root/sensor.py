import cgi

from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext import db

#class TaskStatus:
#    def __init__(self):
#        self.TASK_READY = "READY"
#        self.TASK_RUNNING = "RUNNING"
#        self.setReady()
        
#    def setReady(self):
#        self.change(self.TASK_READY)
        
#    def setRunning(self):
#        self.change(self.TASK_RUNNING)
        
#    def change(self, st):
#        self.task_status = st

#    def get(self):
#        return self.task_status

#status = "READY"

class Guestbook(webapp.RequestHandler):
    def post(self):
        greeting = Greeting()

        if users.get_current_user():
            greeting.author = users.get_current_user()
            
        greeting.content = self.request.get('content')
        greeting.put()
#        application.status.setRunning()
#        global status
#        status = "RUNNING"
        self.redirect('/')
  
class StopCommand(webapp.RequestHandler):
    def post(self):
#        application.status.setReady() 
#        global status
#        status = "READY"
        self.redirect('/')
               
class Greeting(db.Model):
    author = db.UserProperty()
    content = db.StringProperty(multiline=True)
    date = db.DateTimeProperty(auto_now_add=True)
        
class MainPage(webapp.RequestHandler):
    def get(self):
        user = users.get_current_user()
        self.response.out.write('<html><body>')
        self.response.out.write('  <head>')
        self.response.out.write('    <link type="text/css" rel="stylesheet" href="/stylesheets/main.css" />')
        self.response.out.write('  </head>')
        self.response.out.write('<body>')  
  
        if user and user.nickname() == "wormfarm":
#            self.response.out.write('<b>Hello, ' + user.nickname()+'</b><br>Status:'+ application.status.get() +'<br><hr><br>')
            self.response.out.write('<b>Hello, ' + user.nickname()+'</b><br><hr><br>')
#            global status            
#            self.response.out.write('<b>Hello, ' + user.nickname()+'</b><br>Status:'+ status +'<br><hr><br>')
        else:
            self.redirect(users.create_login_url(self.request.uri))
                
        # Write the submission form and the footer of the page
        self.response.out.write("""
              
              <form action="/sign" method="post">
              <table>
                <tr>
                    <td>
                        Input filename:
                    </td>
                <td><input id="file_name" type="text" name="content"></td>
                <td><input type="submit" value="Sign Task to file" onclick="startTask();"></td>
              </form>
              
              <form action="/stop" method="post">
                <table>
                    <tr>
                        <td>
                            Please chek the latest log, and if running state press:
                        </td>
                        <td>
                            <input type="button" value="Stop Task" onclick="stopTask();">
                        </td>
                    </tr>
                </table>
              </form>
              <br>""")
              
        greetings = db.GqlQuery("SELECT * FROM Greeting ORDER BY date DESC LIMIT 10")

        for greeting in greetings:
            if greeting.author:
                self.response.out.write('<b>%s</b> created by <b>%s</b>:' % (greeting.date,greeting.author.nickname()))
            else:
                self.response.out.write('Anonimus create: ')
            self.response.out.write('<blockquote><table><tr>')

            self.response.out.write('<td><table><tr>')
            self.response.out.write('<td>Sensor Data file:</td>')
            self.response.out.write('<td><div></div></td>')
            self.response.out.write('<td><a href="http://interactivefishing.tv:8080/data/'+greeting.content+'_data.txt">'+greeting.content+'_data.txt</a></td>')

            self.response.out.write('</tr><tr>')
            self.response.out.write('<td><a>Sensor Log file: </a></td>')
            self.response.out.write('<td><div></div></td>')
            self.response.out.write('<td><a href="http://interactivefishing.tv:8080/data/'+greeting.content+'_log.txt">'+greeting.content+'_log.txt</a></td>')
            self.response.out.write('</tr><tr>')
            self.response.out.write('<td><a>Encoder Data file: </a></td>')
            self.response.out.write('<td><div></div></td>')
            self.response.out.write('<td><a href="http://interactivefishing.tv:8080/data/'+greeting.content+'_encoder_data.txt">'+greeting.content+'_encoder_data.txt</a></td>')
            self.response.out.write('</tr><tr>')
            self.response.out.write('<td><a>Encoder Log file: </a></td>')
            self.response.out.write('<td><div></div></td>')
            self.response.out.write('<td><a href="http://interactivefishing.tv:8080/data/'+greeting.content+'_encoder_log.txt">'+greeting.content+'_encoder_log.txt</a></td>')

            self.response.out.write('</tr><tr>')
            self.response.out.write('<td><a>XIMU Batt And Therm: </a></td>')
            self.response.out.write('<td><div></div></td>')
            self.response.out.write('<td><a href="http://interactivefishing.tv:8080/data/'+greeting.content+'_CalBattAndTherm.csv">'+greeting.content+'_CalBattAndTherm.csv</a></td>')

            self.response.out.write('</tr><tr>')
            self.response.out.write('<td><a>XIMU Inertial And Mag: </a></td>')
            self.response.out.write('<td><div></div></td>')
            self.response.out.write('<td><a href="http://interactivefishing.tv:8080/data/'+greeting.content+'_CalInertialAndMag.csv">'+greeting.content+'_CalInertialAndMag.csv</a></td>')

            self.response.out.write('</tr><tr>')
            self.response.out.write('<td><a>XIMU Date Time: </a></td>')
            self.response.out.write('<td><div></div></td>')
            self.response.out.write('<td><a href="http://interactivefishing.tv:8080/data/'+greeting.content+'_DateTime.csv">'+greeting.content+'_DateTime.csv</a></td>')

            self.response.out.write('</tr><tr>')
            self.response.out.write('<td><a>XIMU Euler Angles: </a></td>')
            self.response.out.write('<td><div></div></td>')
            self.response.out.write('<td><a href="http://interactivefishing.tv:8080/data/'+greeting.content+'_EulerAngles.csv">'+greeting.content+'_EulerAngles.csv</a></td>')

            self.response.out.write('</tr><tr>')
            self.response.out.write('<td><a>XIMU Quaternion: </a></td>')
            self.response.out.write('<td><div></div></td>')
            self.response.out.write('<td><a href="http://interactivefishing.tv:8080/data/'+greeting.content+'_Quaternion.csv">'+greeting.content+'_Quaternion.csv</a></td>')

            self.response.out.write('</tr><tr>')
            self.response.out.write('<td><a>XIMU Rotation Matrix: </a></td>')
            self.response.out.write('<td><div></div></td>')
            self.response.out.write('<td><a href="http://interactivefishing.tv:8080/data/'+greeting.content+'_RotationMatrix.csv">'+greeting.content+'_RotationMatrix.csv</a></td>')

            self.response.out.write('</tr><tr>')
            self.response.out.write('<td><a href="http://interactivefishing.tv:9001/'+greeting.content+'.css" target="_blank">Update Graphics</a></td>')
            self.response.out.write('<td><div></div></td>')
            self.response.out.write('<td></td>')


            self.response.out.write('</tr><tr>')
            self.response.out.write('<td><a href="http://interactivefishing.tv:9001/'+greeting.content+'.xml" target="_blank">Merge Update</a></td>')
            
            self.response.out.write('<td><div></div></td>')
            self.response.out.write('<td><a href="http://interactivefishing.tv:8080/data/'+greeting.content+'_merged.txt">'+greeting.content+'_merged.txt</a></td>')
            self.response.out.write('</tr></table></td>')

            self.response.out.write('<td><table><tr><td><b>Tension:</b></td></tr><tr><td><a href="/stylesheets/' + greeting.content + '_data.png"><img src="/stylesheets/' + greeting.content + '_data.png" width="200" height="150"></a></td></tr></table></td>')
            self.response.out.write('<td><table><tr><td><b>Delta Encoder:</b></td></tr><tr><td><a href="/stylesheets/' + greeting.content + '_delta_encoder_data.png"><img src="/stylesheets/' + greeting.content + '_delta_encoder_data.png" width="200" height="150"></a></td></tr></table></td>')
            self.response.out.write('<td><table><tr><td><b>Absolute Encoder:</b></td></tr><tr><td><a href="/stylesheets/' + greeting.content + '_value_encoder_data.png"><img src="/stylesheets/' + greeting.content + '_value_encoder_data.png" width="200" height="150"></a></td></tr></table></td>')                                    
            self.response.out.write('</tr></table>')

            self.response.out.write('<table>')

            self.response.out.write('<tr>')
            self.response.out.write('<td><b>Euler Angles</b></td>')
            self.response.out.write('<td><b>Accelerometer</b></td>')
            self.response.out.write('<td><b>Gyroscope</b></td>')
            self.response.out.write('<td><b>Magnetometer</b></td>')
            self.response.out.write('<td><b>Quaternion</b></td>')
            self.response.out.write('<td></td>')
            self.response.out.write('<td><b>RotationMatrix</b></td>')
            self.response.out.write('<td></td>')
            self.response.out.write('</tr>')

            self.response.out.write('<tr>')
            self.response.out.write('<td><table><tr><td>Pitch/Theta/Y:</td></tr><tr><td><a href="/stylesheets/' + greeting.content + '_ea_pty_data.png"><img src="/stylesheets/' + greeting.content + '_ea_pty_data.png" width="200" height="150"></a></td></tr></table></td>')
            self.response.out.write('<td><table><tr><td>x:</td></tr><tr><td><a href="/stylesheets/' + greeting.content + '_im_ax_data.png"><img src="/stylesheets/' + greeting.content + '_im_ax_data.png" width="200" height="150"></a></td></tr></table></td>')
            self.response.out.write('<td><table><tr><td>x:</td></tr><tr><td><a href="/stylesheets/' + greeting.content + '_im_gx_data.png"><img src="/stylesheets/' + greeting.content + '_im_gx_data.png" width="200" height="150"></a></td></tr></table></td>')
            self.response.out.write('<td><table><tr><td>x:</td></tr><tr><td><a href="/stylesheets/' + greeting.content + '_im_mx_data.png"><img src="/stylesheets/' + greeting.content + '_im_mx_data.png" width="200" height="150"></a></td></tr></table></td>')
            self.response.out.write('<td><table><tr><td>element 1:</td></tr><tr><td><a href="/stylesheets/' + greeting.content + '_q_e1_data.png"><img src="/stylesheets/' + greeting.content + '_q_e1_data.png" width="200" height="150"></a></td></tr></table></td>')
            self.response.out.write('<td><table><tr><td>element 11:</td></tr><tr><td><a href="/stylesheets/' + greeting.content + '_rm_e11_data.png"><img src="/stylesheets/' + greeting.content + '_rm_e11_data.png" width="200" height="150"></a></td></tr></table></td>')
            self.response.out.write('<td><table><tr><td>element 21:</td></tr><tr><td><a href="/stylesheets/' + greeting.content + '_rm_e21_data.png"><img src="/stylesheets/' + greeting.content + '_rm_e21_data.png" width="200" height="150"></a></td></tr></table></td>')
            self.response.out.write('<td><table><tr><td>element 31:</td></tr><tr><td><a href="/stylesheets/' + greeting.content + '_rm_e31_data.png"><img src="/stylesheets/' + greeting.content + '_rm_e31_data.png" width="200" height="150"></a></td></tr></table></td>')
            self.response.out.write('</tr>')

            self.response.out.write('<tr>')
            self.response.out.write('<td><table><tr><td>Roll/Phi/X:</td></tr><tr><td><a href="/stylesheets/' + greeting.content + '_ea_rpx_data.png"><img src="/stylesheets/' + greeting.content + '_ea_rpx_data.png" width="200" height="150"></a></td></tr></table></td>')
            self.response.out.write('<td><table><tr><td>y:</td></tr><tr><td><a href="/stylesheets/' + greeting.content + '_im_ay_data.png"><img src="/stylesheets/' + greeting.content + '_im_ay_data.png" width="200" height="150"></a></td></tr></table></td>')
            self.response.out.write('<td><table><tr><td>y:</td></tr><tr><td><a href="/stylesheets/' + greeting.content + '_im_gy_data.png"><img src="/stylesheets/' + greeting.content + '_im_gy_data.png" width="200" height="150"></a></td></tr></table></td>')
            self.response.out.write('<td><table><tr><td>y:</td></tr><tr><td><a href="/stylesheets/' + greeting.content + '_im_my_data.png"><img src="/stylesheets/' + greeting.content + '_im_my_data.png" width="200" height="150"></a></td></tr></table></td>')
            self.response.out.write('<td><table><tr><td>element 2:</td></tr><tr><td><a href="/stylesheets/' + greeting.content + '_q_e2_data.png"><img src="/stylesheets/' + greeting.content + '_q_e2_data.png" width="200" height="150"></a></td></tr></table></td>')
            self.response.out.write('<td><table><tr><td>element 12:</td></tr><tr><td><a href="/stylesheets/' + greeting.content + '_rm_e12_data.png"><img src="/stylesheets/' + greeting.content + '_rm_e12_data.png" width="200" height="150"></a></td></tr></table></td>')
            self.response.out.write('<td><table><tr><td>element 22:</td></tr><tr><td><a href="/stylesheets/' + greeting.content + '_rm_e22_data.png"><img src="/stylesheets/' + greeting.content + '_rm_e22_data.png" width="200" height="150"></a></td></tr></table></td>')
            self.response.out.write('<td><table><tr><td>element 32:</td></tr><tr><td><a href="/stylesheets/' + greeting.content + '_rm_e32_data.png"><img src="/stylesheets/' + greeting.content + '_rm_e32_data.png" width="200" height="150"></a></td></tr></table></td>')
            self.response.out.write('</tr>')

            self.response.out.write('<tr>')
            self.response.out.write('<td><table><tr><td>Yaw/Psi/Z:</td></tr><tr><td><a href="/stylesheets/' + greeting.content + '_ea_ypz_data.png"><img src="/stylesheets/' + greeting.content + '_ea_ypz_data.png" width="200" height="150"></a></td></tr></table></td>')
            self.response.out.write('<td><table><tr><td>z:</td></tr><tr><td><a href="/stylesheets/' + greeting.content + '_im_az_data.png"><img src="/stylesheets/' + greeting.content + '_im_az_data.png" width="200" height="150"></a></td></tr></table></td>')
            self.response.out.write('<td><table><tr><td>z:</td></tr><tr><td><a href="/stylesheets/' + greeting.content + '_im_gz_data.png"><img src="/stylesheets/' + greeting.content + '_im_gz_data.png" width="200" height="150"></a></td></tr></table></td>')
            self.response.out.write('<td><table><tr><td>z:</td></tr><tr><td><a href="/stylesheets/' + greeting.content + '_im_mz_data.png"><img src="/stylesheets/' + greeting.content + '_im_mz_data.png" width="200" height="150"></a></td></tr></table></td>')
            self.response.out.write('<td><table><tr><td>element 3:</td></tr><tr><td><a href="/stylesheets/' + greeting.content + '_q_e3_data.png"><img src="/stylesheets/' + greeting.content + '_q_e3_data.png" width="200" height="150"></a></td></tr></table></td>')
            self.response.out.write('<td><table><tr><td>element 13:</td></tr><tr><td><a href="/stylesheets/' + greeting.content + '_rm_e13_data.png"><img src="/stylesheets/' + greeting.content + '_rm_e13_data.png" width="200" height="150"></a></td></tr></table></td>')
            self.response.out.write('<td><table><tr><td>element 23:</td></tr><tr><td><a href="/stylesheets/' + greeting.content + '_rm_e23_data.png"><img src="/stylesheets/' + greeting.content + '_rm_e23_data.png" width="200" height="150"></a></td></tr></table></td>')
            self.response.out.write('<td><table><tr><td>element 33:</td></tr><tr><td><a href="/stylesheets/' + greeting.content + '_rm_e33_data.png"><img src="/stylesheets/' + greeting.content + '_rm_e33_data.png" width="200" height="150"></a></td></tr></table></td>')
            self.response.out.write('</tr>')

            self.response.out.write('<tr>')
            self.response.out.write('<td><table><tr><td><b>Battery:</b></td></tr><tr><td><a href="/stylesheets/' + greeting.content + '_b_data.png"><img src="/stylesheets/' + greeting.content + '_b_data.png" width="200" height="150"></a></td></tr></table></td>')
            self.response.out.write('<td><table><tr><td><b>Temperature:</b></td></tr><tr><td><a href="/stylesheets/' + greeting.content + '_th_data.png"><img src="/stylesheets/' + greeting.content + '_th_data.png" width="200" height="150"></a></td></tr></table></td>')
            self.response.out.write('<td></td>')
            self.response.out.write('<td></td>')
            self.response.out.write('<td><table><tr><td>element 4:</td></tr><tr><td><a href="/stylesheets/' + greeting.content + '_q_e4_data.png"><img src="/stylesheets/' + greeting.content + '_q_e4_data.png" width="200" height="150"></a></td></tr></table></td>')
            self.response.out.write('<td></td>')
            self.response.out.write('<td></td>')
            self.response.out.write('<td></td>')
            self.response.out.write('</tr>')

            self.response.out.write('</table>')

            self.response.out.write('</blockquote>')
        self.response.out.write("""
            <div id='mySocket'/>
        
        <script>
        
            stopTask = function() 
            {
                window.open('http://interactivefishing.tv:9001/stop.html','Stop command','width=300,height=100')
            }
                    
            startTask = function() 
            {
                var filename = document.getElementById("file_name").value;
   
                if (filename.length>0)
                {
                    window.open("http://interactivefishing.tv:9001/"+filename+".html",'Start command','width=300,height=100')
                }
            }

        </script>
                    
            </body>
          </html>""")

application = webapp.WSGIApplication(
                                     [('/', MainPage),
                                      ('/sign', Guestbook),
                                      ('/stop', StopCommand)],
                                     debug=True)
                                             
#application.status = TaskStatus()      


def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
