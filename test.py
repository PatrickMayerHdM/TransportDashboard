from datetime import datetime, timezone
print("Lokale Zeit:", datetime.now().strftime("%H:%M"))
print("UTC-Zeit:", datetime.now(timezone.utc).strftime("%H:%M"))
