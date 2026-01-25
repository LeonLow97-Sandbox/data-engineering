# Useful commands

```sh
terraform fmt # for formatting .tf files
terraform init
terraform plan
terraform destroy
terraform apply

export GOOGLE_CREDENTIALS=$(pwd)/keys/creds.json
echo $GOOGLE_CREDENTIALS
unset GOOGLE_CREDENTIALS # remove once done
```
