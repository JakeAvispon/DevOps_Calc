#!/bin/bash

# --- CONFIGURACIÓN ---
# ¡IMPORTANTE! Cambia esto por el nombre exacto de tu bucket en AWS
BUCKET_NAME="devops-calc-bucket" 

# Generamos un nombre de archivo con fecha y hora exacta
FECHA=$(date +"%Y-%m-%d_%H-%M-%S")
BACKUP_FILE="backup_calculadora_${FECHA}.tar.gz"
LOG_FILE="backup.log"

# Obtenemos el último cambio (commit) hecho en tu repositorio de Git
ULTIMO_CAMBIO=$(git log -1 --pretty=format:"%h - %s" 2>/dev/null || echo "Cambio detectado en el entorno local")

# --- INICIO DEL LOG ---
echo "==================================================" >> $LOG_FILE
echo "[$(date +"%Y-%m-%d %H:%M:%S")] Iniciando proceso de respaldo CI/CD..." >> $LOG_FILE
echo "Cambio registrado en el repo: $ULTIMO_CAMBIO" >> $LOG_FILE

# --- COMPRESIÓN ---
echo "Comprimiendo el directorio del proyecto..." >> $LOG_FILE
# Comprimimos todo, pero excluimos la carpeta oculta de git y el propio archivo comprimido
tar --exclude='./.git' --exclude="./*.tar.gz" -czf $BACKUP_FILE . >> $LOG_FILE 2>&1

# --- SUBIDA A S3 (EL RESPALDO) ---
if aws s3 cp $BACKUP_FILE s3://$BUCKET_NAME/ >> $LOG_FILE 2>&1; then
    echo "[ÉXITO] Respaldo ($BACKUP_FILE) subido correctamente al bucket." >> $LOG_FILE
else
    echo "[ERROR] Hubo un problema al subir el respaldo." >> $LOG_FILE
fi

# --- SUBIDA A S3 (EL LOG) ---
# Subimos el log al final para que AWS tenga el registro más reciente. 
# Esto te servirá para los Puntos 7 y 10 de tu tarea.
aws s3 cp $LOG_FILE s3://$BUCKET_NAME/ >> /dev/null 2>&1

echo "Proceso finalizado." >> $LOG_FILE
