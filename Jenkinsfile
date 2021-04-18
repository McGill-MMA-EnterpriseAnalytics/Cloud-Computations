Jenkinsfile (Declarative Pipeline)
pipeline{
    agent any
    stages {

        stage('build') {
            when {
                branch 'Docker'
            }
            steps {
                sh 'test_deploy.sh'

            }
        }

    }




}
