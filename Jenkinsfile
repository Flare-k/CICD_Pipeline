def gitUrl = 'https://github.com/Flare-k/CICD_Pipeline.git'
def S3_BUCKET = 'l25004-cicdtest-deploy'
def AWS_CREDENTIAL = 'AKIA5DFZMARIXOUAJMHU'
pipeline {
    agent any
    tools {nodejs "nodejs"}
    stages {
    	stage('git clone') {
    		steps {
    			script {
    				try {
    					git branch: "master", url: "${gitUrl}", credentialsId: "rokkyw" 
                        
    				} catch(Exception e) {
    					print(e)
    					cleanWs()
    				}
    			}
    		}
    	}
    	stage('npm install') {
    		steps {
    			script {
    				try {
    					dir("${WORKSPACE}/server") {
    						sh "npm install"
    					}
    				} catch(Exception e) {
    					print(e)
    					cleanWs()
    				}
    			}
    		}
    	}
    	stage('create appspec.yml') {
    		steps {
    			script {
    				try {
						dir("${WORKSPACE}/server") {
							sh """
								rm -rf scripts
								mkdir scripts
							"""

							sh """
								cd ${WORKSPACE}/server/scripts
								cat << EOF > start_server.sh
#!/bin/bash
cd ..
npm install
npm start &
EOF
"""
							
							sh """
								cd ${WORKSPACE}/server/scripts
								cat << EOF > stop_server.sh
#!/bin/bash
kill -9 `netstat -tnlp|2>/dev/null grep 80|gawk '{ print dollar7 }'|grep -o '[0-9]*'`
EOF
"""
							sh """
cat << EOF > appspec.yml
version: 0.0
os: linux
files:
  - source:  /
    destination: /
permissions:
  - object: /
    pattern: "**"
    owner: jenkins
    group: jenkins
hooks:
  ApplicationStart:
    - location: scripts/start_server.sh
      timeout: 60
      runas: root
  ApplicationStop:
    - location: scripts/stop_server.sh
      timeout: 60
      runas: root
EOF
"""
						}
    				} catch(Exception e) {
    					print(e)
    					cleanWs()
    				}
    			}
    		}
    	}
		stage('zip & upload') {
    		steps {
    			script {
    				try {
    					dir("${WORKSPACE}/server") {
    						sh "zip -r appspec.zip *"
    						withAWS(credentials:"${AWS_CREDENTIAL}", region: 'ap-northeast-2') {
        						sh "aws s3 cp appspec.zip s3://${S3_BUCKET}/${JOB_NAME}/appspec.zip"
    						}
    					}
    				} catch(Exception e) {
    					print(e)
    					cleanWs()
    				} finally {
    					cleanWs()
    				}
    			}
    		}
    	}
    	stage('deploy') {
    		steps {
    			script {
    				try {
						withAWS(credentials: "${AWS_CREDENTIAL}") {
							sh """
							  aws deploy create-deployment \
                              --application-name L25004-TEST-CICD \
                        	  --deployment-group-name L25004-Test \
                              --region ap-northeast-2 \
							  --s3-location bucket=${S3_BUCKET},bundleType=zip,key=${JOB_NAME}/appspec.zip \
							  --ignore-application-stop-failures
							"""
						}
					} catch(Exception e) {
						print(e)
						cleanWs()
					}
    			}
    		}
    	}
	}
}

def getShellCommandResult(cmd) {
    return sh(script: cmd, returnStdout: true).trim()
} 
 
