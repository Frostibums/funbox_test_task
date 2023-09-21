from tldextract import extract


def get_domain_from_url(url: str) -> str | bool:
    """Extracts the domain from a given URL.

    Returns extracted domain if URL is valid, False otherwise
    """
    tsd, td, tsu = extract(url)
    if not all([td, tsu]):
        return False
    return f'{td}.{tsu}'
