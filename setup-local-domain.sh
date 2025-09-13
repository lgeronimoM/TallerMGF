#!/bin/bash
# setup-local-domain.sh

echo "🌐 Configurando dominio local tallermgf.local"

# Obtener la IP del cluster (ajustar según tu setup)
if command -v minikube &> /dev/null; then
    CLUSTER_IP=$(minikube ip)
    echo "📍 Detectado Minikube IP: $CLUSTER_IP"
elif kubectl get nodes -o wide | grep -q "docker-desktop"; then
    CLUSTER_IP="127.0.0.1"
    echo "📍 Detectado Docker Desktop, usando localhost"
else
    CLUSTER_IP="127.0.0.1"
    echo "📍 Usando localhost por defecto"
fi

# Verificar si ya existe la entrada
if grep -q "tallermgf.local" /etc/hosts; then
    echo "⚠️  tallermgf.local ya existe en /etc/hosts"
    echo "Entrada actual:"
    grep "tallermgf.local" /etc/hosts
else
    echo "➕ Añadiendo tallermgf.local a /etc/hosts"
    echo "$CLUSTER_IP tallermgf.local" | sudo tee -a /etc/hosts
    echo "✅ Dominio configurado"
fi

echo ""
echo "🧪 Para probar:"
echo "  curl http://tallermgf.local/health"
echo "  curl http://tallermgf.local/"

# Script para limpiar
cat > cleanup-domain.sh << 'EOF'
#!/bin/bash
echo "🧹 Removiendo tallermgf.local de /etc/hosts"
sudo sed -i '/tallermgf.local/d' /etc/hosts
echo "✅ Dominio removido"
EOF

chmod +x cleanup-domain.sh
echo "📝 Script de limpieza creado: cleanup-domain.sh"
