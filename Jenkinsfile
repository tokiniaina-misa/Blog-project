pipeline {
    agent any

    stages {
        stage('Clean Docker') {
            steps {
                sh 'docker stop $(docker ps -aq) || true'
                sh 'docker rm $(docker ps -aq) || true'
                sh 'docker-compose down -v --remove-orphans || true'
                sh 'docker system prune -af --volumes || true'
            }
        }
        
        stage('Checkout') {
            steps {
                checkout scm
            }
        }
        
        stage('Inject .env from Jenkins Credentials') {
            steps {
                withCredentials([file(credentialsId: '.env', variable: 'ENV_FILE')]) {
                    sh 'cp "$ENV_FILE" .env'
                }
            }
        }
        
        stage('Start Docker Services') {
            steps {
                sh 'docker-compose up -d db'
            }
        }
        
        stage('Wait for DB') {
            steps {
                script {
                    def maxAttempts = 30
                    def attempt = 0
                    def dbReady = false
                    
                    while (attempt < maxAttempts && !dbReady) {
                        try {
                            // Utiliser docker-compose exec pour vérifier la base de données
                            sh 'docker-compose exec -T db pg_isready -U bloguser -d blogdb'
                            dbReady = true
                            echo "Database is ready!"
                        } catch (Exception e) {
                            attempt++
                            echo "Waiting for database to be ready... (attempt ${attempt}/${maxAttempts})"
                            sleep(2)
                        }
                    }
                    
                    if (!dbReady) {
                        error("Database did not become ready after ${maxAttempts} attempts")
                    }
                }
            }
        }
        
        stage('Install dependencies') {
            steps {
                sh '''
                    python3 -m venv venv
                    . venv/bin/activate
                    pip install --upgrade pip
                    pip install -r requirements.txt
                '''
            }
        }
        
        stage('Run migrations') {
            steps {
                sh '. venv/bin/activate && python manage.py migrate'
            }
        }
        
        stage('Collect static files') {
            steps {
                sh '. venv/bin/activate && python manage.py collectstatic --noinput'
            }
        }
        
        stage('Run tests') {
            steps {
                sh '. venv/bin/activate && pytest tests/ --ds=blogproject.settings --junitxml=results.xml'
            }
            post {
                always {
                    junit 'results.xml'
                }
            }
        }
        
        stage('Build Docker image') {
            steps {
                sh 'docker build -t blogproject:latest .'
            }
        }
        
        stage('Docker curl test') {
            steps {
                sh 'docker run -d --rm -p 8000:8000 --name blog_curl_test blogproject:latest'
                sh 'sleep 5' // Attendre que l'application démarre
                sh 'curl -f http://localhost:8000/ || curl -f http://localhost:8000/accounts/profile/ || (docker logs blog_curl_test && exit 1)'
                sh 'docker stop blog_curl_test'
            }
        }
    }

    post {
        always {
            sh 'rm -f .env || true'
            sh 'docker-compose down || true'
            cleanWs()
        }
    }
}