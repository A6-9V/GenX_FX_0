import argparse
import dns.resolver
import sys

def query_dns(domain, record_type):
    """
    Queries DNS for a specific record type.
    """
    try:
        answers = dns.resolver.resolve(domain, record_type)
        return [str(rdata) for rdata in answers]
    except (dns.resolver.NoAnswer, dns.resolver.NXDOMAIN, dns.resolver.NoNameservers):
        return []

def main():
    """
    Performs a DNS lookup for a given domain and returns various record types.
    """
    parser = argparse.ArgumentParser(description="Perform a DNS lookup for a given domain.")
    parser.add_argument("domain", help="The domain to look up.")
    args = parser.parse_args()

    domain_to_check = args.domain
    record_types = ["A", "AAAA", "MX", "CNAME", "NS", "TXT"]
    results = {}

    try:
        print(f"DNS lookup for {domain_to_check}:\n")

        for record_type in record_types:
            records = query_dns(domain_to_check, record_type)
            if records:
                results[record_type] = records

        if not results:
            print("No DNS records found for the specified domain.")
            return

        for record_type, records in results.items():
            print(f"--- {record_type} Records ---")
            for record in records:
                print(record)
            print()

    except Exception as e:
        print(f"An error occurred: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()