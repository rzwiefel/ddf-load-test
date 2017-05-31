import sys, requests, re, time

def main():
    if len(sys.argv) != 4:
        print_usage_statement()
        return

    ingest_type = sys.argv[1]
    file_path = sys.argv[2]
    xml_type = sys.argv[3]

    with open(file_path, "r") as file:
        file_contents = file.read()

    requests.packages.urllib3.disable_warnings()
    headers = {
        "Content-Type" : "application/xml",
        "Authorization" : "Basic YWRtaW46YWRtaW4="
    }

    url = "https://localhost:8993/services/csw/"

    if ingest_type == "csw":
        file_contents = generate_csw_transaction_xml(file_contents, xml_type)
    elif ingest_type == "rest":
        url = "https://localhost:8993/services/catalog?transform=" + xml_type
    else:
        print_usage_statement()
        return

    start = time.time()
    response = requests.post(url, file_contents, headers=headers, verify=False)
    elapsed = time.time() - start
    num_inserted = get_number_of_inserted_records(response, ingest_type)

    print("{} record(s) inserted in {} seconds.".format(num_inserted, round(elapsed, 3)))


def get_number_of_inserted_records(response, ingest_type):
    if ingest_type == "csw":
        return get_number_of_csw_inserted_records(response)
    elif ingest_type == "rest":
        return get_number_of_rest_inserted_records()

def get_number_of_rest_inserted_records():
    return 1

def generate_csw_transaction_xml(file_contents, xml_type):
    csw_transaction_file = open("resources/cswInsertTransaction.xml", "r")
    csw_transaction_xml = csw_transaction_file.read()
    csw_transaction_xml = csw_transaction_xml.replace("${type}", xml_type)
    csw_transaction_xml = csw_transaction_xml.replace("${xml}", file_contents)
    return csw_transaction_xml

def get_number_of_csw_inserted_records(response):
    response_body = str(response.content, "utf-8")
    insert_response_regex = "<csw:totalInserted>[0-9]+</csw:totalInserted>"
    num_inserted = re.search(insert_response_regex, response_body).group(0)
    num_inserted = num_inserted.replace("<csw:totalInserted>", "")
    num_inserted = num_inserted.replace("</csw:totalInserted>", "")
    return int(num_inserted)

def print_usage_statement():
    print("Usage : python3 DDFIngestTest.py <csw | rest> <path-to-xml-file> <metadata-format>")

if __name__ == '__main__':
    main()