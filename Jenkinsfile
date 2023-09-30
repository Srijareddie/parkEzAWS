pipeline {
    agent any 

    steps {
        script {
            def remote = [:]
            remote.name = 'your-ec2-instance'
            remote.host = 'your-ec2-instance-ip'
            remote.user = 'ec2-user'
            remote.identityFile = credentials('your-jenkins-ssh-credentials') 
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
