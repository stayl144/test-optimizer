FROM public.ecr.aws/lambda/python:3.12
COPY optimizer.py api.py ${LAMBDA_TASK_ROOT}/
# Default handler; the API Lambda overrides it in Terraform.
CMD ["optimizer.handler"]
