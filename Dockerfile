FROM harbor.cechealth.cn/tools/python:2.7.16-alpine
ADD sonar_notify_wx.py /bin
RUN chmod +x /bin/sonar_notify_wx.py
#ENTRYPOINT ["python","/bin/weixin.py"]
#CMD ["python","/bin/weixin.py"]
CMD ["/bin/sh"]
