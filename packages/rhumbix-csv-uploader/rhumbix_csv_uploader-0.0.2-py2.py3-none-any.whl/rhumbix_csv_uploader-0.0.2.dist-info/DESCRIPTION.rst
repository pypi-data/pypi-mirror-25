# DataLoader
## Setup
```
pip install rhumbix_csv_processor
```

## Usage
### Process CSV directory
`rhumbix_csv_processor csv_directory company_key api_key`

### Payroll CSV Processor
```python
from rhumbix_csv_uploader import payroll_processor
payroll_processor.process_csv("rhumbix_csv_uploader/test/exampleCSVs/rhumbix_payroll.csv")
```

### Work Order CSV Processor
```python
from rhumbix_csv_uploader import work_order_processor
work_order_processor.process_csv("rhumbix_csv_uploader/test/exampleCSVs/rhumbix_wo.csv")
```

### Job Cost CSV Processor
```python
from rhumbix_csv_uploader import job_cost_processor
job_cost_processor.process_csv("rhumbix_csv_uploader/test/exampleCSVs/rhumbix_job_cost_2.csv")
```



