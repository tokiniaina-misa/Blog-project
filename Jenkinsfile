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
                sh 'docker-compose run --rm web bash -c "pip install -r requirements.txt"'
            }
        }
        stage('Build and Start Services') {
            steps {
                sh 'docker-compose up -d --build db web'
            }
        }
        stage('Wait for DB') {
            steps {
                // Utilisation d'une boucle pour attendre la base de données
                sh '''
                    until docker-compose exec -T db pg_isready -U bloguser -d blogdb; do
                        echo "Waiting for database to be ready..."
                        sleep 2
                    done
                '''
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
                // Exécution des tests et copie du fichier results.xml dans le workspace Jenkins
                sh 'docker-compose exec -T web bash -c "pytest tests/ --ds=blogproject.settings --junitxml=results.xml"'
                sh 'docker cp $(docker-compose ps -q web):/code/results.xml ./results.xml'
            }
            post {
                always {
                    // Le fichier results.xml est maintenant dans le workspace Jenkins
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
                // Utilisation d'une boucle pour attendre que l'application démarre
                sh '''
                    until curl -f http://localhost:8000; do
                        echo "Waiting for application to start..."
                        sleep 2
                    done
                '''
                sh 'docker stop blog_smoke_test'
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