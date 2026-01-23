# Infra basics for this project

- Docker running locally 
- Localstack running through Docker locally 
- IaC setup through troposphere and YAML, just like on AWS with CloudFormation
- Scripts to automate things locally

# 21.1.2026

Automated IAM deployment to CloudFormation on localstack with a Bash script on root/lab_scripts/deploy_iam.sh

It works, this is the output on the terminal: 

$ ./deploy_iam.sh
Deploying IAM stack to LocalStack...
{
    "StackId": "arn:aws:cloudformation:us-east-1:000000000000:stack/local-iam-lab/ae9014e6-98d5-4dac-b0b7-2edd0386cc44"
}
Deployment command issued. Check stack status with:
aws --endpoint-url=http://localhost:4566 cloudformation describe-stacks --stack-name local-iam-lab
(.venv)

Changed the generate_templates.sh script content to include universal file naming instead of hard coded files and tested it locally to make sure it worked, here's the output on LocalStack: 

$ aws --endpoint-url=http://localhost:4566 cloudformation create-stack \
  --stack-name local-ec2-lab \
  --stack-name local-ec2-lab \
  --template-body file://yaml/ec2.yaml
{
    "StackId": "arn:aws:cloudformation:us-east-1:000000000000:stack/local-ec2-lab/ba691f41-77d1-45b9-b938-30775b8c8037"
}
(.venv)

- Changes for the future: 

This is fine as is but should be modified to one big coherent script that spins up all of your IAM, EC2 and other AWS resources by running one script with localstack running already. 

- Later on today: 

I created one big deploy.sh script for deployment and modified generate_templates.sh accordingly so that you can now run one big script on root and automate deployment of all AWS resources you want like IAM, EC2 or NGINX or whatever. Here's the correct output of the script to see that it works, it just needs a rewrite on the NGINX.py troposphere template: 

$ ./lab_scripts/deploy.sh
Using YAML directory: /c/Users/Matias.DESKTOP-2SBTD6B/Desktop/CloudGrindset2026/yaml
Deploying stack: ec2
Stack ec2 exists, deleting before redeploy...
Stack ec2 deleted
Creating stack: ec2
{
    "StackId": "arn:aws:cloudformation:us-east-1:000000000000:stack/ec2/a0c6acdc-c4d6-45e5-98cb-4c5f1ed1ba02"
}
Stack ec2 deployed
Deploying stack: iam
Creating stack: iam
{
    "StackId": "arn:aws:cloudformation:us-east-1:000000000000:stack/iam/2c880263-723b-4189-a375-6f354b31958b"
}
Stack iam deployed
Deploying stack: nginx
Stack nginx exists, deleting before redeploy...
Stack nginx deleted
Creating stack: nginx
{
    "StackId": "arn:aws:cloudformation:us-east-1:000000000000:stack/nginx/2505d1dc-0d20-4787-a0bd-3bb07b27a28f"
}

Waiter StackCreateComplete failed: Waiter encountered a terminal failure state: For expression "Stacks[].StackStatus" we matched expected path: "CREATE_FAILED" at least once
Stack nginx deployed
All YAML stacks deployed!
(.venv) 
{
    "StackId": "arn:aws:cloudformation:us-east-1:000000000000:stack/ec2/a0c6acdc-c4d6-45e5-98cb-4c5f1ed1ba02"
}
Stack ec2 deployed
Deploying stack: iam
Creating stack: iam
{
    "StackId": "arn:aws:cloudformation:us-east-1:000000000000:stack/iam/2c880263-723b-4189-a375-6f354b31958b"
}
Stack iam deployed
Deploying stack: nginx
Stack nginx exists, deleting before redeploy...
Stack nginx deleted
Creating stack: nginx
{
    "StackId": "arn:aws:cloudformation:us-east-1:000000000000:stack/nginx/2505d1dc-0d20-4787-a0bd-3bb07b27a28f"
}

Waiter StackCreateComplete failed: Waiter encountered a terminal failure state: For expression "Stacks[].StackStatus" we matched expected path: "CREATE_FAILED" at least once
Stack nginx deployed
All YAML stacks deployed!
(.venv)
Creating stack: iam
{
    "StackId": "arn:aws:cloudformation:us-east-1:000000000000:stack/iam/2c880263-723b-4189-a375-6f354b31958b"
}
Stack iam deployed
Deploying stack: nginx
Stack nginx exists, deleting before redeploy...
Stack nginx deleted
Creating stack: nginx
{
    "StackId": "arn:aws:cloudformation:us-east-1:000000000000:stack/nginx/2505d1dc-0d20-4787-a0bd-3bb07b27a28f"
}

