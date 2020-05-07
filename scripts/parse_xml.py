from xml.dom.minidom import parse
import xml.dom.minidom


ss = '''<?xml version='1.0' encoding='utf-8'?>
<Server port="8005" shutdown="SHUTDOWN">
    <Listener className="org.apache.catalina.startup.VersionLoggerListener" />
    <Listener className="org.apache.catalina.core.AprLifecycleListener" SSLEngine="on" />
    <Listener className="org.apache.catalina.core.JreMemoryLeakPreventionListener" />
    <Listener className="org.apache.catalina.mbeans.GlobalResourcesLifecycleListener" />
    <Listener className="org.apache.catalina.core.ThreadLocalLeakPreventionListener" />

    <GlobalNamingResources>
        <Resource name="UserDatabase" auth="Container"
                type="org.apache.catalina.UserDatabase"
                description="User database that can be updated and saved"
                factory="org.apache.catalina.users.MemoryUserDatabaseFactory"
                pathname="conf/tomcat-users.xml" />
    </GlobalNamingResources>

    <Service name="Catalina">
        <Connector port="8080" protocol="HTTP/1.1" connectionTimeout="60000" redirectPort="8443"
                maxHttpHeaderSize="8192" maxThreads="1024" acceptCount="512" enableLookups="false" URIEncoding="UTF-8" />
        <Connector port="8009" maxHttpHeaderSize="8192" maxThreads="1024" minSpareThreads="256"
                maxSpareThreads="1024" acceptCount="512" connectionTimeout="60000" enableLookups="false"
                compression="on" compressableMimeType="text/html,text/xml,text/plain,text/javascript,text/css"
                redirectPort="8443" protocol="AJP/1.3" URIEncoding="UTF-8"/>

        <Engine name="Catalina" defaultHost="localhost">

        <Realm className="org.apache.catalina.realm.LockOutRealm">
            <Realm className="org.apache.catalina.realm.UserDatabaseRealm" resourceName="UserDatabase"/>
        </Realm>

        <Host name="www.example.com" appBase="/data/application/example" unpackWARs="true" autoDeploy="true">
            <Alias>a.example.com</Alias>
            <Alias>b.example.com</Alias>
        </Host>
        </Engine>
    </Service>
</Server>
'''

def parse_xml():
    dom_tree = xml.dom.minidom.parseString(ss)
    collection = dom_tree.documentElement
    hosts = collection.getElementsByTagName('Host')

    for item in hosts:
        app_base = item.getAttribute('appBase')
        # print(app_base)

        if app_base == '/data/application/example':
            main_domain = item.getAttribute('name')
            print(main_domain)

            alias = item.getElementsByTagName('Alias')
            for a in alias:
                if a.childNodes:
                    _a = a.childNodes[0].data
                    print(_a)


if __name__ == "__main__":
    parse_xml()
