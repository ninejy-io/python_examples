import jenkins
## pip install python-jenkins

cli = jenkins.Jenkins("https://jenkins.example.com/", username='admin', password='xxx')
new_cli = jenkins.Jenkins("https://new-jenkins.example.com/", username='admin', password='xxx')


def migrate_jenkins_view_job(view_name):
    if not new_cli.view_exists(view_name):
        view_config_xml = cli.get_view_config(view_name)
        # print(view_config_xml)
        new_cli.create_view(view_name, view_config_xml)

    jobs = cli._get_view_jobs(view_name)
    for job in jobs:
        name = job['name']

        if not new_cli.job_exists(name):
            config_xml = cli.get_job_config(name)
            # print(config_xml)
            new_cli.create_job(name, config_xml)


if __name__ == "__main__":
    migrate_jenkins_view_job(view_name)
