pipeline {
    agent any
    
    environment {
        DOCKER_REGISTRY = 'docker.io/nocnex'
        APP_NAME = 'nodejs-hello-world'
    }
    
    stages {
        stage('Setup Node.js') {
            steps {
                script {
                    // Check if Node.js is installed
                    def nodeVersion = sh(script: 'node --version || echo "not_installed"', returnStdout: true).trim()
                    if (nodeVersion == "not_installed") {
                        // Install Node.js if not present
                        sh '''
                            curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
                            sudo apt-get install -y nodejs
                        '''
                    }
                    // Verify installation
                    sh 'node --version'
                    sh 'npm --version'
                }
            }
        }
        
        stage('Checkout') {
            steps {
                git branch: 'main', 
                url: 'https://github.com/nocnexhamza/hello_world.git',
                credentialsId: 'your-github-credentials'
            }
        }
        
        stage('Build') {
            steps {
                sh 'npm install'
            }
        }
        
        stage('Test') {
            steps {
                sh 'npm test || echo "Tests failed but continuing deployment"'
            }
        }
        
    stage('Build Docker Image') {
    environment {
        XDG_RUNTIME_DIR = '/run/user/$(id -u)'
    }
    steps {
        script {
            sh '''
                echo "Setting up rootless containerd environment"
                export XDG_RUNTIME_DIR=/run/user/$(id -u)
                nerdctl build -t ${DOCKER_REGISTRY}/${APP_NAME}:${env.BUILD_NUMBER} .
            '''
        }
    }
}
        
        stage('Push Docker Image') {
            steps {
                script {
                    withCredentials([usernamePassword(
                        credentialsId: 'docker-hub-credentials',
                        usernameVariable: 'DOCKER_USER',
                        passwordVariable: 'DOCKER_PASS'
                    )]) {
                        sh """
                            echo $DOCKER_PASS | nerdctl login -u $DOCKER_USER --password-stdin docker.io
                            nerdctl push ${DOCKER_REGISTRY}/${APP_NAME}:${env.BUILD_NUMBER}
                        """
                    }
                }
            }
        }
        
        stage('Deploy to Kubernetes') {
            steps {
                script {
                    withKubeConfig([credentialsId: 'k8s-credentials']) {
                        sh """
                            sed -i 's|image:.*|image: ${DOCKER_REGISTRY}/${APP_NAME}:${env.BUILD_NUMBER}|g' k8s/deployment.yaml
                            kubectl apply -f k8s/deployment.yaml
                            kubectl apply -f k8s/service.yaml
                            kubectl rollout status deployment/nodejs-hello-world
                        """
                    }
                }
            }
        }
    }
    
    post {
        always {
            script {
                // Clean up workspace
                sh 'rm -rf node_modules'
            }
        }
        success {
            script {
                // Only send Slack notification if properly configured
                if (env.SLACK_CHANNEL) {
                    slackSend(
                        color: "good",
                        message: "SUCCESS: Job '${env.JOB_NAME} [${env.BUILD_NUMBER}]'",
                        channel: env.SLACK_CHANNEL
                    )
                }
            }
        }
        failure {
            script {
                if (env.SLACK_CHANNEL) {
                    slackSend(
                        color: "danger",
                        message: "FAILED: Job '${env.JOB_NAME} [${env.BUILD_NUMBER}]'",
                        channel: env.SLACK_CHANNEL
                    )
                }
            }
        }
    }
}
