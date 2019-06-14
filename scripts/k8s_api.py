from kubernetes import client, config


class K8sNamespace:
    def __init__(self, kubeconfig, name):
        config.load_kube_config(kubeconfig)
        self.name = name
        self.core_v1 = client.CoreV1Api()

    def create_namespace_object(self):
        namespace_obj = client.V1Namespace(
            api_version='v1',
            kind='Namespace',
            metadata=client.V1ObjectMeta(name=self.name))
            # , spec=client.V1NamespaceSpec()
        return namespace_obj
    
    def create_namespace(self):
        if not self.is_exists_namespace():
            namespace_obj = self.create_namespace_object()
            data = self.core_v1.create_namespace(body=namespace_obj)
            print("Namespace '%s' created. data='%s'" % (self.name, str(data)))
        print("Namespace '%s' has already exists." % self.name)

    def delete_namespace(self):
        if self.is_exists_namespace():
            self.core_v1.delete_namespace(
                name=self.name,
                body=client.V1DeleteOptions(
                    api_version='meta/v1',
                    kind='DeleteOptions',
                    propagation_policy='Foreground',
                    grace_period_seconds=5))
            print("Namespace '%s' deleted." % self.name)
        else:
            print("Namespace '%s' is not exists." % self.name)

    def is_exists_namespace(self):
        temp = self.core_v1.list_namespace()
        namespaces = [ item.metadata.name for item in temp.items ]
        return self.name in namespaces


class K8sCronJob:
    def __init__(self, kubeconfig, namespace, name, annotations=None, args=None, image=None, image_pull_secrets=None, concurrency=None, schedule='', server_type='timer'):
        config.load_kube_config(kubeconfig)
        self.namespace = namespace
        self.cronjob_name = name   ## app + '--' + param
        self.container_name = name
        self.annotations = annotations  ## {module/app: vps_vps-timer, parameter: per1min}
        self.args = args  ## [java, -jar, /app.jar, per1min]
        self.image = image
        self.image_pull_secrets = image_pull_secrets
        self.schedule = schedule
        self.concurrency = concurrency
        self.server_type = server_type
        self.batch_v1beta1 = client.BatchV1beta1Api()

    def create_cronjob_object(self):
        container = client.V1Container(
            name=self.container_name,
            args=self.args,
            image=self.image,
            image_pull_policy='IfNotPresent',
            resources={"limits": {"cpu": "1", "memory": "512Mi"}},
            termination_message_policy='File',
            termination_message_path='/dev/termination-log',
            security_context={
                "allowPrivilegeEscalation": False,
                "capabilities": {},
                "privileged": False,
                "readOnlyRootFilesystem": False,
                "runAsNonRoot": False})

        job_template = client.V1beta1JobTemplateSpec(
            spec=client.V1JobSpec(
                backoff_limit=1,
                completions=1,
                parallelism=1,
                template=client.V1PodTemplateSpec(
                    metadata=client.V1ObjectMeta(annotations=self.annotations),
                    spec=client.V1PodSpec(
                        affinity={"nodeAffinity": {
                            "requiredDuringSchedulingIgnoredDuringExecution": {
                                "nodeSelectorTerms": [{
                                    "matchExpressions": [{ "key": "node-type", "operator": "In", "values": [self.server_type] }]
                                }]
                            }
                        }},
                        containers=[container],
                        dns_policy='ClusterFirst',
                        image_pull_secrets=[ {'name': self.image_pull_secrets} ],
                        restart_policy='Never',
                        scheduler_name='default-scheduler',
                        security_context={},
                        termination_grace_period_seconds=30)
                    ),
                )
            )

        spec = client.V1beta1CronJobSpec(
            concurrency_policy=self.concurrency,
            failed_jobs_history_limit=3,
            job_template=job_template,
            starting_deadline_seconds=300,
            schedule=self.schedule,
            successful_jobs_history_limit=3,
            suspend=False)

        cronjob = client.V1beta1CronJob(
            api_version='batch/v1beta1',
            kind='CronJob',
            metadata=client.V1ObjectMeta(
                labels={'cattle.io/creator': 'norman'},
                name=self.cronjob_name,
                namespace=self.namespace),
            spec=spec)

        return cronjob

    def create_cronjob(self):
        cronjob = self.create_cronjob_object()
        if not self.is_exists_cronjob():
            api_response = self.batch_v1beta1.create_namespaced_cron_job(
                namespace=self.namespace,
                body=cronjob)
            print("Cronjob '%s' created. status='%s'" % (self.cronjob_name, str(api_response.status)))
        else:
            self.update_cronjob(cronjob)

    def update_cronjob(self, cronjob):
        api_response = self.batch_v1beta1.replace_namespaced_cron_job(
            name=self.container_name,
            namespace=self.namespace,
            body=cronjob)
        print("Cronjob '%s' updated. status='%s'" % (self.cronjob_name, str(api_response.status)))

    def delete_cronjob(self):
        if self.is_exists_cronjob():
            api_response = self.batch_v1beta1.delete_namespaced_cron_job(
                name=self.container_name,
                namespace=self.namespace,
                body=client.V1DeleteOptions(
                    api_version='meta/v1',
                    kind='DeleteOptions',
                    propagation_policy='Foreground',
                    grace_period_seconds=5))
            print("Cronjob '%s' deleted. status='%s'" % (self.cronjob_name, str(api_response.status)))
        else:
            print("Cronjob '%s' is not exists." % self.cronjob_name)
    
    def is_exists_cronjob(self):
        temp = self.batch_v1beta1.list_namespaced_cron_job(namespace=self.namespace)
        cronjobs = [ item.metadata.name for item in temp.items ]
        return self.cronjob_name in cronjobs


