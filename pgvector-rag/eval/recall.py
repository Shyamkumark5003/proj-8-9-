import json
from app.access import get_user
from app.ask import retrieve

KS = (1, 3, 5)


def main():
    gold = json.load(open("eval/golden.json", encoding="utf-8"))
    user = get_user("admin_acme")   # admin ku ellam theriyum, so retrieval quality mattum measure aagum
    hits = {k: 0 for k in KS}
    for g in gold:
        got = [f"{r['source']}#{r['chunk_no']}" for r in retrieve(user, g["q"], max(KS))]
        for k in KS:
            if g["expected"] in got[:k]:
                hits[k] += 1
        if g["expected"] not in got[:3]:
            print("MISS@3:", g["q"], "| expected", g["expected"], "| got", got[:3])
    for k in KS:
        print(f"recall@{k} = {hits[k]}/{len(gold)} = {hits[k] / len(gold):.2f}")


if __name__ == "__main__":
    main()
