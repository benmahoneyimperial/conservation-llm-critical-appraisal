from datalab_sdk import DatalabClient

client = DatalabClient(api_key="YTzF4AGDlntoM8Xepa2YBtMpV58h2gLBZq7F4Lr_qS4")

execution = client.run_pipeline(
    pipeline_id="pl_DaOCkFJs7xHv",
    version=2,
    file_path="data/papers/papers_pdf/test_5/001.pdf",
)

print(type(execution))
print(dir(execution))
print(execution)