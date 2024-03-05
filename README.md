<h1 align="center">Welcome to apple-health-exporter 👋</h1>

<p>
  <a href="#" target="_blank">
    <img alt="License: MIT" src="https://img.shields.io/badge/License-MIT-yellow.svg" />
  </a>
  <a href="https://twitter.com/fuergaosi" target="_blank">
    <img alt="Twitter: fuergaosi" src="https://img.shields.io/twitter/follow/fuergaosi.svg?style=social" />
  </a>
</p>

> Explore your apple health with Grafana

![Dashbaord](./docs/dashboard.jpeg)

### update
- 使用如下命令，可以直接将json文件推送到server，最后到数据库。可以配合shortcut使用
`curl -X POST "http://192.168.2.21:38001/upload/lin" -H  "accept: application/json" -H  "Content-Type: multipart/form-data" -F "file=@test.json"`

- 也可以配合shortcut使用，比如

`cd ~ && cd Downloads && curl -X POST "http://192.168.2.21:38001/upload/lin" -H "accept: application/json" -H "Content-Type: multipart/form-data" -F "file=@$(ls -t HealthAutoExport-*.json | head -n1)" && rm HealthAutoExport*.json`
  

### 🏠 [Homepage](https://github.com/fuergaosi233/apple-health-exporter) | ✨ [Demo](https://grafana-health.y1s1.host/goto/egkRFfmIR?orgId=1)

[![Deploy on Railway](https://railway.app/button.svg)](https://railway.app/template/qZmI-e?referralCode=FaJtD_)

## Install

```sh
copy .env.example .env
# edit .env
docker compose up -d
```

## Config Grafana


1. Config Postgresql DB (Timescale)
![DB](./docs/postgresql.jpeg)
1. Import `dashboard.json` to your dashboard
![DB](./docs/import.png)
1. Enjoy it

## Start Sync data

1. Download [Health Auto Export - JSON+CSV](https://apps.apple.com/us/app/health-auto-export-json-csv/id1115567069) from App Store
2. Config Automations like this 
![Config](./docs/config.png)
> You might have to pay for it. There's a not free app. You can use `Shortcuts` to do this. But I don't know how to do it. If you know, please tell me.  

URL is `<your domain>/upload`  
Such as   
 `http://localhost:8000/upload`  
 `https://xxx.railway.app/upload`  
  
3. Click `Update`

👤 **Holegots**

* Twitter: [@fuergaosi](https://twitter.com/fuergaosi)
* Github: [@fuergaosi233](https://github.com/fuergaosi233)

## Show your support

Give a ⭐️ if this project helped you!

***
_This README was generated with ❤️ by [readme-md-generator](https://github.com/kefranabg/readme-md-generator)_
