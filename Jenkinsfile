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

        stage('Install and Build') {
            steps {
                dir('frontend') {  // Change directory to 'frontend'
                    sh 'npm install'
                    sh '''
                        unset CI
                        npm run build
                    '''
                }
            }
        }

        stage('Deploy') {
            steps {
                sh 'cp -r frontend/build/* /home/tom/web/dev.gruevy.com/'
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
