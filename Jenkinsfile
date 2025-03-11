pipeline {
    agent any

    environment {
        PYTHONIOENCODING = 'utf-8'  // Ép Python sử dụng UTF-8
    }

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
                    set PYTHONIOENCODING=utf-8
                    C:\\Users\\admin\\AppData\\Local\\Programs\\Python\\Python310\\python test_todolist.py
                    '''
                }
            }
        }
    }
}
