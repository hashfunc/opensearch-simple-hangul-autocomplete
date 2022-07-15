FROM opensearchproject/opensearch:1.2.4

RUN /usr/share/opensearch/bin/opensearch-plugin install analysis-icu
