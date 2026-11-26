import json, os, urllib.request

def run_actor(actor: str, run_input: dict, timeout: int = 300) -> list[dict]:
    """Run an Apify Actor and return its dataset items. Needs APIFY_TOKEN in the environment.

    Uses the synchronous endpoint, which waits up to 300 seconds. For longer runs start the
    Actor with POST /v2/acts/{actor}/runs and read the dataset when the run has finished.
    """
    req = urllib.request.Request(
        f"https://api.apify.com/v2/acts/{actor}/run-sync-get-dataset-items",
        data=json.dumps(run_input).encode(),
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {os.environ['APIFY_TOKEN']}",
        },
    )
    with urllib.request.urlopen(req, timeout=timeout + 30) as resp:
        return json.load(resp)
