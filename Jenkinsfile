pipeline {
    agent any

    stages {
        stage('Clone Repository') {
            steps {
                git branch: 'main', url: 'https://github.com/hanwangho03/TTKiemThuT5.git'
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
