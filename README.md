# OpenSearch Simple Hangul AutoComplete

OpenSearch로 구현하는 간단한 한글 자동완성

## 개요

ElasticSearch(OpenSearch)를 사용하여 한글 자동완성을 구현하는 경우 일반적으로 자소를 분리할 수 있는 플러그인을 사용합니다.

AWS OpenSearch 환경에서는 제공되는 플러그인만 사용할 수 있고 안타깝게도 한글 자소 분리 플러그인은 제공되지 않습니다.

이러한 상황에서 간단하게 한글 자동완성을 구현합니다.

## 준비

- Docker
  - OpenSearch를 머신에 직접 설치하는 경우에는 필요하지 않습니다.
- [소상공인시장진흥공단 상가(상권)정보](https://www.data.go.kr/data/15083033/fileData.do)
  - 테스트를 위한 데이터로 여기서는 소상공인시장진흥공단 상가(상권)정보를 사용합니다. 다른 데이터를 사용해도 문제 없습니다.

## 환경

- Docker (Compose)
- OpenSearch 1.2
  - AWS OpenSearch에서 사용할 수 있는 최신 환경입니다.

## 실행

### 환경 실행

```sh
docker-compose up
```

### 인덱스 생성

준비된 스크립트로 `store` 인덱스를 생성할 수 있습니다.

```sh
./scripts/create_index.py
```

### 데이터 입력

`소상공인시장진흥공단 상가(상권)정보`를 사용하는 경우 준비된 스크립트로 데이터를 입력할 수 있습니다.

/.data 디렉터리에 압축을 풀고 아래와 같이 스크립트를 실행합니다.

```sh
./scripts/insert_data.py
```