Waiter StackCreateComplete failed: Waiter encountered a terminal failure state: For expression "Stacks[].StackStatus" we matched expected path: "CREATE_FAILED" at least once
Stack nginx deployed
All YAML stacks deployed!
(.venv)
}

Waiter StackCreateComplete failed: Waiter encountered a terminal failure state: For expression "Stacks[].StackStatus" we matched expected path: "CREATE_FAILED" at least once
Stack nginx deployed
All YAML stacks deployed!
(.venv)
(.venv)

- Edit: I found the root cause and will fix it tomorro with the template: 

$ aws --endpoint-url=http://localhost:4566 cloudformation describe-stack-events \
  --stack-name nginx
{
    "StackEvents": [
        {
            "StackId": "arn:aws:cloudformation:us-east-1:000000000000:stack/nginx/2505d1dc-0d20-4787-a0bd-3bb07b27a28f",
            "EventId": "963fb653-c9c8-4384-9107-257040982139",
            "StackName": "nginx",
            "LogicalResourceId": "nginx",
            "PhysicalResourceId": "arn:aws:cloudformation:us-east-1:000000000000:stack/nginx/2505d1dc-0d20-4787-a0bd-3bb07b27a28f",
            "ResourceType": "AWS::CloudFormation::Stack",
            "Timestamp": "2026-01-21T13:00:18.340239Z",
            "ResourceStatus": "CREATE_FAILED"
        },
        {
            "StackId": "arn:aws:cloudformation:us-east-1:000000000000:stack/nginx/2505d1dc-0d20-4787-a0bd-3bb07b27a28f",
            "EventId": "3e201a1d-c63f-452e-bd09-8e38183bedd7",
            "StackName": "nginx",
            "LogicalResourceId": "nginx",
            "PhysicalResourceId": "arn:aws:cloudformation:us-east-1:000000000000:stack/nginx/2505d1dc-0d20-4787-a0bd-3bb07b27a28f",
            "ResourceType": "AWS::CloudFormation::Stack",
            "Timestamp": "2026-01-21T13:00:18.340213Z",
            "ResourceStatus": "ROLLBACK_COMPLETE"
        },
        {
            "StackId": "arn:aws:cloudformation:us-east-1:000000000000:stack/nginx/2505d1dc-0d20-4787-a0bd-3bb07b27a28f",
            "EventId": "9f035218-6b5f-4ee3-aa4e-d27098c4af38",
            "StackName": "nginx",
            "LogicalResourceId": "nginx",
            "PhysicalResourceId": "arn:aws:cloudformation:us-east-1:000000000000:stack/nginx/2505d1dc-0d20-4787-a0bd-3bb07b27a28f",
            "ResourceType": "AWS::CloudFormation::Stack",
            "Timestamp": "2026-01-21T13:00:18.340075Z",
            "ResourceStatus": "CREATE_FAILED"
        },
        {
            "StackId": "arn:aws:cloudformation:us-east-1:000000000000:stack/nginx/2505d1dc-0d20-4787-a0bd-3bb07b27a28f",
            "EventId": "eafd20af-d4c2-4826-98c3-453bada5f44a",
            "StackName": "nginx",
            "LogicalResourceId": "WebServer",
            "ResourceType": "AWS::EC2::Instance",
            "Timestamp": "2026-01-21T13:00:18.340034Z",
            "ResourceStatus": "CREATE_FAILED",
            "ResourceStatusReason": "Resource provider operation failed: Invalid base64-encoded string: number of data characters (73) cannot be 1 more than a multiple of 4"
        },
        {
            "StackId": "arn:aws:cloudformation:us-east-1:000000000000:stack/nginx/2505d1dc-0d20-4787-a0bd-3bb07b27a28f",
            "EventId": "ea4ea0fe-8e95-4fc2-8218-d27477e48226",
            "StackName": "nginx",
            "LogicalResourceId": "WebServer",
            "ResourceType": "AWS::EC2::Instance",
            "Timestamp": "2026-01-21T13:00:18.339513Z",
            "ResourceStatus": "CREATE_IN_PROGRESS"
        },
        {
            "StackId": "arn:aws:cloudformation:us-east-1:000000000000:stack/nginx/2505d1dc-0d20-4787-a0bd-3bb07b27a28f",
            "EventId": "0e61db03-7440-4a63-8776-a6f57e4506d5",
            "StackName": "nginx",
            "LogicalResourceId": "WebSG",
            "PhysicalResourceId": "nginx-WebSG-7239af8b",
            "ResourceType": "AWS::EC2::SecurityGroup",
            "Timestamp": "2026-01-21T13:00:18.339244Z",
            "ResourceStatus": "CREATE_COMPLETE"
        },
        {
            "StackId": "arn:aws:cloudformation:us-east-1:000000000000:stack/nginx/2505d1dc-0d20-4787-a0bd-3bb07b27a28f",
            "EventId": "b25fa808-d468-4b6c-8516-b0e161b1d264",
            "StackName": "nginx",
            "LogicalResourceId": "WebSG",
            "ResourceType": "AWS::EC2::SecurityGroup",
            "Timestamp": "2026-01-21T13:00:18.324756Z",
            "ResourceStatus": "CREATE_IN_PROGRESS"
        },
        {
            "StackId": "arn:aws:cloudformation:us-east-1:000000000000:stack/nginx/2505d1dc-0d20-4787-a0bd-3bb07b27a28f",
            "EventId": "f2a4deb3-61a0-4f98-a4e5-306f9318fc5c",
            "StackName": "nginx",
            "LogicalResourceId": "nginx",
            "PhysicalResourceId": "arn:aws:cloudformation:us-east-1:000000000000:stack/nginx/2505d1dc-0d20-4787-a0bd-3bb07b27a28f",
            "ResourceType": "AWS::CloudFormation::Stack",
            "Timestamp": "2026-01-21T13:00:18.323812Z",
            "ResourceStatus": "CREATE_IN_PROGRESS"
        }
    ]
}
(.venv)


