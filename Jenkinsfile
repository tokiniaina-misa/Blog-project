pipeline {
    agent any

    stages {
        stage('Clean Docker') {
            steps {
                // Arrêt et suppression de tous les conteneurs Docker pour éviter tout conflit
                sh 'docker stop $(docker ps -aq) || true'
                sh 'docker rm $(docker ps -aq) || true'
                sh 'docker-compose down -v || true'
                sh 'docker system prune -af || true'
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
        stage('Wait for DB') {
            steps {
                sh '''
                    for i in {1..10}; do
                        pg_isready -h localhost -U bloguser -d blogdb && break
                        echo "Waiting for database to be ready..."
                        sleep 2
                    done
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
                sh 'curl -f http://localhost:8000/accounts/profile/ || (docker logs blog_curl_test && exit 1)'
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