class K8sDeployment:
    def __init__(self, kubeconfig, namespace, name, **kwargs):
        config.load_kube_config(kubeconfig)
        self.namespace = namespace
        self.deployment_name = name
        self.container_name = name
        self.env = kwargs.get('env')
        self.app_label = kwargs.get('app_label')
        self.workload_selector = kwargs.get('workload_selector')
        self._volumes = kwargs.get('volumes')
        self.image = kwargs.get('image')
        self.image_pull_secrets = kwargs.get('image_pull_secrets')
        self.container_port = kwargs.get('port')
        self.pod_num = kwargs.get('pod_num')
        self.limits = kwargs.get('limits')
        self.server_type = kwargs.get('server_type')
        self.volumes = None

        self.pod_labels = {
            "pod-type": self.server_type,
            "workload.user.cattle.io/workloadselector": self.workload_selector
        }
        if isinstance(self.app_label, dict):
            self.pod_labels.update(self.app_label)
        if isinstance(self._volumes, list):
            self.volumes = self._volumes

        self.apps_v1 = client.AppsV1Api()

    def create_deployment_object(self):
        filebeat_container = client.V1Container(
            name='filebeat',
            image='harbor.uletm.com/public/filebeat:6.3.2',
            image_pull_policy='Always',
            volume_mounts=[
                {"name": "filebeat-config", "mountPath": "/usr/share/filebeat/filebeat.yml", "subPath": "filebeat.yml"},
                {"name": "app-logs", "mountPath": "/data/logs/tomcat"} ],
            resources={"limits": {"cpu": "100m", "memory": "200Mi"}, "requests": {"cpu": "100m", "memory": "100Mi"}}
        )
        app_container = client.V1Container(
            env=self.env,
            name=self.container_name,
            image=self.image,
            image_pull_policy='Always',
            volume_mounts=[ {"name": "app-logs", "mountPath": "/data/logs/tomcat"} ],
            liveness_probe={
                "failureThreshold": 3,
                "initialDelaySeconds": 10,
                "periodSeconds": 2,
                "successThreshold": 1,
                "tcpSocket": {"port": self.container_port},
                "timeoutSeconds": 2
            },
            ports=[
                client.V1ContainerPort(container_port=self.container_port, name='8080tcp00', protocol='TCP')
            ],
            readiness_probe={
                "failureThreshold": 3,
                "initialDelaySeconds": 10,
                "periodSeconds": 2,
                "successThreshold": 2,
                "tcpSocket": {"port": self.container_port},
                "timeoutSeconds": 2
            },
            resources={"limits": self.limits, "requests": self.limits},
            security_context={
                "allowPrivilegeEscalation": False,
                "capabilities": {},
                "privileged": False,
                "procMount": "Default",
                "readOnlyRootFilesystem": False,
                "runAsNonRoot": False
            },
            stdin=True,
            termination_message_path='/dev/termination-log',
            termination_message_policy='File',
            tty=True)

        template = client.V1PodTemplateSpec(
            metadata=client.V1ObjectMeta(labels=self.pod_labels),
            spec=client.V1PodSpec(
                affinity={
                    "nodeAffinity": {
                        "requiredDuringSchedulingIgnoredDuringExecution": {
                            "nodeSelectorTerms": [{
                                "matchExpressions": [
                                    {"key": "node-type", "operator": "In", "values": [self.server_type]}
                                ]
                            }]
                        }
                    }
                },
                containers=[app_container, filebeat_container],
                dns_policy="ClusterFirst",
                image_pull_secrets=self.image_pull_secrets,
                priority=0,
                restart_policy="Always",
                scheduler_name="default-scheduler",
                security_context={},
                service_account="default",
                service_account_name="default",
                termination_grace_period_seconds=30,
                tolerations=[
                    {"effect": "NoExecute", "key": "node.kubernetes.io/not-ready", "operator": "Exists", "tolerationSeconds": 300},
                    {"effect": "NoExecute", "key": "node.kubernetes.io/unreachable", "operator": "Exists", "tolerationSeconds": 300}
                ],
                volumes=self.volumes
            ))

        spec = client.V1DeploymentSpec(
            progress_deadline_seconds=600,
            replicas=self.pod_num,
            revision_history_limit=10,
            selector={
                "matchLabels": {
                    "workload.user.cattle.io/workloadselector": self.workload_selector
                }
            },
            strategy={
                "rollingUpdate": {"maxSurge": 1, "maxUnavailable": 0},
                "type": "RollingUpdate"
            },
            template=template)

        deployment = client.V1Deployment(
            api_version="apps/v1",
            kind="Deployment",
            metadata=client.V1ObjectMeta(
                namespace=self.namespace,
                name=self.deployment_name,
                generation=10,
                labels={
                    "cattle.io/creator": "norman",
                    "workload.user.cattle.io/workloadselector": self.workload_selector
                }),
            spec=spec)

        return deployment

    def create_deployment(self):
        deployment = self.create_deployment_object()
        if not self.is_exists_deployment():
            api_response = self.apps_v1.create_namespaced_deployment(
                namespace=self.namespace,
                body=deployment)
            print("Deployment '%s' created. status='%s'" % (self.deployment_name, str(api_response.status)))
        else:
            self.update_deployment(deployment)

    def update_deployment(self, deployment):
        api_response = self.apps_v1.replace_namespaced_deployment(
            name=self.deployment_name,
            namespace=self.namespace,
            body=deployment)
        print("Deployment '%s' updated. status='%s'" % (self.deployment_name, str(api_response.status)))

    def delete_deployment(self):
        if self.is_exists_deployment():
            api_response = self.apps_v1.delete_namespaced_deployment(
                name=self.deployment_name,
                namespace=self.namespace,
                body=client.V1DeleteOptions(
                    api_version='meta/v1',
                    kind='DeleteOptions',
                    propagation_policy='Foreground',
                    grace_period_seconds=5))
            print("Deployment '%s' deleted. status='%s'" % (self.deployment_name, str(api_response.status)))
        else:
            print("Deployment '%s' is not exists." % self.deployment_name)

    def is_exists_deployment(self):
        temp = self.apps_v1.list_namespaced_deployment(namespace=self.namespace)
        deployments = [ item.metadata.name for item in temp.items ]
        return self.deployment_name in deployments


