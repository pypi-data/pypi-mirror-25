
    def setSmtpServer(self, host, user=None, password=None, tls=False):
        self._server={'type': 'smtp', 'host': host, 'user': user, 'password': password, 'tls': tls}

    def setGmailSmtpServer(self, user, password):
        return self.setSmtpServer('smtp.gmail.com:587', user, password, True)

    def connect(self):
        try:
            server=smtplib.SMTP(self._server['host'])
            # server.set_debuglevel(1)

            if self._server['tls']:
                server.starttls()
            if self._server['user']:
                server.login(self._server['user'], self._server['password'])
            else:
                server.connect()
            self._server['instance']=server
            return True
        except:
            return False

    def disconnect(self):
        try:
            self._server['instance'].quit()
            self._server['instance']=None
        except:
            pass

    def getCID(self):
        self._cid+=1
        return 'cdi-{0}'.format(self._cid)

    def attach(self, obj):
        self._attach.append(obj)

    def createMessage(self, subject=None):
        self._message=MIMEMultipart(_subtype='related')
        if subject:
            self.setSubject(subject)

    def reset(self):
        self._recipients=[]
        self._attach=[]
        self._cid=0
        self._html=''
        self._style=''
        self.createMessage()

    def setSubject(self, subject):
        self._message['Subject']=subject

    def writeStyle(self, style):
        self._style = self._style + style

    def writeHtml(self, html):
        self._html = self._html + html

    def imageToHtmlSnipet(self, image, format='PNG'):
        if image:
            buf=StringIO.StringIO()
            image.save(buf, format)
            obj=MIMEImage(buf.getvalue(), image.format)
            buf.close()

            cid=self.getCID()
            obj.add_header('Content-Id', '<{0}>'.format(cid))
            self.attach(obj)
            return "<img src='cid:{0}'/>".format(cid)
        return ''

    def snapshotToHtmlSnipet(self, fpath, width=0):
        snap=self._rws.snapshooter()
        image=snap.shoot(fpath, width)
        return self.imageToHtmlSnipet(image)

    def addRecipient(self, address):
        if address:
            if type(address)==type(''):
                address=address.split(',')
            for a in address:
                if a not in self._recipients:
                    self._recipients.append(a)

    def getHtml(self):
        html="<head>"
        if self._style:
            html += "<style type='text/css'>" + self._style + "</style>"
        html += "</head>"
        html += "<body>" + self._html + "</body>"
        return html

    def send(self, recipients=None):
        result=False
        self.addRecipient(recipients)
        if self._recipients:
            if self.connect():
                originator='Digimat'
                self._message['From']=originator
                self._message['To']=', '.join(self._recipients)

                self._message.attach(MIMEText(self.getHtml(), _subtype='html'))

                if self._attach:
                    for obj in self._attach:
                        self._message.attach(obj)

                try:
                    self._server['instance'].sendmail(originator, self._recipients, self._message.as_string())
                    result=True
                except:
                    pass

                self.disconnect()

        return result

