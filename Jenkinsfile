pipeline {
    agent any 

    stages{
        stage('SSH Install') {
                def remote = [:]
                remote.name = 'ec2-user'
                remote.host = '3.149.252.158'
                remote.user = 'ec2-user'
                remote.identityFile = credentials('ec2-user') 
                remote.allowAnyHosts = true

                sshCommand remote: remote, command: '''
                    cd /home/ec2-user/ParkEZ/dev/
                    git pull origin dev 
                '''
            }
        }

    post {
        success {
            echo 'Build and deployment were successful!'
        }
        failure {
            echo 'Build or deployment failed.'
        }
    }
}
}
