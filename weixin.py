#!/usr/bin/python
#_*_coding:utf-8 _*_

import requests,sys,json,os
requests.packages.urllib3.disable_warnings()
reload(sys)
sys.setdefaultencoding('utf-8')

#获取Token
def GetToken(Corpid,Secret):
    Url = "https://qyapi.weixin.qq.com/cgi-bin/gettoken"
    Data = {
        "corpid": Corpid,
        "corpsecret": Secret
    }
    r = requests.get(url=Url,params=Data,verify=False)
    Token = r.json()['access_token']
    return Token

#将获取到的趋势图，上传至企业微信临时素材，返回MediaId发送图文消息是使用
def GetImageUrl(Token,Path):
    Url = "https://qyapi.weixin.qq.com/cgi-bin/media/upload?access_token=%s&type=image" % Token
    data = {
        "media": open(Path,'r')
        }
    r = requests.post(url=Url,files=data)
    dict = r.json()
    return dict['media_id']

#文本消息    
def SendTextMessage(Token,User,Agentid,Content):
    Url = "https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token=%s" % Token
    Data = {
        "touser": User,                                 # 企业号中的用户帐号
        "msgtype": "text",                          # 消息类型
        "agentid": Agentid,                             # 企业号中的应用id
        "text": {
            "content": Content
        },
    "safe": "0"
    }
    r = requests.post(url=Url,data=json.dumps(Data),verify=False)
    return r.text


#卡片消息    
def SendCardMessage(Token,User,Agentid,Subject,Content):
    Url = "https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token=%s" % Token
    Data = {
        "touser": User,                                 # 企业号中的用户帐号
        "msgtype": "textcard",                          # 消息类型
        "agentid": Agentid,                             # 企业号中的应用id
        "textcard": {
            "title": Subject,
            "description": Content,
            "url": zabbix_host,          #点击详情后打开的页面
            "btntxt": "详情"
        },
    "safe": "0"
    }
    r = requests.post(url=Url,data=json.dumps(Data),verify=False)
    return r.text

#图文消息news
def SendnewsMessage(Token,User,Agentid,Subject,Content,History_url,Pic_url):
    Url = "https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token=%s" % Token
    Data = {
            "touser": User,                                 # 企业号中的用户帐号
            "msgtype": "news",                            # 消息类型
            "agentid": Agentid,                             # 企业号中的应用id
            "news": {
                    "articles": [
                    {
                            "title": Subject,
                            "description": Content,
                            "picurl": Pic_url,
                            "url": History_url,      #点击阅读原文后，打开趋势图大图，第一次需要登录
                    }
                    ]
            },
            "safe": "0"
    }
    headers = {'content-type': 'application/json'}
    data = json.dumps(Data,ensure_ascii=False).encode('utf-8')
    r = requests.post(url=Url,headers=headers,data=data)
    return r.text

#图文消息mpnews
def SendmpnewsMessage(Token,User,Agentid,Subject,Content,Media_id,history_url):
    Url = "https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token=%s" % Token
    Data = {
            "touser": User,                                 # 企业号中的用户帐号
            "msgtype": "mpnews",                            # 消息类型
            "agentid": Agentid,                             # 企业号中的应用id
            "mpnews": {
                    "articles": [
                    {
                            "title": Subject,
                            "thumb_media_id": Media_id,
                            "content": Content,
                            "content_source_url": history_url,      #点击阅读原文后，打开趋势图大图，第一次需要登录
                            "digest": Content,
                            "show_cover_pic": "1"
                    }
                    ]
            },
            "safe": "1"
    }
    headers = {'content-type': 'application/json'}
    data = json.dumps(Data,ensure_ascii=False).encode('utf-8')
    r = requests.post(url=Url,headers=headers,data=data)
    return r.text

