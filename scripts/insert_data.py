#!/usr/bin/env python3

from http.client import HTTPConnection
from json import dumps
from os import listdir

DEFAULT_DATA_PATH = ".data"

DEFAULT_OPENSEARCH_URL = "localhost"
DEFAULT_OPENSEARCH_PORT = 9200

DEFAULT_BULK_SIZE = 100000


def get_csv_files(path):
    return [f"{path}/{file}" for file in listdir(path) if file.endswith(".csv")]


def read_csv_data(filename):
    with open(filename, mode="r") as csv_file:
        lines = csv_file.readlines()
        return lines


def get_index(header, target):
    return header.index(target)


def parse_csv_data(csv_data):
    header = csv_data[0].split(",")

    index_of_id = get_index(header, "상가업소번호")
    index_of_name = get_index(header, "상호명")
    index_of_address = get_index(header, "지번주소")
    index_of_road_address = get_index(header, "도로명")

    data = []
    for line in csv_data[1:]:
        columns = line.split(",")
        data.append(
            {
                "index": {
                    "_index": "store",
                    "_id": columns[index_of_id].strip('"'),
                }
            }
        )
        data.append(
            {
                "name": columns[index_of_name].strip('"'),
                "address": columns[index_of_address].strip('"'),
                "road_address": columns[index_of_road_address].strip('"'),
            }
        )

    return data


def make_payload(data):
    return "\n".join([dumps(item, ensure_ascii=False) for item in data]) + "\n"


def insert_data(data):
    headers = {"Content-Type": "application/json"}
    payload = make_payload(data)

    connection = HTTPConnection(DEFAULT_OPENSEARCH_URL, DEFAULT_OPENSEARCH_PORT)
    connection.request("POST", "/_bulk", payload.encode("utf-8"), headers)

    response = connection.getresponse()

    if response.status != 200:
        message = f"failed to insert data: {response.status} {response.reason}"
        connection.close()
        raise Exception(message)

    else:
        connection.close()


if __name__ == "__main__":
    csv_files = get_csv_files(DEFAULT_DATA_PATH)

    for csv_file in csv_files:
        csv_data = read_csv_data(csv_file)
        data = parse_csv_data(csv_data)

        for offset in range(0, len(data), DEFAULT_BULK_SIZE):
            insert_data(data[offset : offset + DEFAULT_BULK_SIZE])
