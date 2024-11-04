variable "HOST" {
    type = string
}

variable "PORT" {
    type = string
}

variable "DATABASE_NAME" {
    type = string
}

variable "USERNAME" {
    type = string
}

variable "PASSWORD" {
    type = string
    sensitive = true
}


variable "SCHEMA" {
    type = string
}

variable "URI" {
    type = string
}