# 22.1.2026

- Maybe CI/CD for today, we'll see

Installed pylint locally and the plan is to integrate that to the codebase via CI/CD. The linter now runs locally and works.

- Got GitHub Actions CI/CD working and runnign the linter and deployment as expected. Everything works for now.

# 23.1.2026

Today I got an S3 bucket working with IaC and Localstack with my previous 2021/2024-era regional map website: 

$ aws --endpoint-url=http://localhost:4566 s3 sync ~/Desktop/regional-map-2024/ s3://regional-map-2024-website
upload: ..\regional-map-2024\.git\description to s3://regional-map-2024-website/.git/description
upload: ..\regional-map-2024\.git\hooks\applypatch-msg.sample to s3://regional-map-2024-website/.git/hooks/applypatch-msg.sample
upload: ..\regional-map-2024\.git\hooks\pre-merge-commit.sample to s3://regional-map-2024-website/.git/hooks/pre-merge-commit.sample
upload: ..\regional-map-2024\.git\hooks\pre-receive.sample to s3://regional-map-2024-website/.git/hooks/pre-receive.sample
upload: ..\regional-map-2024\.git\hooks\prepare-commit-msg.sample to s3://regional-map-2024-website/.git/hooks/prepare-commit-msg.sample
upload: ..\regional-map-2024\.git\hooks\push-to-checkout.sample to s3://regional-map-2024-website/.git/hooks/push-to-checkout.sample
upload: ..\regional-map-2024\.git\hooks\sendemail-validate.sample to s3://regional-map-2024-website/.git/hooks/sendemail-validate.sample
upload: ..\regional-map-2024\.git\hooks\update.sample to s3://regional-map-2024-website/.git/hooks/update.sample
upload: ..\regional-map-2024\.git\index to s3://regional-map-2024-website/.git/index  
upload: ..\regional-map-2024\.git\info\exclude to s3://regional-map-2024-website/.git/info/exclude
upload: ..\regional-map-2024\.git\logs\HEAD to s3://regional-map-2024-website/.git/logs/HEAD
upload: ..\regional-map-2024\.git\logs\refs\heads\main to s3://regional-map-2024-website/.git/logs/refs/heads/main
upload: ..\regional-map-2024\.git\logs\refs\remotes\origin\HEAD to s3://regional-map-2024-website/.git/logs/refs/remotes/origin/HEAD
upload: ..\regional-map-2024\.git\objects\pack\pack-1323993467bcb7829d24636170e66122a1bac58c.idx to s3://regional-map-2024-website/.git/objects/pack/pack-1323993467bcb7829d24636170e66122a1bac58c.idx
upload: ..\regional-map-2024\.git\objects\pack\pack-1323993467bcb7829d24636170e66122a1bac58c.pack to s3://regional-map-2024-website/.git/objects/pack/pack-1323993467bcb7829d24636170e66122a1bac58c.pack
upload: ..\regional-map-2024\.git\objects\pack\pack-1323993467bcb7829d24636170e66122a1bac58c.rev to s3://regional-map-2024-website/.git/objects/pack/pack-1323993467bcb7829d24636170e66122a1bac58c.rev
upload: ..\regional-map-2024\.git\packed-refs to s3://regional-map-2024-website/.git/packed-refs
upload: ..\regional-map-2024\.git\refs\heads\main to s3://regional-map-2024-website/.git/refs/heads/main
upload: ..\regional-map-2024\.git\refs\remotes\origin\HEAD to s3://regional-map-2024-website/.git/refs/remotes/origin/HEAD
upload: ..\regional-map-2024\Helsinki coordinates & postnumbers.txt to s3://regional-map-2024-website/Helsinki coordinates & postnumbers.txt
upload: ..\regional-map-2024\Licenses.md to s3://regional-map-2024-website/Licenses.md
upload: ..\regional-map-2024\Projekti.qgz to s3://regional-map-2024-website/Projekti.qgz
upload: ..\regional-map-2024\README.md to s3://regional-map-2024-website/README.md   
upload: ..\regional-map-2024\css\MarkerCluster.Default.css to s3://regional-map-2024-website/css/MarkerCluster.Default.css 
upload: ..\regional-map-2024\css\MarkerCluster.css to s3://regional-map-2024-website/css/MarkerCluster.css
upload: ..\regional-map-2024\css\espoo.css to s3://regional-map-2024-website/css/espoo.css
upload: ..\regional-map-2024\css\fontawesome-all.min.css to s3://regional-map-2024-website/css/fontawesome-all.min.css     
upload: ..\regional-map-2024\css\images\Helsinki.vaakuna.svg.png to s3://regional-map-2024-website/css/images/Helsinki.vaakuna.svg.png
upload: ..\regional-map-2024\css\images\cancel.png to s3://regional-map-2024-website/css/images/cancel.png
upload: ..\regional-map-2024\css\images\cancel_@2X.png to s3://regional-map-2024-website/css/images/cancel_@2X.png
upload: ..\regional-map-2024\css\images\check.png to s3://regional-map-2024-website/css/images/check.png
upload: ..\regional-map-2024\css\images\check_@2X.png to s3://regional-map-2024-website/css/images/check_@2X.png
upload: ..\regional-map-2024\css\images\focus.png to s3://regional-map-2024-website/css/images/focus.png
upload: ..\regional-map-2024\css\images\focus_@2X.png to s3://regional-map-2024-website/css/images/focus_@2X.png
upload: ..\regional-map-2024\css\images\layers-2x.png to s3://regional-map-2024-website/css/images/layers-2x.png
upload: ..\regional-map-2024\css\images\layers.png to s3://regional-map-2024-website/css/images/layers.png
upload: ..\regional-map-2024\css\images\marker-icon-2x.png to s3://regional-map-2024-website/css/images/marker-icon-2x.png
upload: ..\regional-map-2024\css\images\marker-icon.png to s3://regional-map-2024-website/css/images/marker-icon.png
upload: ..\regional-map-2024\css\images\marker-shadow.png to s3://regional-map-2024-website/css/images/marker-shadow.png   
upload: ..\regional-map-2024\css\images\measure-control.png to s3://regional-map-2024-website/css/images/measure-control.png
upload: ..\regional-map-2024\css\images\rulers.png to s3://regional-map-2024-website/css/images/rulers.png
upload: ..\regional-map-2024\css\images\rulers_@2X.png to s3://regional-map-2024-website/css/images/rulers_@2X.png
upload: ..\regional-map-2024\css\images\start.png to s3://regional-map-2024-website/css/images/start.png
upload: ..\regional-map-2024\css\images\start_@2X.png to s3://regional-map-2024-website/css/images/start_@2X.png
upload: ..\regional-map-2024\css\images\throbber.gif to s3://regional-map-2024-website/css/images/throbber.gif
upload: ..\regional-map-2024\css\images\trash.png to s3://regional-map-2024-website/css/images/trash.png
upload: ..\regional-map-2024\css\images\trash_@2X.png to s3://regional-map-2024-website/css/images/trash_@2X.png
upload: ..\regional-map-2024\css\jkl.css to s3://regional-map-2024-website/css/jkl.css
upload: ..\regional-map-2024\css\leaflet.css to s3://regional-map-2024-website/css/leaflet.css
upload: ..\regional-map-2024\css\main.css to s3://regional-map-2024-website/css/main.css
upload: ..\regional-map-2024\css\oulu.css to s3://regional-map-2024-website/css/oulu.css
upload: ..\regional-map-2024\css\pori.css to s3://regional-map-2024-website/css/pori.css
upload: ..\regional-map-2024\css\qgis2web.css to s3://regional-map-2024-website/css/qgis2web.css
upload: ..\regional-map-2024\css\tre.css to s3://regional-map-2024-website/css/tre.css
upload: ..\regional-map-2024\css\turku.css to s3://regional-map-2024-website/css/turku.css
upload: ..\regional-map-2024\css\vantaa.css to s3://regional-map-2024-website/css/vantaa.css
upload: ..\regional-map-2024\espoo.html to s3://regional-map-2024-website/espoo.html 
upload: ..\regional-map-2024\hki.html to s3://regional-map-2024-website/hki.html     
upload: ..\regional-map-2024\images\99167-Helsinki.jpg to s3://regional-map-2024-website/images/99167-Helsinki.jpg
upload: ..\regional-map-2024\images\Espoo.jpg to s3://regional-map-2024-website/images/Espoo.jpg
upload: ..\regional-map-2024\images\Finland.jpg to s3://regional-map-2024-website/images/Finland.jpg
upload: ..\regional-map-2024\images\HelsinkiBG.jpg to s3://regional-map-2024-website/images/HelsinkiBG.jpg
upload: ..\regional-map-2024\images\JKL.jpg to s3://regional-map-2024-website/images/JKL.jpg
upload: ..\regional-map-2024\images\Oulu.jpg to s3://regional-map-2024-website/images/Oulu.jpg
upload: ..\regional-map-2024\images\Pori.jpg to s3://regional-map-2024-website/images/Pori.jpg
upload: ..\regional-map-2024\images\Tampere.jpg to s3://regional-map-2024-website/images/Tampere.jpg
upload: ..\regional-map-2024\images\Turku.jpg to s3://regional-map-2024-website/images/Turku.jpg
upload: ..\regional-map-2024\images\Vantaa.jpg to s3://regional-map-2024-website/images/Vantaa.jpg
upload: ..\regional-map-2024\images\favicon.ico to s3://regional-map-2024-website/images/favicon.ico
upload: ..\regional-map-2024\images\hki.png to s3://regional-map-2024-website/images/hki.png
upload: ..\regional-map-2024\index.html to s3://regional-map-2024-website/index.html 
upload: ..\regional-map-2024\jkl.html to s3://regional-map-2024-website/jkl.html
upload: ..\regional-map-2024\js\Autolinker.min.js to s3://regional-map-2024-website/js/Autolinker.min.js
upload: ..\regional-map-2024\js\Leaflet.VectorGrid.js to s3://regional-map-2024-website/js/Leaflet.VectorGrid.js
upload: ..\regional-map-2024\js\OSMBuildings-Leaflet.js to s3://regional-map-2024-website/js/OSMBuildings-Leaflet.js
upload: ..\regional-map-2024\js\labelgun.min.js to s3://regional-map-2024-website/js/labelgun.min.js
upload: ..\regional-map-2024\js\labels.js to s3://regional-map-2024-website/js/labels.js
upload: ..\regional-map-2024\js\leaflet-hash.js to s3://regional-map-2024-website/js/leaflet-hash.js
upload: ..\regional-map-2024\js\leaflet-heat.js to s3://regional-map-2024-website/js/leaflet-heat.js
upload: ..\regional-map-2024\js\leaflet-svg-shape-markers.min.js to s3://regional-map-2024-website/js/leaflet-svg-shape-markers.min.js
upload: ..\regional-map-2024\js\leaflet-tilelayer-wmts.js to s3://regional-map-2024-website/js/leaflet-tilelayer-wmts.js   
upload: ..\regional-map-2024\js\leaflet.js to s3://regional-map-2024-website/js/leaflet.js
upload: ..\regional-map-2024\js\leaflet.js.map to s3://regional-map-2024-website/js/leaflet.js.map
upload: ..\regional-map-2024\js\leaflet.markercluster.js to s3://regional-map-2024-website/js/leaflet.markercluster.js
upload: ..\regional-map-2024\js\leaflet.pattern.js to s3://regional-map-2024-website/js/leaflet.pattern.js
upload: ..\regional-map-2024\js\leaflet.rotatedMarker.js to s3://regional-map-2024-website/js/leaflet.rotatedMarker.js     
upload: ..\regional-map-2024\js\leaflet.wms.js to s3://regional-map-2024-website/js/leaflet.wms.js
upload: ..\regional-map-2024\js\multi-style-layer.js to s3://regional-map-2024-website/js/multi-style-layer.js
upload: ..\regional-map-2024\js\pohina_legacy.js to s3://regional-map-2024-website/js/pohina_legacy.js
upload: ..\regional-map-2024\js\pohina_new.js to s3://regional-map-2024-website/js/pohina_new.js
upload: ..\regional-map-2024\js\pohina_vantaa.js to s3://regional-map-2024-website/js/pohina_vantaa.js
upload: ..\regional-map-2024\js\qgis2web_expressions.js to s3://regional-map-2024-website/js/qgis2web_expressions.js
upload: ..\regional-map-2024\js\rbush.min.js to s3://regional-map-2024-website/js/rbush.min.js
upload: ..\regional-map-2024\js\reset.js to s3://regional-map-2024-website/js/reset.js
upload: ..\regional-map-2024\legend\Pysakointipaikat_alue_5.png to s3://regional-map-2024-website/legend/Pysakointipaikat_alue_5.png
upload: ..\regional-map-2024\legend\Seutukartta_liikenne_juna_asema_1.png to s3://regional-map-2024-website/legend/Seutukartta_liikenne_juna_asema_1.png
upload: ..\regional-map-2024\legend\Seutukartta_liikenne_lentoasemat_2.png to s3://regional-map-2024-website/legend/Seutukartta_liikenne_lentoasemat_2.png
upload: ..\regional-map-2024\legend\Seutukartta_liikenne_metroasemat_3.png to s3://regional-map-2024-website/legend/Seutukartta_liikenne_metroasemat_3.png
upload: ..\regional-map-2024\legend\Seutukartta_liikenne_paatiet_4.png to s3://regional-map-2024-website/legend/Seutukartta_liikenne_paatiet_4.png
upload: ..\regional-map-2024\legend\Tyopaikkaruudukko_2018_6.png to s3://regional-map-2024-website/legend/Tyopaikkaruudukko_2018_6.png
upload: ..\regional-map-2024\oulu.html to s3://regional-map-2024-website/oulu.html
upload: ..\regional-map-2024\pori.html to s3://regional-map-2024-website/pori.html
upload: ..\regional-map-2024\tampere.html to s3://regional-map-2024-website/tampere.html
upload: ..\regional-map-2024\turku.html to s3://regional-map-2024-website/turku.html
upload: ..\regional-map-2024\.git\HEAD to s3://regional-map-2024-website/.git/HEAD
upload: ..\regional-map-2024\vantaa.html to s3://regional-map-2024-website/vantaa.html
upload: ..\regional-map-2024\webfonts\fa-solid-900.ttf to s3://regional-map-2024-website/webfonts/fa-solid-900.ttf
upload: ..\regional-map-2024\.git\config to s3://regional-map-2024-website/.git/config
upload: ..\regional-map-2024\webfonts\fa-solid-900.woff2 to s3://regional-map-2024-website/webfonts/fa-solid-900.woff2     
upload: ..\regional-map-2024\.git\hooks\commit-msg.sample to s3://regional-map-2024-website/.git/hooks/commit-msg.sample
upload: ..\regional-map-2024\.git\hooks\post-update.sample to s3://regional-map-2024-website/.git/hooks/post-update.sample 
upload: ..\regional-map-2024\.git\hooks\fsmonitor-watchman.sample to s3://regional-map-2024-website/.git/hooks/fsmonitor-watchman.sample
upload: ..\regional-map-2024\.git\hooks\pre-applypatch.sample to s3://regional-map-2024-website/.git/hooks/pre-applypatch.sample
upload: ..\regional-map-2024\.git\hooks\pre-push.sample to s3://regional-map-2024-website/.git/hooks/pre-push.sample       
upload: ..\regional-map-2024\.git\hooks\pre-commit.sample to s3://regional-map-2024-website/.git/hooks/pre-commit.sample   
upload: ..\regional-map-2024\.git\hooks\pre-rebase.sample to s3://regional-map-2024-website/.git/hooks/pre-rebase.sample
(.venv) 
rtta_liikenne_lentoasemat_2.png
upload: ..\regional-map-2024\legend\Seutukartta_liikenne_metroasemat_3.png to s3://regional-map-2024-website/legend/Seutukartta_liikenne_metroasemat_3.png
upload: ..\regional-map-2024\legend\Seutukartta_liikenne_paatiet_4.png to s3://regional-map-2024-website/legend/Seutukartta_liikenne_paatiet_4.png
upload: ..\regional-map-2024\legend\Tyopaikkaruudukko_2018_6.png to s3://regional-map-2024-website/legend/Tyopaikkaruudukko_2018_6.png
upload: ..\regional-map-2024\oulu.html to s3://regional-map-2024-website/oulu.html
upload: ..\regional-map-2024\pori.html to s3://regional-map-2024-website/pori.html
upload: ..\regional-map-2024\tampere.html to s3://regional-map-2024-website/tampere.html
upload: ..\regional-map-2024\turku.html to s3://regional-map-2024-website/turku.html
upload: ..\regional-map-2024\.git\HEAD to s3://regional-map-2024-website/.git/HEAD
upload: ..\regional-map-2024\vantaa.html to s3://regional-map-2024-website/vantaa.html
upload: ..\regional-map-2024\webfonts\fa-solid-900.ttf to s3://regional-map-2024-website/webfonts/fa-solid-900.ttf
upload: ..\regional-map-2024\.git\config to s3://regional-map-2024-website/.git/config
upload: ..\regional-map-2024\webfonts\fa-solid-900.woff2 to s3://regional-map-2024-website/webfonts/fa-solid-900.woff2     
upload: ..\regional-map-2024\.git\hooks\commit-msg.sample to s3://regional-map-2024-website/.git/hooks/commit-msg.sample   
upload: ..\regional-map-2024\.git\hooks\post-update.sample to s3://regional-map-2024-website/.git/hooks/post-update.sample 
upload: ..\regional-map-2024\.git\hooks\fsmonitor-watchman.sample to s3://regional-map-2024-website/.git/hooks/fsmonitor-watchman.sample
upload: ..\regional-map-2024\.git\hooks\pre-applypatch.sample to s3://regional-map-2024-website/.git/hooks/pre-applypatch.sample
upload: ..\regional-map-2024\.git\hooks\pre-push.sample to s3://regional-map-2024-website/.git/hooks/pre-push.sample       
upload: ..\regional-map-2024\.git\hooks\pre-commit.sample to s3://regional-map-2024-website/.git/hooks/pre-commit.sample   
upload: ..\regional-map-2024\.git\hooks\pre-rebase.sample to s3://regional-map-2024-website/.git/hooks/pre-rebase.sample   
(.venv)
_liikenne_paatiet_4.png
upload: ..\regional-map-2024\legend\Tyopaikkaruudukko_2018_6.png to s3://regional-map-2024-website/legend/Tyopaikkaruudukko_2018_6.png
upload: ..\regional-map-2024\oulu.html to s3://regional-map-2024-website/oulu.html
upload: ..\regional-map-2024\pori.html to s3://regional-map-2024-website/pori.html
upload: ..\regional-map-2024\tampere.html to s3://regional-map-2024-website/tampere.html
upload: ..\regional-map-2024\turku.html to s3://regional-map-2024-website/turku.html
upload: ..\regional-map-2024\.git\HEAD to s3://regional-map-2024-website/.git/HEAD
upload: ..\regional-map-2024\vantaa.html to s3://regional-map-2024-website/vantaa.html
upload: ..\regional-map-2024\webfonts\fa-solid-900.ttf to s3://regional-map-2024-website/webfonts/fa-solid-900.ttf
upload: ..\regional-map-2024\.git\config to s3://regional-map-2024-website/.git/config
upload: ..\regional-map-2024\webfonts\fa-solid-900.woff2 to s3://regional-map-2024-website/webfonts/fa-solid-900.woff2     
upload: ..\regional-map-2024\.git\hooks\commit-msg.sample to s3://regional-map-2024-website/.git/hooks/commit-msg.sample   
upload: ..\regional-map-2024\.git\hooks\post-update.sample to s3://regional-map-2024-website/.git/hooks/post-update.sample 
upload: ..\regional-map-2024\.git\hooks\fsmonitor-watchman.sample to s3://regional-map-2024-website/.git/hooks/fsmonitor-watchman.sample
upload: ..\regional-map-2024\.git\hooks\pre-applypatch.sample to s3://regional-map-2024-website/.git/hooks/pre-applypatch.sample
upload: ..\regional-map-2024\.git\hooks\pre-push.sample to s3://regional-map-2024-website/.git/hooks/pre-push.sample       
upload: ..\regional-map-2024\.git\hooks\pre-commit.sample to s3://regional-map-2024-website/.git/hooks/pre-commit.sample   
upload: ..\regional-map-2024\.git\hooks\pre-rebase.sample to s3://regional-map-2024-website/.git/hooks/pre-rebase.sample   
(.venv)
upload: ..\regional-map-2024\turku.html to s3://regional-map-2024-website/turku.html
upload: ..\regional-map-2024\.git\HEAD to s3://regional-map-2024-website/.git/HEAD
upload: ..\regional-map-2024\vantaa.html to s3://regional-map-2024-website/vantaa.html
upload: ..\regional-map-2024\webfonts\fa-solid-900.ttf to s3://regional-map-2024-website/webfonts/fa-solid-900.ttf
upload: ..\regional-map-2024\.git\config to s3://regional-map-2024-website/.git/config
upload: ..\regional-map-2024\webfonts\fa-solid-900.woff2 to s3://regional-map-2024-website/webfonts/fa-solid-900.woff2     
upload: ..\regional-map-2024\.git\hooks\commit-msg.sample to s3://regional-map-2024-website/.git/hooks/commit-msg.sample   
upload: ..\regional-map-2024\.git\hooks\post-update.sample to s3://regional-map-2024-website/.git/hooks/post-update.sample 
upload: ..\regional-map-2024\.git\hooks\fsmonitor-watchman.sample to s3://regional-map-2024-website/.git/hooks/fsmonitor-watchman.sample
upload: ..\regional-map-2024\.git\hooks\pre-applypatch.sample to s3://regional-map-2024-website/.git/hooks/pre-applypatch.sample
upload: ..\regional-map-2024\.git\hooks\pre-push.sample to s3://regional-map-2024-website/.git/hooks/pre-push.sample       
upload: ..\regional-map-2024\.git\hooks\pre-commit.sample to s3://regional-map-2024-website/.git/hooks/pre-commit.sample   
upload: ..\regional-map-2024\.git\hooks\pre-rebase.sample to s3://regional-map-2024-website/.git/hooks/pre-rebase.sample   
(.venv)
upload: ..\regional-map-2024\.git\hooks\post-update.sample to s3://regional-map-2024-website/.git/hooks/post-update.sample 
upload: ..\regional-map-2024\.git\hooks\fsmonitor-watchman.sample to s3://regional-map-2024-website/.git/hooks/fsmonitor-watchman.sample
upload: ..\regional-map-2024\.git\hooks\pre-applypatch.sample to s3://regional-map-2024-website/.git/hooks/pre-applypatch.sample
upload: ..\regional-map-2024\.git\hooks\pre-push.sample to s3://regional-map-2024-website/.git/hooks/pre-push.sample       
upload: ..\regional-map-2024\.git\hooks\pre-commit.sample to s3://regional-map-2024-website/.git/hooks/pre-commit.sample   
upload: ..\regional-map-2024\.git\hooks\pre-rebase.sample to s3://regional-map-2024-website/.git/hooks/pre-rebase.sample   
(.venv)
upload: ..\regional-map-2024\.git\hooks\pre-push.sample to s3://regional-map-2024-website/.git/hooks/pre-push.sample       
upload: ..\regional-map-2024\.git\hooks\pre-commit.sample to s3://regional-map-2024-website/.git/hooks/pre-commit.sample   
upload: ..\regional-map-2024\.git\hooks\pre-rebase.sample to s3://regional-map-2024-website/.git/hooks/pre-rebase.sample   
(.venv)
(.venv)

- I even got it to show on my browser through the S3 bucket on Localstack at: http://localhost:4566/regional-map-2024-website/index.html

- Added a fake dummy DynamoDB table to show localstack competence, deploying that now.
- Added Cloudwatch IaC as well.