class K8sService:
    def __init__(self, kubeconfig, namespace, service_name, **kwargs):
        config.load_kube_config(kubeconfig)
        self.namespace = namespace
        self.service_name = service_name
        self.selector = kwargs.get('selector')
        self.ports = kwargs.get('ports')  # [{'protocol': 'TCP','port': 8080, 'target_port': 8080}]
        self.type = kwargs.get('type')
        self.core_v1 = client.CoreV1Api()

    def create_service_object(self):
        spec = client.V1ServiceSpec(
            selector=self.selector,
            ports=[
                {"protocol": p['protocol'], "port": p['port'], "targetPort": p['target_port']} for p in self.ports ],
            type=self.type)

        service = client.V1Service(
            api_version='v1',
            kind='Service',
            metadata=client.V1ObjectMeta(name=self.service_name),
            spec=spec)
        return service

    def create_service(self):
        service = self.create_service_object()
        if not self.is_exists_service():
            api_response = self.core_v1.create_namespaced_service(
                namespace=self.namespace,
                body=service)
            print("Service '%s' created. status='%s'" % (self.service_name, str(api_response.status)))
        else:
            self.update_service(service)

    def update_service(self, service):
        api_response = self.core_v1.patch_namespaced_service(
            name=self.service_name,
            namespace=self.namespace,
            body=service)
        print("Service '%s' updated. status='%s'" % (self.service_name, str(api_response.status)))

    def delete_service(self):
        if self.is_exists_service():
            api_response = self.core_v1.delete_namespaced_service(
                name=self.service_name,
                namespace=self.namespace,
                body=client.V1DeleteOptions(
                    api_version='meta/v1',
                    kind='DeleteOptions',
                    propagation_policy='Foreground',
                    grace_period_seconds=5))
            print("Service '%s' deleted. status='%s'" % (self.service_name, str(api_response.status)))
        else:
            print("Service '%s' is not exists." % self.service_name)

    def is_exists_service(self):
        temp = self.core_v1.list_namespaced_service(namespace=self.namespace)
        services = [ item.metadata.name for item in temp.items ]
        return self.service_name in services


