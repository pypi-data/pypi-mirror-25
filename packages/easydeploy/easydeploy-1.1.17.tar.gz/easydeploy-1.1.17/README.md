# EasyDeploy
Configure any server and deploy any application to any server in minutes!


How it works?

This app uses all the power of Docker to deploy application using a single configuration file (easydeploy.yml), when you have the file with the server settings and the application
you need to depoloy, all you need to do is type a command.

Behind the hood this appication uses Fabric(Thanks Fabric, you're GREAT! ) to make the changes on host!

The server configured by the app uses Nginx as frontend webserver, working as reverse proxy to containers on host.

the ideia is with single file, you provision all infrastructure you need, configuring servers and deploying with easier any application.


Can I extend the features?

  Sure, usually at part of server settings, improving security settings, support for others operation systems and others.



How to use?

Install EasyDeploy

- pip install easydeploy or pip install git+https://github.com/rodrigorodriguescosta/django-like.git

Clone this respository, Example to use EasyDeploy with MySQL database, PhpMyAdmin and a static website

- git clone https://github.com/rodrigorodriguescosta/easydeploy-example-staticwebsite.git


Configure your server first

 1 - Make the changes in file easydeploy.yml to your server address or settings to use Vagrant on your host, of couse your server need to be accessible, even
     Vagrant VM

 2 - to configure your server, type ed config_server:MyServerGroupName


Deploy the applications

Deploy MySQL and PhpMyAdmin

 - type ed deploy:MyServerGroupName,mysql
 - That's it, MySQL and PhpMyAdmin was deployed to your server and you can access your app with the domain defined in file easydeploy.yml


Deploy static Website
 - type ed deploy:MyServerGroupName,MyWebSite
 - The same way above, you should access the static website on demain you defined








