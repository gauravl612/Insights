#-------------------------------------------------------------------------------
# Copyright 2017 Cognizant Technology Solutions
# 
# Licensed under the Apache License, Version 2.0 (the "License"); you may not
# use this file except in compliance with the License.  You may obtain a copy
# of the License at
# 
#   http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.  See the
# License for the specific language governing permissions and limitations under
# the License.
#-------------------------------------------------------------------------------
'''
Created on Jun 16, 2016

@author: 146414
'''

import json
from com.cognizant.devops.platformagents.core.MessageQueueProvider import MessageFactory
from com.cognizant.devops.platformagents.core.CommunicationFacade import CommunicationFacade
from apscheduler.schedulers.blocking import BlockingScheduler
import sys
import os.path
import uuid
from datetime import datetime
from pytz import timezone
import logging.handlers

class BaseAgent(object):
       
    def __init__(self):
        try:
            self.setupAgent()
        except Exception as ex:
            self.publishHealthData(self.generateHealthData(ex=ex))
            logging.error(ex)
            self.logIndicator(self.SETUP_ERROR, self.config.get('isDebugAllowed', False))

    def setupAgent(self):
        self.resolveConfigPath()
        self.loadConfig()
        self.setupLogging()
        self.loadTrackingConfig()
        self.loadCommunicationFacade()
        self.initializeMQ()
        #self.configUpdateSubscriber()
        self.setupLocalCache()
        self.extractToolName()
        self.execute()
        self.scheduleAgent()
        
    
    def resolveConfigPath(self):
        filePresent = os.path.isfile('config.json')
        if filePresent:
            self.configFilePath = 'config.json'
            self.trackingFilePath = 'tracking.json'
            self.logFilePath = 'log_'+type(self).__name__+'.log'
        else:
            agentDir = os.path.dirname(sys.modules[self.__class__.__module__].__file__) + os.path.sep
            self.configFilePath = agentDir+'config.json'
            self.trackingFilePath = agentDir+'tracking.json'
            self.logFilePath = agentDir+'log_'+type(self).__name__+'.log'
        trackingFilePresent = os.path.isfile(self.trackingFilePath)
        if not trackingFilePresent:
            self.updateTrackingJson({})
    
    def setupLogging(self):
        loggingSetting = self.config.get('loggingSetting',{})
        maxBytes = loggingSetting.get('maxBytes', 1000 * 1000 * 5)
        backupCount = loggingSetting.get('backupCount', 1000)
        handler = logging.handlers.RotatingFileHandler(self.logFilePath, maxBytes=maxBytes, backupCount=backupCount)
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(filename)s - %(funcName)s - %(message)s')
        handler.setFormatter(formatter)
        logging.getLogger().setLevel(loggingSetting.get('logLevel',logging.WARN))
        logging.getLogger().addHandler(handler)
    
    def setupLocalCache(self):
        self.dataRoutingKey = str(self.config.get('publish').get('data'))
        self.healthRoutingKey = str(self.config.get('publish').get('health'))
        self.runSchedule = self.config.get('runSchedule', 30)
        self.insightsTimeZone = timezone('UTC')
        self.toolsTimeZone = timezone(self.config.get('toolsTimeZone'))
        self.epochStartDateTime = datetime(1970, 1, 1, tzinfo=self.insightsTimeZone)
        isEpochTime = self.config.get('isEpochTimeFormat', False)
        if not isEpochTime:
            self.dateTimeLength = len(self.epochStartDateTime.strftime(self.config.get('timeStampFormat', None)))        
    
    def extractToolName(self):
        tokens = self.dataRoutingKey.split('.')
        self.categoryName = tokens[0]
        self.toolName = tokens[1]
         
    
    def loadConfig(self):
        with open(self.configFilePath, 'r') as config_file:    
            self.config = json.load(config_file)
        if self.config == None:
            raise ValueError('BaseAgent: unable to load config JSON')
        
    def loadTrackingConfig(self):
        with open(self.trackingFilePath, 'r') as config_file:    
            self.tracking = json.load(config_file)
        if self.tracking == None:
            raise ValueError('BaseAgent: unable to load tracking JSON')
        
    def loadCommunicationFacade(self):
        communicationFacade = CommunicationFacade();
        config = self.config.get('communication',{})
        facadeType = config.get('type', None)
        sslVerify = config.get('sslVerify', True)
        self.responseType = config.get('responseType', 'JSON')
        self.communicationFacade = communicationFacade.getCommunicationFacade(facadeType, sslVerify, self.responseType)
        
    def initializeMQ(self):
        mqConfig = self.config.get('mqConfig', None)
        if mqConfig == None:
            raise ValueError('BaseAgent: unable to initialize MQ. mqConfig is not found')
        
        self.messageFactory = MessageFactory(mqConfig.get('user', None), 
                                             mqConfig.get('password', None), 
                                             mqConfig.get('host', None), 
                                             mqConfig.get('exchange', None))
        if self.messageFactory == None:
            raise ValueError('BaseAgent: unable to initialize MQ. messageFactory is Null')
        
    '''
    Subscribe for Engine Config Changes. Any changes to respective agent will be consumed and processed here.
    '''
    def configUpdateSubscriber(self):
        routingKey = self.config.get('subscribe').get('config')
        def callback(ch, method, properties, data):
            #Update the config file and cache.
            updatedConfig = json.loads(data)
            self.updateJsonFile(self.configFilePath, updatedConfig)
            self.config = updatedConfig 
            self.setupLocalCache()
            ch.basic_ack(delivery_tag = method.delivery_tag)
        self.messageFactory.subscribe(routingKey, callback)
                
    
    def publishToolsData(self, data):
        if data:
            self.addExecutionId(data, self.executionId)
            self.addTimeStampField(data)
            self.messageFactory.publish(self.dataRoutingKey, data, self.config.get('dataBatchSize', None))
            self.logIndicator(self.PUBLISH_START, self.config.get('isDebugAllowed', False))

    def publishHealthData(self, data):
        self.addExecutionId(data, self.executionId)
        self.messageFactory.publish(self.healthRoutingKey, data)
    
    def addTimeStampField(self, data):
        timeStampField = self.config.get('timeStampField')
        timeStampFormat = self.config.get('timeStampFormat')
        isEpochTime = self.config.get('isEpochTimeFormat', False)
        for d in data:
            eventTime = d.get(timeStampField, None)
            if eventTime != None:
                timeResponse = None
                if isEpochTime:
                    eventTime = str(eventTime)
                    eventTime = long(eventTime[:10])
                    timeResponse = self.getRemoteDateTime(datetime.fromtimestamp(eventTime))
                else:
                    eventTime = eventTime[:self.dateTimeLength]
                    timeResponse = self.getRemoteDateTime(datetime.strptime(eventTime, timeStampFormat))
                d['inSightsTime'] = timeResponse['epochTime']
                d['inSightsTimeX'] = timeResponse['time']
                d['toolName'] = self.toolName;
                d['categoryName'] = self.categoryName; 
                        
    def getRemoteDateTime(self, time):
        localDateTime = self.toolsTimeZone.localize(time)
        remoteDateTime = localDateTime.astimezone(self.insightsTimeZone)
        response = {
                    'epochTime' : (remoteDateTime - self.epochStartDateTime).total_seconds(),
                    'time' : remoteDateTime.strftime('%Y-%m-%dT%H:%M:%SZ')
                    }
        return response;
    
    def addExecutionId(self, data, executionId):
        for d in data:
            d['execId'] = executionId
    
    def updateTrackingJson(self, data):
        #Update the tracking json file and cache.
        self.updateJsonFile(self.trackingFilePath, data)
            
    def updateJsonFile(self, jsonFile, data):
        with open(jsonFile, 'w') as outfile:
            json.dump(data, outfile, indent=4, sort_keys=True)
            
    def getResponse(self, url, method, userName, password, data, authType='BASIC', reqHeaders=None, responseTupple=None):
        return self.communicationFacade.communicate(url, method, userName, password, data, authType, reqHeaders, responseTupple)
    
    def parseResponse(self, template, response, injectData={}):
        return self.communicationFacade.processResponse(template, response, injectData, self.config.get('useResponseTemplate',False))
    
    def getResponseTemplate(self):
        return self.config.get('responseTemplate', None)
    
    def generateHealthData(self, ex=None, systemFailure=False):
        data = []
        currentTime = self.getRemoteDateTime(datetime.now())
        health = { 'inSightsTimeX' : currentTime['time'], 'inSightsTime' : currentTime['epochTime'], 'executionTime' : self.executionTime}
        if systemFailure:
            health['status'] = 'failure'
            health['message'] = 'Agent is shutting down'
        elif ex != None:
            health['status'] = 'failure'
            health['message'] = 'Error occured: '+str(ex)
            logging.error(ex)
        else:
            health['status'] = 'success'
        data.append(health)
        return data
    
    def scheduleAgent(self):
        if not hasattr(self, 'scheduler'):
            scheduler = BlockingScheduler()
            self.scheduler = scheduler
            self.scheduledJob = scheduler.add_job(self.execute,'interval', seconds=60*self.runSchedule)
            try:
                scheduler.start()
            except (KeyboardInterrupt, SystemExit):
                self.publishHealthData(self.generateHealthData(systemFailure=True))
                
        else:
            scheduler = self.scheduler
            schedulerStatus = self.config.get('schedulerStatus', None)
            if schedulerStatus == 'UPDATE_SCHEDULE':
                self.scheduledJob.reschedule('interval', seconds=60*self.runSchedule)
            elif schedulerStatus == 'STOP':
                scheduler.shutdown()
            elif schedulerStatus == 'PAUSE':
                scheduler.pause()
            elif schedulerStatus == 'RESUME':
                scheduler.resume()
            elif schedulerStatus == 'RESTART':
                scheduler.start()
            else:
                pass
    
    def execute(self):
        try:
            self.logIndicator(self.EXECUTION_START, self.config.get('isDebugAllowed', False))
            self.executionId = str(uuid.uuid1())
            startTime = datetime.now()
            self.process()
            self.executionTime = int((datetime.now() - startTime).total_seconds() * 1000)
            self.publishHealthData(self.generateHealthData())
        except Exception as ex:
            self.publishHealthData(self.generateHealthData(ex=ex))
            logging.error(ex)
            self.logIndicator(self.EXECUTION_ERROR, self.config.get('isDebugAllowed', False))
        
    def process(self):
        '''
        Override process in Agent class
        '''
    
    EXECUTION_START = 1
    PUBLISH_START = 2
    EXECUTION_ERROR = 3
    SETUP_ERROR = 4
    
    def logIndicator(self, indicator, isDebugAllowed=False):
        if isDebugAllowed:
            if indicator == self.EXECUTION_START :
                sys.stdout.write('.')
            elif indicator == self.PUBLISH_START :
                sys.stdout.write('*')
            elif indicator == self.EXECUTION_ERROR :
                sys.stdout.write('|')
            elif indicator == self.SETUP_ERROR :
                sys.stdout.write('#')
