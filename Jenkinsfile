pipeline {
    agent any

    stages {
        stage('Clean Docker') {
            steps {
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
                withCredentials([file(credentialsId: 'env_file', variable: 'ENV_FILE')]) {
                    sh 'cp "$ENV_FILE" .env'
                }
            }
        }
        stage('Check requirements') {
            steps {
                sh 'docker-compose run --rm web bash -c "pip install pip-check && pip-check requirements.txt"'
            }
        }
        stage('Build and Start Services') {
            steps {
                sh 'docker-compose up -d --build db web'
            }
        }
        stage('Wait for DB') {
            steps {
                sh 'docker-compose exec -T db pg_isready -U bloguser -d blogdb'
            }
        }
        stage('Migrate DB') {
            steps {
                sh 'docker-compose exec -T web python manage.py migrate'
            }
        }
        stage('Collectstatic') {
            steps {
                sh 'docker-compose exec -T web python manage.py collectstatic --noinput'
            }
        }
        stage('Tests') {
            steps {
                sh 'docker-compose run --rm tests bash -c "pytest tests/ --ds=blogproject.settings --junitxml=results.xml"'
                sh 'docker cp $(docker-compose ps -q tests):/code/results.xml results.xml || true'
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
        stage('Docker smoke test') {
            steps {
                sh 'docker run -d --rm -p 8000:8000 --name blog_smoke_test blogproject:latest'
                sh 'curl -f http://localhost:8000 || (docker logs blog_smoke_test && exit 1)'
                sh 'docker stop blog_smoke_test'
            }
        }
    }

    post {
        always {
            sh 'rm .env || true'
            sh 'docker-compose down || true'
            cleanWs()
        }
    }
}
