import cgi
import os
from django.utils import simplejson
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp import util
from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext import db
from appconf import app_host_name, os_div

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
        self.response.out.write("""
    <script type="text/javascript" src="./static/json2.js"></script>
    <script type="text/javascript">


    if( !window.XMLHttpRequest ) XMLHttpRequest = function()
    {
      try{ return new ActiveXObject("Msxml2.XMLHTTP.6.0") }catch(e){}
      try{ return new ActiveXObject("Msxml2.XMLHTTP.3.0") }catch(e){}
      try{ return new ActiveXObject("Msxml2.XMLHTTP") }catch(e){}
      try{ return new ActiveXObject("Microsoft.XMLHTTP") }catch(e){}
      throw new Error("Could not find an XMLHttpRequest alternative.")
    };

    function Request(function_name, opt_argv) {

      if (!opt_argv)
        opt_argv = new Array();

      var callback = null;
      var len = opt_argv.length;
      if (len > 0 && typeof opt_argv[len-1] == 'function') {
        callback = opt_argv[len-1];
        opt_argv.length--;
      }
      var async = (callback != null);

      var query = 'action=' + encodeURIComponent(function_name);
      for (var i = 0; i < opt_argv.length; i++) {
        var key = 'arg' + i;
        var val = JSON.stringify(opt_argv[i]);
        query += '&' + key + '=' + encodeURIComponent(val);
      }
      query += '&time=' + new Date().getTime(); // IE cache workaround

      var req = new XMLHttpRequest();
      req.open('GET', '/rpc?' + query, async);

      if (async) {
        req.onreadystatechange = function() {
          if(req.readyState == 4 && req.status == 200) {
            var response = null;
            try {
             response = JSON.parse(req.responseText);
            } catch (e) {
             response = req.responseText;
            }
            callback(response);
          }
        }
      }
      req.send(null);
    }
    function InstallFunction(obj, functionName) {
      obj[functionName] = function() { Request(functionName, arguments); }
    }

    </script>
    <script type="text/javascript">
    var server = {};

    InstallFunction(server, 'Add');

    // Handy "macro"
    function $(id){
      return document.getElementById(id);
    }

    // Client function that calls a server rpc and provides a callback
    function doAdd() {
    
      server.Add($('b_cnt').value, $('e_cnt').value, onAddSuccess);
      setTimeout("doAdd();",500);
    }

    // Callback for after a successful doAdd
    function onAddSuccess(response) {
      params = response.split(',');
      $('b_st').value = params[0];
      $('b_cnt').value = params[1];
      $('e_st').value = params[2];
      $('e_cnt').value = params[3];
      $('x_st').value = params[4];
      $('x_cnt').value = params[5];

    }

    </script>
    
    <script>
        window.onload = function(){doAdd(); };
    </script>
        """)        
        self.response.out.write('  </head>')
        self.response.out.write('<body>')  
  
        if user and user.nickname() == "wormfarm":
#            self.response.out.write('<b>Hello, ' + user.nickname()+'</b><br>Status:'+ application.status.get() +'<br><hr><br>')
            self.response.out.write('<b>Hello, ' + user.nickname()+'</b><br><hr><br>')
