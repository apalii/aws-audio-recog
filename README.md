# aws-audio-recog

Serverless audio recognition task

## Resources
<img width="834" alt="image" src="https://github.com/apalii/aws-audio-recog/assets/8919200/8a95e783-e137-4eba-bf70-4a12cc1270f8">
<img width="624" alt="image" src="https://github.com/apalii/aws-audio-recog/assets/8919200/547d883e-1f45-41c5-aa10-6012018fd843">
![image](https://github.com/apalii/aws-audio-recog/assets/8919200/d15846be-fb7d-4ee9-a0cb-82a46a5af46e)
![image](https://github.com/apalii/aws-audio-recog/assets/8919200/dc7a8cf7-4f43-4b58-8b89-d1851330a296)
![image](https://github.com/apalii/aws-audio-recog/assets/8919200/5538e190-74c0-491a-b7e9-680a96276483)
![image](https://github.com/apalii/aws-audio-recog/assets/8919200/de9ffa01-dcae-40dd-b174-6554283a9d9b)

## Steps of the implementation

### audio file creation
File has been created at the https://www.narakeet.com/ with the following text from official aws docs:

```
Lambda runs your code on a high-availability compute infrastructure and performs all of the administration of the compute resources, including server and operating system maintenance, capacity provisioning and automatic scaling, and logging.
```
### Cloud infrustructure entities

1) API Gateway invoke URL: https://lvydkx8cvb.execute-api.us-east-1.amazonaws.com/dev
2) S3 bucket `apalii-audio-samples` with audio sample
3) S3 bucket `apalii-recognition-results` with transribes
4) Lambda: `recognition-task-consumer`
5) Lambda: `recognition-task-producer`
6) Lambda: `recognition-post-processing`
7) Lambda: `recognition-results`
8) SQS queue: `recognition`
9) DynamoDB: table `recognition-results`
10) DynamoDB: table `recognition-results`

### Flow
 - First lambda: `recognition-task-producer` takes arguments from the POST request and creates task at the SQS
 - SQS has another lambda `recognition-task-consumer` as a trigger which creates record in DynamoDB and also job at AWS Transcribe service
 - AWS Transcribe creates a file with the results which will trigger the 3rd lambda `recognition-post-processing`
 - Lambda `recognition-post-processing` reads the file, finds substring and saves results at the DynamoDb table `recognition-results`

### Request example

```
curl -X POST \
  https://lvydkx8cvb.execute-api.us-east-1.amazonaws.com/dev \
  -H 'Connection: keep-alive' \
  -H 'Content-Type: application/json' \
  -H 'Host: lvydkx8cvb.execute-api.us-east-1.amazonaws.com' \
  -d '{
    "audio_url": "s3://apalii-audio-samples/Lambda.mp3",
    "sentences": [
        "including server and operating system",
        "can you hear me?"
    ]
}'
```

### Results endpoint example

```
https://lvydkx8cvb.execute-api.us-east-1.amazonaws.com/dev/result?job_id=52fd082e-4e99-4189-9283-f420d63c5132
```
