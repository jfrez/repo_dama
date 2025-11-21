from setuptools import find_packages, setup

setup(
    name="utils_edu",
    version="0.1.0",
    packages=find_packages(),
    description="Utilidades de soporte para el proyecto educacional de gestión de datos",
    python_requires=">=3.9",
)
# Paquete instalable en editable para reutilizar helpers (DAMA: reutilización y arquitectura común en todo el demo).
