pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Build and Start Services') {
            steps {
                sh 'docker-compose up -d --build db web'
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

        stage('Unit tests') {
            steps {
                sh 'docker-compose exec -T web pytest tests/test_accounts_models.py tests/test_blog_models.py --ds=blogproject.settings --junitxml=unit-test-results.xml --cov=accounts --cov=blog --cov-report=xml'
            }
            post {
                always {
                    junit 'unit-test-results.xml'
                }
            }
        }

        stage('Integration tests') {
            steps {
                sh 'docker-compose exec -T web pytest tests/test_accounts_integration.py tests/test_blog_integration.py --ds=blogproject.settings --junitxml=integration-test-results.xml'
            }
            post {
                always {
                    junit 'integration-test-results.xml'
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
                sh 'sleep 10'
                sh 'curl -f http://localhost:8000 || (docker logs blog_smoke_test && exit 1)'
                sh 'docker stop blog_smoke_test'
            }
        }
    }

        stage('Integration tests') {
            steps {
                sh '. venv/bin/activate && pytest tests/test_accounts_integration.py tests/test_blog_integration.py --ds=blogproject.settings --junitxml=integration-test-results.xml'
            }
            post {
                always {
                    junit 'integration-test-results.xml'
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
                sh 'sleep 10'
                sh 'curl -f http://localhost:8000 || (docker logs blog_smoke_test && exit 1)'
                sh 'docker stop blog_smoke_test'
            }
        }
    }

    post {
        always {
            sh 'docker-compose down || true'
            cleanWs()
        }
    }
}