class K8sIngress:
    def __init__(self, kubeconfig, namespace, ingress_name, **kwargs):
        config.load_kube_config(kubeconfig)
        self.namespace = namespace
        self.ingress_name = ingress_name
        self.domain = kwargs.get('domain')
        self.backends = kwargs.get('backends')  # [{'context': 'context', 'service_name': 'my-service', 'service_port': 80}]

        self.extensions_v1_beta1 = client.ExtensionsV1beta1Api()

    def create_ingress_object(self):
        spec = client.V1beta1IngressSpec(
            # backend=client.V1beta1IngressBackend(service_name=None, service_port=None),
            rules=[{
                "host": self.domain,
                "http": {
                    "paths": [{
                        "path": backend['context'],
                        "backend": {
                            "serviceName": backend['service_name'],
                            "servicePort": backend['service_port']
                        }
                    } for backend in self.backends ]
                }
            }],
            tls=None)

        ingress = client.V1beta1Ingress(
            api_version='extensions/v1beta1',
            kind='Ingress',
            metadata=client.V1ObjectMeta(name=self.ingress_name),
            spec=spec)
        return ingress
    
    def create_ingress(self):
        ingress = self.create_ingress_object()
        if not self.is_exists_ingress():
            api_response = self.extensions_v1_beta1.create_namespaced_ingress(
                namespace=self.namespace,
                body=ingress)
            print("Ingress '%s' created. status='%s'" % (self.ingress_name, str(api_response.status)))
        else:
            self.update_ingress(ingress)

    def update_ingress(self, ingress):
        api_response = self.extensions_v1_beta1.patch_namespaced_ingress(
            name=self.ingress_name,
            namespace=self.namespace,
            body=ingress)
        print("Ingress '%s' updated. status='%s'" % (self.ingress_name, str(api_response.status)))

    def delete_ingress(self):
        if self.is_exists_ingress():
            api_response = self.extensions_v1_beta1.delete_namespaced_ingress(
                name=self.ingress_name,
                namespace=self.namespace,
                body=client.V1DeleteOptions(
                    api_version='meta/v1',
                    kind='DeleteOptions',
                    propagation_policy='Foreground',
                    grace_period_seconds=5))
            print("Ingress '%s' deleted. status='%s'" % (self.ingress_name, str(api_response.status)))
        else:
            print("Ingress '%s' is not exists." % self.ingress_name)

    def is_exists_ingress(self):
        temp = self.extensions_v1_beta1.list_namespaced_ingress(namespace=self.namespace)
        ingresses = [ item.metadata.name for item in temp.items ]
        return self.ingress_name in ingresses


