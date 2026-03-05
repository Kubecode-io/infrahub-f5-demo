# Development notes

```
export INFRAHUB_ADDRESS="http://192.168.10.57:8000"
export INFRAHUB_API_TOKEN="44af444d-3b26-410d-9546-b758657e026c"
```
## Build venv
```
python -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```
## Load schema and data, build Ansible vars, build AVD configs and deploy
```
infrahubctl schema load schema/base_schema/ --branch main
infrahubctl schema check schema/f5_schema/ --branch F5_DEMO
infrahubctl schema load schema/f5_schema/ --branch F5_DEMO

python build_ansible_vars.py --branch main

cd ansible
ansible-playbook -i hosts f5_vip.yml

```
