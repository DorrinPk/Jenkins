### ECS Job

Let's face it. deploying to ECS for developers is difficult. They don't want to be making Services and tasks. A lot of details like "what should be log driver for this?" is not so interesting to them either. 

Devops to rescue! 

Here's a Jenkins job! I know a lot of people deploy with cloudformation but this will do as well. Have your job pass two parameters (name, env) to the job. The name is used in all resources created by the script.  