class K8sConfigMap:
    def __init__(self, kubeconfig, namespace, config_map_name, **kwargs):
        config.load_kube_config(kubeconfig)
        self.namespace = namespace
        self.config_map_name = config_map_name
        self.data = kwargs.get('data')

        self.core_v1 = client.CoreV1Api()

    def create_config_map_object(self):
        content = '''
        '''

        config_map = client.V1ConfigMap(
            api_version='v1',
            kind='ConfigMap',
            data=self.data,
            metadata=client.V1ObjectMeta(name=self.config_map_name))
        return config_map

    def create_config_map(self):
        config_map = self.create_config_map_object()
        if not self.is_exists_config_map():
            api_response = self.core_v1.create_namespaced_config_map(
                namespace=self.namespace,
                body=config_map)
            print("ConfigMap '%s' created. status='%s'" % (self.config_map_name, str(api_response)))
        else:
            self.update_config_map(config_map)

    def update_config_map(self, config_map):
        api_response = self.core_v1.patch_namespaced_config_map(
            name=self.config_map_name,
            namespace=self.namespace,
            body=config_map)
        print("ConfigMap '%s' updated. status='%s'" % (self.config_map_name, str(api_response)))

    def delete_config_map(self):
        if self.is_exists_config_map():
            api_response = self.core_v1.delete_namespaced_config_map(
                name=self.config_map_name,
                namespace=self.namespace,
                body=client.V1DeleteOptions(
                    api_version='meta/v1',
                    kind='DeleteOptions',
                    propagation_policy='Foreground',
                    grace_period_seconds=5))
            print("ConfigMap '%s' deleted. status='%s'" % (self.config_map_name, str(api_response)))
        else:
            print("ConfigMap '%s' is not exists." % self.config_map_name)

    def is_exists_config_map(self):
        temp = self.core_v1.list_namespaced_config_map(namespace=self.namespace)
        config_maps = [ item.metadata.name for item in temp.items ]
        return self.config_map_name in config_maps


class K8sHPA:
    def __init__(self, kubeconfig, namespace, hpa_name, **kwargs):
        config.load_kube_config(kubeconfig)
        self.namespace = namespace
        self.hpa_name = hpa_name

        self.target_api_version = kwargs.get('target_api_version')
        self.target_kind = kwargs.get('target_kind')
        self.target_name = kwargs.get('target_name')
        self.min_replicas = kwargs.get('min_replicas')
        self.max_replicas = kwargs.get('max_replicas')
        self.target_cpu_utilization_percentage = kwargs.get('target_cpu_utilization_percentage')

        self.autoscaling_v1 = client.AutoscalingV1Api()

    def create_hpa_object(self):
        spec = client.V1HorizontalPodAutoscalerSpec(
            min_replicas=self.min_replicas,
            max_replicas=self.max_replicas,
            target_cpu_utilization_percentage=self.target_cpu_utilization_percentage,
            scale_target_ref=client.V1CrossVersionObjectReference(
                api_version=self.target_api_version, kind=self.target_kind, name=self.target_name))
        hpa = client.V1HorizontalPodAutoscaler(
            api_version='autoscaling/v1',
            kind='HorizontalPodAutoscaler',
            metadata=client.V1ObjectMeta(name=self.hpa_name),
            spec=spec)
        return hpa

    def create_hpa(self):
        hpa = self.create_hpa_object()
        if not self.is_exists_hpa():
            api_response = self.autoscaling_v1.create_namespaced_horizontal_pod_autoscaler(
                namespace=self.namespace,
                body=hpa)
            print("HorizontalPodAutoscaler '%s' created. status='%s'" % (self.hpa_name, str(api_response.status)))
        else:
            self.update_hpa(hpa)

    def update_hpa(self, hpa):
        api_response = self.autoscaling_v1.patch_namespaced_horizontal_pod_autoscaler(
            name=self.hpa_name,
            namespace=self.namespace,
            body=hpa)
        print("HorizontalPodAutoscaler '%s' updated. status='%s'" % (self.hpa_name, str(api_response.status)))

    def delete_hpa(self):
        if self.is_exists_hpa():
            api_response = self.autoscaling_v1.delete_namespaced_horizontal_pod_autoscaler(
                name=self.hpa_name,
                namespace=self.namespace,
                body=client.V1DeleteOptions(
                    api_version='meta/v1',
                    kind='DeleteOptions',
                    propagation_policy='Foreground',
                    grace_period_seconds=5))
            print("HorizontalPodAutoscaler '%s' deleted. status='%s'" % (self.hpa_name, str(api_response.status)))
        else:
            print("HorizontalPodAutoscaler '%s' is not exists." % self.hpa_name)

    def is_exists_hpa(self):
        temp = self.autoscaling_v1.list_namespaced_horizontal_pod_autoscaler(namespace=self.namespace)
        hpas = [ item.metadata.name for item in temp.items ]
        return self.hpa_name in hpas


