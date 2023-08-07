# aws-audio-recog

Serverless audio recognition task

## Resources
![image](https://github.com/apalii/aws-audio-recog/assets/8919200/8930a554-aa33-4d17-82fe-b2426f2f0274)
![image](https://github.com/apalii/aws-audio-recog/assets/8919200/04aed209-c1e5-4656-94a9-e3de0b04c459)
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
5) Lambda: recognition-task-consumer
6) Lambda: recognition-task-producer
7) Lambda: recognition-post-processing
8) SQS queue: recognition
9) DynamoDB: table recognition-results
10) DynamoDB: table recognition-results

### Flow
