pipeline {
    agent any 

    tools {
        // This assumes you've configured NodeJS installations in Jenkins global tools configuration
        nodejs 'node'  // 'node' is the name you gave to the Node.js installation in Jenkins
    }

    stages {
        stage('Checkout') {
            steps {
                // This checks out your code from the specified repository
                checkout scm
            }
        }

        stage('Install and Build') {
            steps {
                dir('frontend') {  // Change directory to 'frontend'
                    // Install dependencies and build
                    sh 'npm install'
                    sh 'npm run build'
                }
            }
        }
    }

post {
    success {
        echo 'Build was successful!'
    }
    failure {
        echo 'Build failed.'
    }
}
}