class K8sDaemonSet:
    def __init__(self, kubeconfig, namespace, daemon_set_name):
        config.load_kube_config(kubeconfig)
        self.namespace = namespace
        self.daemon_set_name = daemon_set_name
        self.container_name = daemon_set_name
        self.annotations = ''
        self.args = ''
        self.image = ''
        self.apps_v1 = client.AppsV1Api()

    def create_daemon_set_object(self):
        container = client.V1Container(
            name=self.container_name,
            args=self.args,
            image=self.image,
            image_pull_policy='IfNotPresent',
            ports=[client.V1ContainerPort(container_port=8080)],
            resources={"limits": {"cpu": "1", "memory": "512Mi"}},
            termination_message_policy='File',
            termination_message_path='/dev/termination-log',
            security_context={
                "allowPrivilegeEscalation": False,
                "capabilities": {},
                "privileged": False,
                "readOnlyRootFilesystem": False,
                "runAsNonRoot": False})

        template = client.V1PodTemplateSpec(
            metadata=client.V1ObjectMeta(annotations=self.annotations),
            spec=client.V1PodSpec(containers=[container])
        )

        # min_ready_seconds=None, revision_history_limit=None, selector=None, template=None, template_generation=None, update_strategy=None
        spec = client.V1DaemonSetSpec(
            revision_history_limit=3,
            template=template)

        daemon_set = client.V1DaemonSet(
            api_version='apps/v1',
            kind='DaemonSet',
            metadata=client.V1ObjectMeta(
                labels={},
                name=self.daemon_set_name,
                namespace=self.namespace),
            spec=spec)
        return daemon_set

    def create_daemon_set(self):
        daemon_set = self.create_daemon_set_object()
        if not self.is_exists_daemon_set():
            api_response = self.apps_v1.create_namespaced_daemon_set(
                namespace=self.namespace,
                body=daemon_set)
            print("DaemonSet '%s' created. status='%s'" % (self.daemon_set_name, str(api_response.status)))
        else:
            self.update_daemon_set(daemon_set)

    def update_daemon_set(self, daemon_set):
        api_response = self.apps_v1.patch_namespaced_daemon_set(
            name=self.daemon_set_name,
            namespace=self.namespace,
            body=daemon_set)
        print("DaemonSet '%s' updated. status='%s'" % (self.daemon_set_name, str(api_response.status)))

    def delete_daemon_set(self):
        if self.is_exists_daemon_set():
            api_response = self.apps_v1.delete_namespaced_daemon_set(
                name=self.daemon_set_name,
                namespace=self.namespace,
                body=client.V1DeleteOptions(
                    api_version='meta/v1',
                    kind='DeleteOptions',
                    propagation_policy='Foreground',
                    grace_period_seconds=5))
            print("DaemonSet '%s' deleted. status='%s'" % (self.daemon_set_name, str(api_response.status)))
        else:
            print("DaemonSet '%s' is not exists." % self.daemon_set_name)

    def is_exists_daemon_set(self):
        temp = self.apps_v1.list_namespaced_daemon_set(namespace=self.namespace)
        daemon_sets = [ item.metadata.name for item in temp.items ]
        return self.daemon_set_name in daemon_sets


kubeconfig = "/root/kubeconfig"
namespace = "default"

deployment_params = {
    "workload_selector": "k8s-example-nignx",
    "app_label": {"app": "example-nginx"},
    "image": "nginx",
    "port": 80,
    "pod_num": 2,
    "server_type": "nginx"
}
deployment_name = "nginx-deployment"

kd = K8sDeployment(kubeconfig, namespace, deployment_name, **deployment_params)
kd.create_deployment()
#kd.delete_deployment()



service_params = {
    "selector": {"app": "example-nginx"},
    "ports": [{'protocol': 'TCP','port': 80, 'target_port': 80}]
}
service_name = 'nginx-service'
#ks = K8sService(kubeconfig, namespace, service_name, **service_params)
#ks.create_service()
#ks.delete_service()


ingress_params = {
    "domain":"www.example.com",
    "backends": [{'context': '/', 'service_name': service_name, 'service_port': 80}]
}
ingress_name = 'nginx-ingress'
#ki = K8sIngress(kubeconfig, namespace, ingress_name, **ingress_params)
#ki.create_ingress()
#ki.delete_ingress()