#            global status            
#            self.response.out.write('<b>Hello, ' + user.nickname()+'</b><br>Status:'+ status +'<br><hr><br>')
        else:
            self.redirect(users.create_login_url(self.request.uri))
        self.response.out.write("""
    <table>
        <tr>
        <td>
        <a>Current Status:</a>
        </td>
            <td>
                <a>Bridge status:</a>
                <input id="b_st" type="text" value="N/A" readonly="true" disabled="true"/>
            </td>
            
            <td>
                <a>Bridge Chunks Received:</a>
                <input id="b_cnt" type="text" value="0" readonly="true" disabled="true"/>
            </td>

            <td>
                <a>Encoder status:</a>
                <input id="e_st" type="text" value="N/A" readonly="true" disabled="true"/>
            </td>
            
            <td>
                <a>Encoder Chunks Received:</a>
                <input id="e_cnt" type="text" value="0" readonly="true" disabled="true"/>
            </td>

            <td>
                <a>xIMU status:</a>
                <input id="x_st" type="text" value="N/A" readonly="true" disabled="true"/>
            </td>
            
            <td>
                <a>xIMU Chunks Received:</a>
                <input id="x_cnt" type="text" value="0" readonly="true" disabled="true"/>
            </td>
                    
        </tr>
    </table>
""")                
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
              
        greetings = db.GqlQuery("SELECT * FROM Greeting ORDER BY date DESC LIMIT 50")

        for greeting in greetings:
            if greeting.author:
                self.response.out.write('<b>%s</b> created by <b>%s</b>:' % (greeting.date,greeting.author.nickname()))
            else:
                self.response.out.write('Anonimus create: ')
            self.response.out.write('<blockquote><table><tr>')

            self.response.out.write('<td><table><tr>')
            self.response.out.write('<td>Sensor Data file:</td>')
            self.response.out.write('<td><div></div></td>')
            self.response.out.write('<td><a href="'+ app_host_name +':8080/data/'+greeting.content+'_data.txt">'+greeting.content+'_data.txt</a></td>')

            self.response.out.write('</tr><tr>')
            self.response.out.write('<td><a>Sensor Log file: </a></td>')
            self.response.out.write('<td><div></div></td>')
            self.response.out.write('<td><a href="'+app_host_name+':8080/data/'+greeting.content+'_log.txt">'+greeting.content+'_log.txt</a></td>')
            self.response.out.write('</tr><tr>')
            self.response.out.write('<td><a>Encoder Data file: </a></td>')
            self.response.out.write('<td><div></div></td>')
            self.response.out.write('<td><a href="'+app_host_name+':8080/data/'+greeting.content+'_encoder_data.txt">'+greeting.content+'_encoder_data.txt</a></td>')
            self.response.out.write('</tr><tr>')
            self.response.out.write('<td><a>Encoder Log file: </a></td>')
            self.response.out.write('<td><div></div></td>')
            self.response.out.write('<td><a href="'+app_host_name+':8080/data/'+greeting.content+'_encoder_log.txt">'+greeting.content+'_encoder_log.txt</a></td>')

            self.response.out.write('</tr><tr>')
            self.response.out.write('<td><a>XIMU Batt And Therm: </a></td>')
            self.response.out.write('<td><div></div></td>')
            self.response.out.write('<td><a href="'+app_host_name+':8080/data/'+greeting.content+'_CalBattAndTherm.csv">'+greeting.content+'_CalBattAndTherm.csv</a></td>')

            self.response.out.write('</tr><tr>')
            self.response.out.write('<td><a>XIMU Inertial And Mag: </a></td>')
            self.response.out.write('<td><div></div></td>')
            self.response.out.write('<td><a href="'+app_host_name+':8080/data/'+greeting.content+'_CalInertialAndMag.csv">'+greeting.content+'_CalInertialAndMag.csv</a></td>')

            self.response.out.write('</tr><tr>')
            self.response.out.write('<td><a>XIMU Date Time: </a></td>')
            self.response.out.write('<td><div></div></td>')
            self.response.out.write('<td><a href="'+app_host_name+':8080/data/'+greeting.content+'_DateTime.csv">'+greeting.content+'_DateTime.csv</a></td>')

            self.response.out.write('</tr><tr>')
            self.response.out.write('<td><a>XIMU Euler Angles: </a></td>')
            self.response.out.write('<td><div></div></td>')
            self.response.out.write('<td><a href="'+app_host_name+':8080/data/'+greeting.content+'_EulerAngles.csv">'+greeting.content+'_EulerAngles.csv</a></td>')

            self.response.out.write('</tr><tr>')
            self.response.out.write('<td><a>XIMU Quaternion: </a></td>')
            self.response.out.write('<td><div></div></td>')
            self.response.out.write('<td><a href="'+app_host_name+':8080/data/'+greeting.content+'_Quaternion.csv">'+greeting.content+'_Quaternion.csv</a></td>')

            self.response.out.write('</tr><tr>')
            self.response.out.write('<td><a>XIMU Rotation Matrix: </a></td>')
            self.response.out.write('<td><div></div></td>')
            self.response.out.write('<td><a href="'+app_host_name+':8080/data/'+greeting.content+'_RotationMatrix.csv">'+greeting.content+'_RotationMatrix.csv</a></td>')

            self.response.out.write('</tr><tr>')
            self.response.out.write('<td><a href="'+app_host_name+':9001/'+greeting.content+'.css" target="_blank">Update Graphics</a></td>')
            self.response.out.write('<td><div></div></td>')
            self.response.out.write('<td></td>')


            self.response.out.write('</tr><tr>')
            self.response.out.write('<td><a href="'+app_host_name+':9001/'+greeting.content+'.xml" target="_blank">Merge Update</a></td>')
            
            self.response.out.write('<td><div></div></td>')
            self.response.out.write('<td><a href="'+app_host_name+':8080/data/'+greeting.content+'_merged.txt">'+greeting.content+'_merged.txt</a></td>')
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
                window.open('"""+app_host_name+""":9001/stop.html','Stop command','width=300,height=100')
            }
                    
            startTask = function() 
            {
                var filename = document.getElementById("file_name").value;
   
                if (filename.length>0)
                {
                    window.open(" """ +app_host_name+""":9001/"+filename+".html",'Start command','width=300,height=100')
                }
            }

        </script>
                    
            </body>
          </html>""")

class RPCHandler(webapp.RequestHandler):
    """ Allows the functions defined in the RPCMethods class to be RPCed."""
    def __init__(self):
        webapp.RequestHandler.__init__(self)
        self.methods = RPCMethods()

    def get(self):
        func = None

        action = self.request.get('action')
        if action:
            if action[0] == '_':
                self.error(403) # access denied
                return
            else:
                func = getattr(self.methods, action, None)

        if not func:
            self.error(404) # file not found
            return

        args = ()
        while True:
            key = 'arg%d' % len(args)
            val = self.request.get(key)
            if val:
                args += (simplejson.loads(val),)
            else:
                break
        result = func(*args)
        self.response.out.write(simplejson.dumps(result))


class RPCMethods:

    def Add(self, *args):
        
        try:
            f_b_cnt = open('proc' + os_div + 'b_cnt.txt','r')
            str_b_cnt = f_b_cnt.read()
            f_b_cnt.close()
        except IOError as e:
            print e
            str_b_cnt = "Unknown"
            
                        
        try:
            f_b_st = open('proc' + os_div + 'b_st.txt','r')
            str_b_st = f_b_st.read()
            f_b_st.close()
        except IOError as e1:
            print e1
            str_b_st = "Unknown"
           
        try:
            f_e_cnt = open('proc' + os_div + 'e_cnt.txt','r')
            str_e_cnt = f_e_cnt.read()
            f_e_cnt.close()
        except IOError as e2:
            print e2
            str_e_cnt = "Unknown"
            
        try:
            f_e_st = open('proc' + os_div + 'e_st.txt','r')
            str_e_st = f_e_st.read()
            f_e_st.close()
        except:
            str_e_st = "Unknown"

        try:
            f_x_cnt = open('proc' + os_div + 'x_cnt.txt','r')
            str_x_cnt = f_x_cnt.read()
            f_x_cnt.close()
        except:
            str_x_cnt = "Unknown"
            
        try:
            f_x_st = open('proc' + os_div + 'x_st.txt','r')
            str_x_st = f_x_st.read()
            f_x_st.close()
        except:
            str_x_st = "Unknown"  
                      
        return str_b_st + "," + str_b_cnt + "," + str_e_st + "," + str_e_cnt + "," + str_x_st + "," + str_x_cnt

application = webapp.WSGIApplication(
                                     [('/', MainPage),
                                      ('/sign', Guestbook),
                                      ('/rpc', RPCHandler),
                                      ('/stop', StopCommand)],
                                     debug=True)
                                             
#application.status = TaskStatus()      


def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
