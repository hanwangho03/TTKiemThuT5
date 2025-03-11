pipeline {
    agent any

    stages {
        stage('Clone Repository') {
            steps {
                git branch: 'main', url: 'https://github.com/hanwangho03/TTKiemThuT5.git'
            }
        }

        stage('Set Up Environment') {
            steps {
                script {
                    bat 'python -m venv venv'
                    bat '. venv/bin/activate && pip install -r requirements.txt'
                }
            }
        }

        stage('Run Tests') {
            steps {
                script {
                    bat '. venv/bin/activate && python test_todolist.py'
                }
            }
        }
    }
}
