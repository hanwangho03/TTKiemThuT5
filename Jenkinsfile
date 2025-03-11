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
                    bat '''
                    if not exist venv (
                        C:\\Users\\admin\\AppData\\Local\\Programs\\Python\\Python310\\python -m venv venv
                    )
                    '''
                }
            }
        }

        stage('Run Tests') {
            steps {
                script {
                    bat '''
                    call venv\\Scripts\\activate
                    C:\\Users\\admin\\AppData\\Local\\Programs\\Python\\Python310\\python test_todolist.py
                    '''
                }
            }
        }
    }
}
