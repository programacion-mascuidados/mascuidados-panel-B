-- Índices para acelerar las consultas del panel (orden por creado_en DESC, id DESC).
-- Ejecutar una vez en la base Postgres del panel.

CREATE INDEX IF NOT EXISTS idx_leads_narela_panel
ON leads_narela (creado_en DESC NULLS LAST, id DESC)
WHERE estado IS NOT NULL;

CREATE INDEX IF NOT EXISTS idx_apify_leads_panel
ON apify_leads (creado_en DESC NULLS LAST, id DESC)
WHERE flujo IS NOT NULL AND btrim(flujo) <> '';
