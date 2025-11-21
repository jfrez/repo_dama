-- Estructura base para el proyecto educacional de comercio electrónico.
-- Diseñada para SQLite; si usas PostgreSQL, mapea cada conjunto a esquemas (raw, stage, core, dm).

-- RAW (batch e incremental)
CREATE TABLE IF NOT EXISTS raw_clientes_csv (
    customer_id TEXT NOT NULL,
    nombre TEXT,
    email TEXT,
    pais TEXT,
    region TEXT,
    creado_en TEXT,
    actualizado_en TEXT
);

CREATE TABLE IF NOT EXISTS raw_catalogo_csv (
    sku TEXT NOT NULL,
    nombre TEXT,
    categoria TEXT,
    precio NUMERIC,
    moneda TEXT,
    activo INTEGER,
    actualizado_en TEXT
);

CREATE TABLE IF NOT EXISTS raw_ordenes_csv (
    order_id TEXT NOT NULL,
    customer_id TEXT NOT NULL,
    order_date TEXT NOT NULL,
    status TEXT NOT NULL,
    currency TEXT NOT NULL,
    total_amount NUMERIC NOT NULL,
    updated_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS raw_order_items_csv (
    order_id TEXT NOT NULL,
    line_number INTEGER NOT NULL,
    sku TEXT NOT NULL,
    quantity INTEGER NOT NULL,
    unit_price NUMERIC NOT NULL,
    currency TEXT NOT NULL,
    updated_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS raw_ordenes_api (
    order_id TEXT NOT NULL,
    customer_id TEXT NOT NULL,
    order_date TEXT NOT NULL,
    status TEXT NOT NULL,
    currency TEXT NOT NULL,
    total_amount NUMERIC NOT NULL,
    updated_at TEXT NOT NULL,
    source TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS raw_order_items_api (
    order_id TEXT NOT NULL,
    line_number INTEGER NOT NULL,
    sku TEXT NOT NULL,
    quantity INTEGER NOT NULL,
    unit_price NUMERIC NOT NULL,
    currency TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    source TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS raw_payments_api (
    payment_id TEXT NOT NULL,
    order_id TEXT NOT NULL,
    method TEXT NOT NULL,
    status TEXT NOT NULL,
    amount NUMERIC NOT NULL,
    currency TEXT NOT NULL,
    paid_at TEXT,
    updated_at TEXT NOT NULL,
    source TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS raw_inventory_api (
    sku TEXT NOT NULL,
    warehouse TEXT NOT NULL,
    stock INTEGER NOT NULL,
    updated_at TEXT NOT NULL,
    source TEXT NOT NULL
);

-- STAGE
CREATE TABLE IF NOT EXISTS stage_clientes (
    customer_id TEXT NOT NULL,
    nombre TEXT,
    email TEXT,
    pais TEXT,
    region TEXT,
    creado_en TEXT,
    actualizado_en TEXT
);

CREATE TABLE IF NOT EXISTS stage_catalogo (
    sku TEXT NOT NULL,
    nombre TEXT,
    categoria TEXT,
    precio NUMERIC,
    moneda TEXT,
    activo INTEGER,
    actualizado_en TEXT
);

CREATE TABLE IF NOT EXISTS stage_ordenes (
    order_id TEXT NOT NULL,
    customer_id TEXT NOT NULL,
    order_date TEXT NOT NULL,
    status TEXT NOT NULL,
    currency TEXT NOT NULL,
    total_amount NUMERIC NOT NULL,
    updated_at TEXT NOT NULL,
    source TEXT
);

CREATE TABLE IF NOT EXISTS stage_order_items (
    order_id TEXT NOT NULL,
    line_number INTEGER NOT NULL,
    sku TEXT NOT NULL,
    quantity INTEGER NOT NULL,
    unit_price NUMERIC NOT NULL,
    currency TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    source TEXT
);

CREATE TABLE IF NOT EXISTS stage_payments (
    payment_id TEXT NOT NULL,
    order_id TEXT NOT NULL,
    method TEXT NOT NULL,
    status TEXT NOT NULL,
    amount NUMERIC NOT NULL,
    currency TEXT NOT NULL,
    paid_at TEXT,
    updated_at TEXT NOT NULL,
    source TEXT
);

CREATE TABLE IF NOT EXISTS stage_inventory (
    sku TEXT NOT NULL,
    warehouse TEXT NOT NULL,
    stock INTEGER NOT NULL,
    updated_at TEXT NOT NULL,
    source TEXT
);

-- CORE / DATAMART
CREATE TABLE IF NOT EXISTS core_ordenes (
    order_id TEXT NOT NULL,
    customer_id TEXT NOT NULL,
    order_date TEXT NOT NULL,
    status TEXT NOT NULL,
    currency TEXT NOT NULL,
    total_amount NUMERIC NOT NULL,
    items_amount NUMERIC,
    updated_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS core_order_items (
    order_id TEXT NOT NULL,
    line_number INTEGER NOT NULL,
    sku TEXT NOT NULL,
    quantity INTEGER NOT NULL,
    unit_price NUMERIC NOT NULL,
    currency TEXT NOT NULL,
    updated_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS dm_sales_diarias (
    fecha DATE NOT NULL,
    categoria TEXT,
    total_ordenes INTEGER NOT NULL,
    total_items INTEGER NOT NULL,
    ingresos NUMERIC NOT NULL
);

CREATE TABLE IF NOT EXISTS dm_pagos_diarios (
    fecha DATE NOT NULL,
    metodo TEXT,
    estado TEXT,
    monto NUMERIC NOT NULL,
    pagos INTEGER NOT NULL
);

CREATE TABLE IF NOT EXISTS dm_inventario_snapshot (
    fecha DATE NOT NULL,
    sku TEXT NOT NULL,
    warehouse TEXT NOT NULL,
    stock INTEGER NOT NULL
);

CREATE TABLE IF NOT EXISTS control_ejecuciones (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    proceso TEXT NOT NULL,
    estado TEXT NOT NULL,
    registros INTEGER DEFAULT 0,
    detalle TEXT,
    ejecutado_en TEXT NOT NULL
);

-- Índices básicos
CREATE INDEX IF NOT EXISTS idx_raw_orders_date ON raw_ordenes_csv (order_date);
CREATE INDEX IF NOT EXISTS idx_raw_orders_api_date ON raw_ordenes_api (order_date);
CREATE INDEX IF NOT EXISTS idx_stage_orders_date ON stage_ordenes (order_date);
CREATE INDEX IF NOT EXISTS idx_core_orders_date ON core_ordenes (order_date);
CREATE INDEX IF NOT EXISTS idx_dm_sales_fecha ON dm_sales_diarias (fecha);
