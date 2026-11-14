output "web_url" { value = "https://${aws_cloudfront_distribution.web.domain_name}" }
output "api_url" { value = aws_apigatewayv2_api.api.api_endpoint }
output "user_pool_id" { value = aws_cognito_user_pool.planners.id }
output "client_id" { value = aws_cognito_user_pool_client.web.id }