#提交审批    
def SendApproval(Token,Creator_userid, Template_id, Project_name, Branch_name, Branch_commit, Image_name, Image_tag, Option_id, Platform_type):
    Url = "https://qyapi.weixin.qq.com/cgi-bin/oa/applyevent?access_token=%s" % Token
    Data = {
    	"creator_userid": Creator_userid,
    	"template_id": Template_id,
    	"use_template_approver": 1,
    	#"approver": [
    	#    {
    	#        "attr": 2,
    	#        "userid": ["WuJunJie","WangXiaoMing"]
    	#    },
    	#    {
    	#        "attr": 1,
    	#        "userid": ["LiuXiaoGang"]
    	#    }
    	#],
    	#"notifyer":[ "WuJunJie","WangXiaoMing" ],
    	#"notify_type" : 1,
    	"apply_data": {
    	    "contents":[
                {
    	            "control": "Text",
    	            "id": "Text-1581492024088",
    	            "title": [
    	                {
    	                    "text": "项目名称",
    	                    "lang": "zh_CN"
    	                }
    	            ],
    	            "value": {
    	                "text": Project_name.strip()
    	            }
    	        },
    	        {
    	           "control": "Selector",
    	           "id": "Selector-1581492416321",
    	           "title": [
    	               {
    	                   "text": "发布环境",
    	                   "lang": "zh_CN"
    	               }
    	           ],
    	           "value": {
                       "selector": {
	           	"type": "single",
                             "options": [
                                  {
                                      "key": Option_id 
                                  }
                              ]
	               }
    	           }
    	        },
    	        {
    	           "control": "Text",
    	           "id": "Text-1581492549750",
    	           "title": [
    	               {
    	                   "text": "代码分支",
    	                   "lang": "zh_CN"
    	               }
    	           ],
    	           "value": {
    	               "text": Branch_name.strip()
    	           }
    	        },
    	        {
    	           "control": "Text",
    	           "id": "Text-1581492572185",
    	           "title": [
    	               {
    	                   "text": "Commit",
    	                   "lang": "zh_CN"
    	               }
    	           ],
    	           "value": {
    	               "text": Branch_commit.strip()
    	           }
    	        },
    	        {
    	           "control": "Text",
    	           "id": "Text-1581492656710",
    	           "title": [
    	               {
    	                   "text": "镜像名称",
    	                   "lang": "zh_CN"
    	               }
    	           ],
    	           "value": {
    	               "text": Image_name.strip()
    	           }
    	        },
    	        {
    	           "control": "Text",
    	           "id": "Text-1581492696732",
    	           "title": [
    	               {
    	                   "text": "镜像tag",
    	                   "lang": "zh_CN"
    	               }
    	           ],
    	           "value": {
    	               "text": Image_tag.strip()
    	           }
    	        }
            ]
        }, 
         "summary_list": [
            {
                "summary_info": [{
                    "text": "项目名称: %s" %Project_name ,
                    "lang": "zh_CN"
                }]
            },
            {
                "summary_info": [{
                    "text": "发布环境: %s" %Platform_type ,
                    "lang": "zh_CN"
                }]
            },
            { "summary_info": [{
                    "text": "镜像名称: %s:%s" %(Image_name, Image_tag),
                    "lang": "zh_CN"
                }]
            }

        ]
    }

    r = requests.post(url=Url,data=json.dumps(Data),verify=False)
    return r.text

#获取审批模板详情    
def GetTemplateDetail(Token, Template_id):
    Url = "https://qyapi.weixin.qq.com/cgi-bin/oa/gettemplatedetail?access_token=%s" % Token
    Data = {
        "template_id": Template_id 
    }
    r = requests.post(url=Url,data=json.dumps(Data),verify=False)
    return r.text

if __name__ == "__main__":
    Corpid = os.getenv('PLUGIN_CORPID')
    Secret = os.getenv('PLUGIN_CORP_SECRET')
    Template_id = os.getenv('PLUGIN_TEMPLATE_ID')
    Project_name = os.getenv('DRONE_REPO')
    Repo_name = os.getenv('DRONE_REPO_NAME')
    Registry_name = os.getenv('PLUGIN_REGISTRY_NAME')
    Branch_name = os.getenv('DRONE_COMMIT_BRANCH')
    Branch_commit = os.getenv('DRONE_COMMIT_MESSAGE')
    Image_tag = os.getenv('PLUGIN_IMAGE_TAG')
    Creator_userid = os.getenv('PLUGIN_CREATOR_USERID')
    Token = GetToken(Corpid,Secret) 
    #根据分支名Branch_name,判断harbor项目
    map_harbortype = {
         "develop": "dev",
         "release": "test",
         "master": "prod"
     }
    Image_name = "%s/%s/%s" %(Registry_name, map_harbortype[Branch_name.strip()],Repo_name)
    #根据分支名Branch_name,判断发布环境
    map_platformtype = {
         "develop": "开发环境",
         "release": "测试环境",
         "master": "生产环境"
     }
    #根据分支名Branch_name,判断升级申请模板中发布环境的值
    #"key": "option-1581492416321"  #开发
    #"key": "option-1581492416322", #测试
    #"key": "option-1581492437334", #预生产
    #"key": "option-1581492441037", #生产
    map_optionid = {
         "develop": "option-1581492416321",
         "release": "option-1581492416322",
         "master": "option-1581492441037"
     }
    Option_id = map_optionid[Branch_name.strip()]
    Platform_type = map_platformtype[Branch_name.strip()]
    
    res = SendApproval(Token, Creator_userid, Template_id, Project_name, Branch_name, Branch_commit, Image_name, Image_tag, Option_id, Platform_type)
    res_dict = json.loads(res)
    if res_dict['errcode'] == 0:
        print 'Send Approval success!!!'
        #print 'Corpid: %s \nSecret: %s \nTemplate_id: %s \nProject_name: %s \nBranch_name: %s \nBranch_commit: %s \nImage_name: %s \nImage_tag: %s' %(Corpid, Secret, Template_id, Project_name, Branch_name, Branch_commit, Image_name, Image_tag)
        print 'Template_id: %s \nProject_name: %s \nBranch_name: %s \nBranch_commit: %s \nImage_name: %s \nImage_tag: %s' %(Template_id, Project_name, Branch_name, Branch_commit, Image_name, Image_tag)
    else:
        print 'Send Approval error!!! Detail: %s' %res_dict
        #print 'Corpid: %s \nSecret: %s \nTemplate_id: %s \nProject_name: %s \nBranch_name: %s \nBranch_commit: %s \nBranch_commit: %s\n Image_name: %s \nImage_tag: %s' %(Corpid, Secret, Template_id, Project_name, Branch_name, Branch_commit, Image_name, Image_tag)
        print 'Template_id: %s \nProject_name: %s \nBranch_name: %s \nBranch_commit: %s \nImage_name: %s \nImage_tag: %s' %(Template_id, Project_name, Branch_name, Branch_commit, Image_name, Image_tag)
        sys.exit(1)

