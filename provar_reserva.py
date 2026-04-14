from calendar_handler import crear_cita

print("Intentant reservar cita per a l'Adrian...")
# El format ha de ser AAAA-MM-DDTHH:MM:SSZ
exit = crear_cita("Cita Perruqueria: Adrian (Corte Chico)", "2026-03-27T10:00:00Z")

if exit:
    print("✅ CITA GUARDADA! Mira el teu Google Calendar.")
else:
    print("❌ Error al guardar.")