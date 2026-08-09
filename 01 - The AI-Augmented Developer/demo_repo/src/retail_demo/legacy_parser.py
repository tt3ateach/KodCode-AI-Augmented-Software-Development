def parse_partner_feed(lines: list[str]) -> list[dict]:
    """
    Parse a partner pipe-delimited feed.

    Format:
        id|name|email|spend|active_flag

    This function is intentionally legacy-ish and under-defended.
    """
    out = []
    for ln in lines:
        x = [p.strip() for p in ln.split("|")]
        if len(x) < 5:
            continue

        st = x[4].lower()
        if st in ("y", "yes", "1", "true"):
            st = "active"
        else:
            st = "inactive"

        out.append(
            {
                "id": int(x[0]),
                "name": x[1].title(),
                "email": x[2].lower(),
                "spend": float(x[3]),
                "status": st,
            }
        )
    return out
