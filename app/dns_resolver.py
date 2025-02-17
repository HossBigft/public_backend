from dns import resolver, reversename, rdatatype
from tldextract import extract


class RecordNotFoundError(Exception):
    def __init__(self, message):
        super().__init__(message)


def resolve_record(record: str, type: str, dns_list="internal"):
    custom_resolver = resolver.Resolver()
    match dns_list:
        case "internal":
            custom_resolver.nameservers = [
                "208.67.222.222",
                "208.67.220.220",
            ]
        case "free":
            custom_resolver.nameservers = ["8.8.8.8", "8.8.4.4"]
    try:
        match type:
            case "A":
                return [
                    ipval.to_text() for ipval in custom_resolver.resolve(record, type)
                ]
            case "PTR":
                addr_record = reversename.from_address(record)
                return [
                    ipval.to_text()
                    for ipval in custom_resolver.resolve(addr_record, type)
                ]
            case "MX":
                return [
                    ipval.to_text().split(" ")[1] for ipval in custom_resolver.resolve(record, "MX")
                ]

            case "NS":
                custom_resolver.nameservers = ["8.8.8.8", "8.8.4.4"]
                top_level_domain = extract(record).registered_domain
                primary_ns = str(
                    custom_resolver.resolve(top_level_domain, "SOA")[0].mname
                ).rstrip(".")
                primary_ns_ip = str(custom_resolver.resolve(primary_ns, "A")[0])
                custom_resolver.nameservers = [primary_ns_ip]

                ns_records = [
                    str(record) for record in custom_resolver.resolve(record, "NS")
                ]
                ns_records.sort()
                return ns_records
            case _:
                raise rdatatype.UnknownRdatatype
    except (resolver.NoAnswer, resolver.NXDOMAIN, resolver.NoNameservers) as exc:
        raise RecordNotFoundError(f"{type} record not found for {record}") from exc
