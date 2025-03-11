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
                    // Kiểm tra và tạo virtual environment nếu chưa có
                    bat '''
                    if not exist venv (
                        python -m venv venv
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
                    python test_todolist.py
                    '''
                }
            }
        }
    }
}
