pipeline {
    agent any  // This will use any available agent

    tools {
        nodejs 'node'  // 'node' is the name you gave to the Node.js installation in Jenkins
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }
        stage('Deploy Frontend') {
            steps {
                sh '/usr/bin/ssh ec2-user@3.149.252.158 "cd /home/ec2-user/ParkEZ/dev/frontend/"'
            }
        }

        stage('Deploy Backend') {
            steps {
                sh 'cp -r backend/* /home/ec2-user/ParkEZ/dev/backend/'
            }
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
