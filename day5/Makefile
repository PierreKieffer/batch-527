GCP_PROJECT_ID=ai-datalake
APP_NAME=webapp

all : build 

local-build : 
	@echo " ---- LOCAL BUILD ---- "
	@docker build -t ${APP_NAME} .

local-run : 
	@echo " ---- LOCAL RUN ---- "
	@docker run -d -p 8080:8080 --name ${APP_NAME} ${APP_NAME} 

build : 
	@echo " ---- BUILD ---- "
	@docker build -t eu.gcr.io/${GCP_PROJECT_ID}/${APP_NAME} .
	@gcloud docker -- push eu.gcr.io/${GCP_PROJECT_ID}/${APP_NAME}

cloud-run-deploy:
	@echo " ---- CLOUD RUN DEPLOY ---- "
	@gcloud run deploy --image eu.gcr.io/${GCP_PROJECT_ID}/${APP_NAME} --platform managed --cpu 1 --memory 2Gi --region "europe-west1" --port 8080

k8s-deploy:
	@echo " ---- K8S DEPLOY ---- "
	@cd k8s && ./deploy.sh 

