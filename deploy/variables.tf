variable "document_api_endpoint" {
  description = "Адрес YDB (DynamoDB), куда класть результаты из Yandex Forms"
  type = string
}

variable "region_name" {
  description = "Нужен для корректной работы с S3 API к DynamoDB"
  type = string
  default = "ru-central1"
}

variable "webhook_verification_token" {
  description = "TODO: написать точнее, для чего он и должен ли он быть в секрете"
  type = string
}

variable "facebook-client-secret" {
  description = "Секрет для подключения к Facebook Graph API"
}

variable "aws-client-id" {
  description = "Доступ к DynamoDB по токену от сервис-аккаунта"
}

variable "aws-client-secret" {
  description = "Доступ к DynamoDB по токену от сервис-аккаунта"
}
