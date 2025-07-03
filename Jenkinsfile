pipeline {
    agent any
    
    environment {
        DOCKER_REGISTRY = 'docker.com'
        APP_NAME = 'nodejs-hello-world'
    }
    
    stages {
        stage('Checkout') {
            steps {
                git branch: 'main', url: 'https://github.com/nocnexhamza/hello_world.git'
            }
        }
        
        stage('Build') {
            steps {
                sh 'npm install'
            }
        }
        
        stage('Test') {
            steps {
                sh 'npm test'
            }
        }
        
        stage('Build Docker Image') {
            steps {
                script {
                    docker.build("${DOCKER_REGISTRY}/${APP_NAME}:${env.BUILD_NUMBER}")
                }
            }
        }
        
        stage('Push Docker Image') {
            steps {
                script {
                    docker.withRegistry('https://registry.hub.docker.com', 'dockerhublogin') {
                        docker.image("${DOCKER_REGISTRY}/${APP_NAME}:${env.BUILD_NUMBER}").push()
                        docker.image("${DOCKER_REGISTRY}/${APP_NAME}:${env.BUILD_NUMBER}").push('latest')
                    }
                }
            }
        }
        
        stage('Deploy to Kubernetes') {
            steps {
                script {
                    // Use kubeconfig credentials without sudo
                    withKubeConfig([credentialsId: 'k8s-credentials']) {
                        // Update image tag in deployment
                        sh """
                            sed -i 's|nocnex/nodejs-hello-world:latest|${DOCKER_REGISTRY}/${APP_NAME}:${env.BUILD_NUMBER}|g' k8s/deployment.yaml
                            kubectl apply -f k8s/deployment.yaml
                            kubectl apply -f k8s/service.yaml
                        """
                        
                        // Verify deployment
                        sh 'kubectl get pods -n default'
                        sh 'kubectl get svc -n default'
                    }
                }
            }
        }
    }
    
    post {
        success {
            slackSend(color: "good", message: "SUCCESS: Job '${env.JOB_NAME} [${env.BUILD_NUMBER}]'")
        }
        failure {
            slackSend(color: "danger", message: "FAILED: Job '${env.JOB_NAME} [${env.BUILD_NUMBER}]'")
        }
    }
}
