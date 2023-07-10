data "archive_file" "cf-archive" {
  type = "zip"
  source_dir = "../"
  output_path = "../cf-webhook-facebook.zip"
}

resource "yandex_function" "cf-webhook-facebook" {
  name = "cf-webhook-facebook"
  description = "Webhook для получения событий от Facebook Graph API (событий обновления сертов и появления новых поддоменов)"
  user_hash = data.archive_file.cf-archive.output_base64sha256 # uuid()  # Должна меняться, иначе версия функции не создастся
  runtime = "python311"
  entrypoint = "main.event_handler"
  memory = "128"  # 128 MB
  execution_timeout = "10"  # 10 seconds
  # service_account_id = "TODO"  # Пока не знаю, для чего SA для CF

  environment = {
    DOCUMENT_API_ENDPOINT = var.document_api_endpoint
    REGION_NAME = var.region_name
  }

  secrets {
    id = var.facebook-graph-api-secrets.secret_id
    version_id = var.facebook-graph-api-secrets.id
    key = "client_secret"
    environment_variable = "FACEBOOK_CLIENT_SECRET"
  }
  secrets {
    id = var.facebook-graph-api-secrets.secret_id
    version_id = var.facebook-graph-api-secrets.id
    key = "webhook_verification_token"
    environment_variable = "WEBHOOK_VERIFICATION_TOKEN"
  }
  secrets {
    id = var.aws-static-access-key.secret_id
    version_id = var.aws-static-access-key.id
    key = "client_id"
    environment_variable = "AWS_ACCESS_KEY_ID"
  }
  secrets {
    id = var.aws-static-access-key.secret_id
    version_id = var.aws-static-access-key.id
    key = "client_secret"
    environment_variable = "AWS_SECRET_ACCESS_KEY"
  }

  content {
    zip_filename = data.archive_file.cf-archive.output_path
  }
}
