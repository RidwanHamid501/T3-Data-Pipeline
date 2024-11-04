provider "aws" {
  region = "eu-west-2"
}

data "aws_iam_role" "ecs_task_execution_role" {
  name = "ecsTaskExecutionRole"
}


resource "aws_ecs_task_definition" "task_definition" {
  family                   = "pipeline_task_definition"
  network_mode             = "awsvpc"
  requires_compatibilities = ["FARGATE"]
  cpu                      = "512" 
  memory                   = "1024" 
  execution_role_arn       = data.aws_iam_role.ecs_task_execution_role.arn

  container_definitions = jsonencode([
    {
      name      = "pipeline-container"
      image     = var.URI
      cpu       = 512
      memory    = 1024
      essential = true

      portMappings = [
        {
          containerPort = 80
          hostPort      = 80
          protocol      = "tcp"
          name          = "pipeline_port"
          appProtocol   = "http"
        }
      ]

      environment = [
        { name = "HOST", value = var.HOST },
        { name = "USERNAME", value = var.USERNAME },
        { name = "DATABASE_NAME", value = var.DATABASE_NAME },
        { name = "PASSWORD", value = var.PASSWORD },
        { name = "PORT", value = var.PORT },
        { name = "SCHEMA", value = var.SCHEMA },
      ]
    }
  ])
}
